# Overview

This choice of language and framework for the submission is Python3 with Flask.  This choice was made as it is the language I currently use most often, and provided the best foundation for me to build a PoC codebase for the test and to submit in a timely manner.

The service assumes that a live stream will periodically maintain a lease with this service that will expire if not renewed within a set time limit.


# Assumptions

* The level of submission for this test should be to a proof-of-concept, rather than production ready
* A subscribe/renew/expire pattern is applicable for managing concurrent streams, on the basis that this would be an online service
* It cannot be relied upon that a stream will be ended gracefully, or that this service will receive any notification
* Performance metrics are not stated, but given the scale of the organisation an aim of 30,000 concurrent streams with a peak load of 500tps might be a reasonable aim
* The service will not be consumed directly by a client, but by another trusted service
* A unique `subscriber_id` is available to identify a subscription that holds a limit of 3 concurrent streams
* A unique `stream_id` is available to identify an individual live stream
* Upon individual component failure that it may be acceptable to temporarily allow >3 concurrent streams, but that the architecture will allow these to be automatically pared back on service restoration
* Where > 3 streams are requested, the preference is to continue existing streams and deny the new one(s)


# Availability

The service is built in such a way that data is short-term in nature and can be quickly re-created by the consumers.  Therefore upon component failure service can be maintained by destroying and re-generating pods/containers.  Data recovery would be achieved automatically within the timeframe of a lease.


# Scaling for Performance

The service as built for this submission is proven capable of 100+tps based on the AWS t2.micro instance upon which it is hosted.


## Optimisation

The solution is not optimised.  The first avenue to performance scaling would be to review the codebase and supporting components, e.g.:

* Flask is used to provide the endpoints in naked format.  Alternative higher performance options could be investigated
* The code has some expensive operations, which could be potentially moved away from from main flow
* If locking of the main dict becomes a bottleneck, then sharding and locking of individual dict objects may provide relief

In addition to optimisation of the codebase, it is important to ensure that the most appropriate hosting solution is selected.  At this point the solution is hosted on AWS Elastic Container Service using a `t2.micro` instance.


## Distribution

The PoC is built as a single instance that can be scaled only vertically (i.e. adding hardware/VM resources).

To adapt the service to be horizontally scalable I might implement a sharding mechanism based on the subscriber ID.  The approach would provide a mechanism to predictably distribute load across many nodes in an even manner (depending on selected hash/algorithm).


# Running

The service can be run locally, or accessed via it's online implementation.

## Local

````
docker build -t stream_register .
docker run -p 5005:5005 stream_register &

curl http://localhost:5005/renew/sub_id/str_0
curl http://localhost:5005/renew/sub_id/str_1
curl http://localhost:5005/renew/sub_id/str_2
curl http://localhost:5005/renew/sub_id/str_3

# To kill the container
docker kill $(docker ps | grep stream_register | awk '{print $1}')
````

## Online

````
curl http://stream-register-lb-1461482584.eu-west-1.elb.amazonaws.com/renew/sub_id/str_id
````


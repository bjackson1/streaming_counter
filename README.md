# Overview

Firstly, the test is written in Python.  This choice was made as it is the language I currently use most often, and provided the best foundation for me to build a PoC codebase for the test and to submit in a timely manner.

The service assumes that


# Assumptions

* A subscribe/renew/expire pattern is applicable for managing concurrent streams, on the basis that this would be an online service
* Given the availability/consistency/partition trilema, that availability is most important
* It cannot be relied upon that a stream will be ended gracefully
* The level of submission should be to a proof-of-concept, rather than production ready
* Performance metrics are not stated, but given the scale of the organisation an aim of 30,000 concurrent streams with a peak load of 300tps might be a reasonable aim
* The service will not be consumed directly by a client, but by another trusted service
* A unique subscriber_id is available to identify a subscription that holds a limit of 3 concurrent streams
* A unique stream_id is available to identify an individual live stream
* Upon individual component failure that it may be accessible to temporarily allow >3 concurrent streams, but that the architecture will allow these to be automatically pared back on service restoration


# Availability

The service is built in such a way that data is short-term in nature and can be quickly re-created by the consumers.  Therefore upon failure of an component service can be maintained by destroying and regeneration free from replication or data recovery considerations.

Combined with the sharding approach used for performance scaling


# Scaling for Performance

The PoC is built as a single instance that can be scaled only vertically (i.e. adding hardware/VM resources).

A branch is provided in the repository called `sharding_spike` to demonstrate implementation of horizontal scaling through distribution of load based on a high performance hash of the subscriber_id.


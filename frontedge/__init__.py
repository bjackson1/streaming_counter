from flask import Flask, request, make_response
from stream_register import stream_register

app = Flask(__name__)

stream_register = stream_register()

@app.route('/renew/<subscriber_id>/<stream_id>')
def renew(subscriber_id, stream_id):
    try:
        renewed = stream_register.add(subscriber_id, stream_id)

        return "{'status': '%s'}" % ('OK' if renewed == True else 'SubscriptionLimitReached'), 200
    except:
        # Would expect to include handling of one or more specific exception types, and
        #  any appropriate system logging for failure analysis.  Additionally any exception
        #  detail can optionally be passed back with the response if desired
        return "{'status': 'RequestFailed'}", 500


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5005, threaded=True, use_reloader=False)

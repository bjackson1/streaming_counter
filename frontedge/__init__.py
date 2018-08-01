from flask import Flask, request, make_response
from stream_register import stream_register
import json

app = Flask(__name__)

stream_register = stream_register()

@app.route('/renew/<subscriber_id>/<stream_id>')
def renew(subscriber_id, stream_id):
    try:
        renewed = stream_register.renew(subscriber_id, stream_id)

        status = 'OK' if renewed else 'SubscriptionLimitReached'
        web_response_status = 200

    except:
        # Would expect to include handling of one or more specific exception types, and
        #  any appropriate system logging for failure analysis.  Additionally any exception
        #  detail can optionally be passed back with the response if desired
        status = 'RequestFailed'
        web_response_status = 500

    response = json.dumps({'status': status})
    return response, web_response_status


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5005, threaded=True, use_reloader=False)

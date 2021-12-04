from flask import Flask
import smtplib
import time

app = Flask(__name__)


@app.route('/refresh', methods=['GET'])
def refresh():
    return 'refresh'


if __name__ == '__main__':
    app.run(host='10.0.0.63', threaded=True)


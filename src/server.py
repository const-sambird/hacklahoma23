import requests

def sendScore(ticks_data):
    requests.post("https://nguyentendo.sambird.dev/api/score", data = ticks_data)

# from flask import Flask
# from flask import request
#
# app = Flask(__name__)
#
# @app.route('/newScore', methods=['GET', 'POST'])
# def sendScore(tick_data):
#     if request.method == 'POST':
#         return tick_data
#
#
# if __name__ == '__main__':
#    app.run(debug = True)
from flask import Flask
from flask import request

app = Flask(__name__)

@app.route('/newScore', methods=['GET', 'POST'])
def sendScore(tick_data):
    if request.method == 'POST':
        return tick_data


if __name__ == '__main__':
   app.run(debug = True)
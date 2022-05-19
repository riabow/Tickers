import time
from random import random
import json
from flask import Flask, render_template
from flask_sock import Sock

app = Flask(__name__)
sock = Sock(app)

def generate_movement():
    movement = -1 if random() < 0.5 else 1
    return movement

sel = '<select onchange="tickers_changed()" name="tickers" id="tickers">'
TICKERS = {} #Здесь словарь с тикерами
for n in range(0,100):
    tname = "ticker_{0:0>2}".format(n)
    sel += f'<option value="{tname}">{tname}</option>'
    TICKERS[tname] = 0
sel += "</select>"

@app.route('/')
def index():
    return render_template('index2.html', sel=sel)


def generate_next_data(tickers):
    """ генерируем следуюшие значения """
    for n in tickers:
        tickers[n] += generate_movement()
    return tickers


@sock.route('/echo')
def echo(sock):
    global TICKERS
    while True:
        #data = sock.receive()
        n = 0
        # при установлении соединения уходим в бесконечный цикл 
        # и отправляем новые данные на фронт
        while True:
            js = json.dumps(generate_next_data(TICKERS))
            sock.send(js)
            n += 1
            time.sleep(1)




if __name__ == "__main__":
    app.run(debug=True)


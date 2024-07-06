from flask import Flask, render_template
from nengo import nengo

app = Flask(__name__)

app.config["DEBUG"] = True

@app.route('/')
def hello () -> str:
    return "Hallo Webwelt from Flask"

@app.route('/nengo/<datumstr>')
def nengostr(datumstr) -> str:
    return nengo(datumstr)

if __name__ == "__main__":
    app.run()

from flask import Flask
import db_init

app = Flask(__name__)


@app.route('/index')
def index():
    return 'Hello World'

if __name__ == "__main__":
    app.run()

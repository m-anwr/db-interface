from flask import Flask, render_template, request, redirect, url_for
from driver import Driver
import db_init

app = Flask(__name__)
db_init.init()


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/drivers')
def drivers():
    return render_template("drivers/index.html", drivers=Driver.all())


@app.route('/drivers/new', methods=['GET', 'POST'])
def new_driver():
    if request.method == 'POST':
        d = Driver(request.form.to_dict(flat=True))
        d.save()
        return redirect(url_for('drivers'))
    return render_template('drivers/new.html')


@app.errorhandler(404)
def page_not_found(e):
    return (render_template("404.html"), 400)


if __name__ == "__main__":
    app.run()

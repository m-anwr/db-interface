from flask import Flask, render_template, request, redirect, url_for
from driver import Driver
from street import Street
from trafficlight import Trafficlight
from intersection import Intersection
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

@app.route('/streets')
def streets():
    return render_template("streets/index.html", streets=Street.all())


@app.route('/streets/new', methods=['GET', 'POST'])
def new_street():
    if request.method == 'POST':
        d = Street(request.form.to_dict(flat=True))
        d.save()
        return redirect(url_for('streets'))
    return render_template('streets/new.html')

@app.route('/trafficlights')
def trafficlights():
    return render_template("trafficlights/index.html", traffic_lights=Trafficlight.all())


@app.route('/trafficlights/new', methods=['GET', 'POST'])
def new_trafficlight():
    if request.method == 'POST':
        d = Trafficlight(request.form.to_dict(flat=True))
        d.save()
        return redirect(url_for('trafficlights'))
    return render_template('trafficlights/new.html')

@app.route('/intersections')
def intersections():
    return render_template("intersections/index.html", intersections=Intersection.all())


@app.route('/intersections/new', methods=['GET', 'POST'])
def new_intersection():
    if request.method == 'POST':
        d = Intersection(request.form.to_dict(flat=True))
        d.save()
        return redirect(url_for('intersections'))
    return render_template('intersections/new.html')


@app.errorhandler(404)
def page_not_found(e):
    return (render_template("404.html"), 400)


if __name__ == "__main__":
    app.run()

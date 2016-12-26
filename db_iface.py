from flask import Flask, render_template, request, redirect, url_for
from driver import Driver
from street import Street
from trafficlight import Trafficlight
from intersection import Intersection
from emergencyvehicle import EmergencyVehicle
import db_init


app = Flask(__name__)
db_init.init()


@app.route('/')
def index():
    return render_template("index.html")


def _collection(model_class):
    collection = []
    filters = request.args.to_dict(flat=True)
    filters = {k: v for k, v in filters.items() if v != ''}

    if filters:
        if model_class.__name__ == "Street":
            collection = model_class.where_range(filters)
        else:
            collection = model_class.where(filters)
    else:
        collection = model_class.all()

    return collection


@app.route('/drivers')
def drivers():
    collection = _collection(Driver)
    return render_template("drivers/index.html", drivers=collection)


@app.route('/drivers/new', methods=['GET', 'POST'])
def new_driver():
    if request.method == 'POST':
        d = Driver(request.form.to_dict(flat=True))
        d.save()
        return redirect(url_for('drivers'))
    return render_template('drivers/new.html')


@app.route('/drivers/<username>')
def show_driver(username):
    driver = Driver.find('username', username)
    if driver is not None:
        return render_template("drivers/show.html", driver=driver)
    else:
        return page_not_found(None)


@app.route('/drivers/<username>/edit', methods=['GET', 'POST'])
def edit_driver(username):
    driver = Driver.find('username', username)
    if request.method == 'POST':
        form_data = request.form.to_dict(flat=True)
        form_data = {k: v for k, v in form_data.items() if driver.data[k] != v}
        driver.update(form_data)
        return redirect(
            url_for('show_driver', username=driver.data['username'])
        )
    else:
        return render_template('drivers/edit.html', driver=driver)


@app.route('/drivers/<username>/delete')
def delete_driver(username):
    driver = Driver.find('username', username)
    driver.delete()
    return redirect(url_for('drivers'))


@app.route('/streets')
def streets():
    collection = _collection(Street)
    return render_template("streets/index.html", streets=collection)


@app.route('/streets/new', methods=['GET', 'POST'])
def new_street():
    if request.method == 'POST':
        d = Street(request.form.to_dict(flat=True))
        d.save()
        return redirect(url_for('streets'))
    return render_template('streets/new.html')


@app.route('/trafficlights')
def trafficlights():
    collection = _collection(Trafficlight)
    return render_template(
        "trafficlights/index.html",
        traffic_lights=collection
    )


@app.route('/trafficlights/new', methods=['GET', 'POST'])
def new_trafficlight():
    if request.method == 'POST':
        d = Trafficlight(request.form.to_dict(flat=True))
        d.save()
        return redirect(url_for('trafficlights'))
    return render_template('trafficlights/new.html')


@app.route('/intersections')
def intersections():
    collection = _collection(Intersection)
    return render_template("intersections/index.html", intersections=collection)


@app.route('/intersections/new', methods=['GET', 'POST'])
def new_intersection():
    if request.method == 'POST':
        d = Intersection(request.form.to_dict(flat=True))
        d.save()
        return redirect(url_for('intersections'))
    return render_template('intersections/new.html')


@app.route('/emergency_vehicles')
def emergency_vehicles():
    collection = _collection(EmergencyVehicle)
    return render_template("emergency_vehicles/index.html", emergency_vehicles=collection)


@app.route('/emergency_vehicles/new', methods=['GET', 'POST'])
def new_emergency_vehicle():
    if request.method == 'POST':
        d = EmergencyVehicle(request.form.to_dict(flat=True))
        d.save()
        return redirect(url_for('emergency_vehicles'))
    return render_template('emergency_vehicles/new.html')

@app.route('/emergency_vehicles/<id>')
def show_emergency_vehicle(id):
    emergency_vehicle = EmergencyVehicle.find('id', id)
    if emergency_vehicle is not None:
        return render_template("emergency_vehicles/show.html", emergency_vehicle=emergency_vehicle)
    else:
        return page_not_found(None)


@app.route('/emergency_vehicles/<id>/edit', methods=['GET', 'POST'])
def edit_emergency_vehicle(id):
    emergency_vehicle = EmergencyVehicle.find('id', id)
    if request.method == 'POST':
        form_data = request.form.to_dict(flat=True)
        form_data = {k: v for k, v in form_data.items() if emergency_vehicle.data[k] != v}
        emergency_vehicle.update(form_data)
        return redirect(
            url_for('show_emergency_vehicle', id=emergency_vehicle.data['id'])
        )
    else:
        return render_template('emergency_vehicles/edit.html', emergency_vehicle=emergency_vehicle)


@app.route('/emergency_vehicles/<id>/delete')
def delete_emergency_vehicle(id):
    emergency_vehicle = EmergencyVehicle.find('id', id)
    emergency_vehicle.delete()
    return redirect(url_for('emergency_vehicles'))


@app.errorhandler(404)
def page_not_found(e):
    return (render_template("404.html"), 400)


if __name__ == "__main__":
    app.run()

from flask import Flask, render_template, request, redirect, url_for
from driver import Driver
from street import Street
from trafficlight import Trafficlight
from intersection import Intersection
from emergencyvehicle import EmergencyVehicle
from uses import Uses
import db_init
import datetime


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

    associated_vehicles = EmergencyVehicle.join(
        driver,
        'uses',
        'emergency_vehicle_id',
        'driver_national_id'
    )

    associated_vehicles_ids = [v.data['id'] for v in associated_vehicles]
    rest_of_evs = list(
        filter(
            lambda x: x.data['id'] not in associated_vehicles_ids,
            EmergencyVehicle.all()
        )
    )

    if driver is not None:
        return render_template(
            "drivers/show.html",
            driver=driver,
            associated_vehicles=associated_vehicles,
            rest_of_evs=rest_of_evs
        )
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


@app.route('/drivers/<username>/assign_to_vehicle', methods=['POST'])
def assign_driver_to_vehicle(username):
    form_data = request.form.to_dict(flat=True)
    form_data['date'] = str(datetime.date.today())
    u = Uses(form_data)
    u.save()
    return redirect(url_for('show_driver', username=username))


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

@app.route('/streets/<id>')
def show_street(id):
    street = Street.find('id', id)
    if street is not None:
        return render_template("streets/show.html", street=street)
    else:
        return page_not_found(None)


@app.route('/streets/<id>/edit', methods=['GET', 'POST'])
def edit_street(id):
    street = Street.find('id', id)
    if request.method == 'POST':
        form_data = request.form.to_dict(flat=True)
        form_data = {k: v for k, v in form_data.items() if street.data[k] != v}
        street.update(form_data)
        return redirect(
            url_for('show_street', id=street.data['id'])
        )
    else:
        return render_template('streets/edit.html', street=street)


@app.route('/streets/<id>/delete')
def delete_street(id):
    street = Street.find('id', id)
    street.delete()
    return redirect(url_for('streets'))


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

@app.route('/trafficlights/<id>')
def show_trafficlight(id):
    trafficlight = Trafficlight.find('id', id)
    if trafficlight is not None:
        return render_template("trafficlights/show.html", trafficlight=trafficlight)
    else:
        return page_not_found(None)


@app.route('/trafficlights/<id>/edit', methods=['GET', 'POST'])
def edit_trafficlight(id):
    trafficlight = Trafficlight.find('id', id)
    if request.method == 'POST':
        form_data = request.form.to_dict(flat=True)
        form_data = {k: v for k, v in form_data.items() if trafficlight.data[k] != v}
        trafficlight.update(form_data)
        return redirect(
            url_for('show_trafficlight', id=trafficlight.data['id'])
        )
    else:
        return render_template('trafficlights/edit.html', trafficlight=trafficlight)


@app.route('/trafficlights/<id>/delete')
def delete_trafficlight(id):
    trafficlight = Trafficlight.find('id', id)
    trafficlight.delete()
    return redirect(url_for('trafficlights'))


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


@app.route('/intersections/<mac>')
def show_intersection(mac):
    intersection = Intersection.find('mac', mac)
    if intersection is not None:
        return render_template("intersections/show.html", intersection=intersection)
    else:
        return page_not_found(None)


@app.route('/intersections/<mac>/edit', methods=['GET', 'POST'])
def edit_intersection(mac):
    intersection = Intersection.find('mac', mac)
    if request.method == 'POST':
        form_data = request.form.to_dict(flat=True)
        form_data = {k: v for k, v in form_data.items() if intersection.data[k] != v}
        intersection.update(form_data)
        return redirect(
            url_for('show_intersection', mac=intersection.data['mac'])
        )
    else:
        return render_template('intersections/edit.html', intersection=intersection)


@app.route('/intersections/<mac>/delete')
def delete_intersection(mac):
    intersection = Intersection.find('mac', mac)
    intersection.delete() 
    return redirect(url_for('intersections'))


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

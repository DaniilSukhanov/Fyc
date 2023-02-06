import flask
from data.database import Database
from data.cars import Cars
import os

app = flask.Flask(__name__)


@app.route("/")
def index():
    with Database() as session:
        name_cars = session.query(Cars).all()
    return flask.render_template(
        "index.html",
        cars=[(car.id, car.name_car) for car in name_cars]
    )


@app.route("/car/<int:id_car>")
def car(id_car: int):
    with Database() as session:
        current_car = session.query(Cars).filter(Cars.id == id_car).first()
    if current_car is None:
        return flask.redirect("/")
    data_car = current_car.get_all_parameters()
    images_current_car = data_car["images"]
    images = enumerate(
        filename for filename in os.listdir(f"static/img/{images_current_car}")
    )
    data_car["list_images"] = images
    return flask.render_template("car.html", **data_car)


def main():
    Database.connect("db/db.db")
    app.run(port=8080, host="127.0.0.1")


if __name__ == "__main__":
    main()

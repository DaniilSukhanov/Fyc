import flask
from flask_login import login_user, LoginManager, login_required,\
    logout_user, current_user

from data.database import Database
from data.cars import Cars
import os

from data.login_form import LoginForm
from data.user import User
from data.register_form import RegisterForm


app = flask.Flask(__name__)
app.config["SECRET_KEY"] = "SECRET_KEY"

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id: str):
    with Database() as session:
        user = session.query(User).get(int(user_id))
    return user


@app.route("/cars/<int:type_cars>")
def cars(type_cars: int):
    with Database() as session:
        name_cars = session.query(Cars).all()
    return flask.render_template(
        "cars.html",
        cars=[(car.id, car.name_car) for car in name_cars if car.type == type_cars]
    )


@app.route("/")
def index():
    with Database() as session:
        type_cars = tuple(set(car.type for car in session.query(Cars).all()))
    return flask.render_template(
        "index.html", type_cars=type_cars, dict_cars={
            0: "Легковые",
            1: "Минивены"
        }
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


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.is_submitted():
        with Database() as session:
            user_email = session.query(User.email).filter(
                User.email == form.email.data
            ).all()
            if user_email:
                return flask.render_template(
                    'register.html', form=form,
                    message='Пользователь с такой почтой есть.'
                )
            if form.repeated_password.data != form.password.data:
                return flask.render_template(
                    'register.html', form=form,
                    message='Пароли не совпали.'
                )
            user = User()
            user.name = form.name.data
            user.surname = form.surname.data
            user.email = form.email.data
            user.set_password(form.password.data)
            user.age = form.ago.data
            session.add(user)
            session.commit()
        return flask.redirect("/")
    return flask.render_template("register.html", form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        with Database() as session:
            user = session.query(User).filter(User.email == form.email.data).first()
            if user and user.check_password(form.password.data):
                login_user(user, remember=form.remember_me.data)
                return flask.redirect("/")
        return flask.render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return flask.render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return flask.redirect("/")


def main():
    Database.connect("db/db.db")
    app.run(port=8081, host="127.0.0.1")


if __name__ == "__main__":
    main()

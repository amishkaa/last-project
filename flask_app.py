from flask import Flask, render_template, request, redirect
from flask_login import LoginManager, login_required, logout_user, login_user, current_user
from hashlib import sha256

from data import db_session
from data.sql_models import User, Wish
from data.forms.registration_form import RegistrationForm
from data.forms.login_form import LoginForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/', methods=['GET', 'POST'])
@app.route('/wishes', methods=['GET', 'POST'])
def wishes():
    if not current_user.is_authenticated:
        return redirect('/login')
    db_sess = db_session.create_session()
    users = sorted(db_sess.query(User.id, User.email, User.name).all(), key=lambda user: user.id)
    wishes = db_sess.query(Wish).all()
    return render_template('wishes.html', profile_name=current_user.name, wishes=wishes, users=users)


@app.route('/new_wish', methods=['GET', 'POST'])
def new_wish():
    if not current_user.is_authenticated:
        return redirect('/login')
    if request.method == 'POST' and not request.form.get('title'):
        db_sess = db_session.create_session()
        new_wish = Wish()
        new_wish.title = request.form.get('wish_title')
        new_wish.text = request.form.get('text')
        new_wish.user_id = current_user.id
        db_sess.add(new_wish)
        db_sess.commit()
        return redirect('/')
    return render_template('new_wish.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        password_h = sha256(form.password.data.encode()).hexdigest()
        if user and user.check(password_h, form.email.data, form.username.data):
            login_user(user)
            return redirect("/")
        return render_template('login.html',
                               message="Неверная информация",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    form = RegistrationForm()
    if request.method == 'POST':
        db_sess = db_session.create_session()
        u = db_sess.query(User).filter(User.email == form.email.data).first()
        if not u:
            if form.maniac.data:
                return render_template('registration.html', message="Извините, но вы маньяк", form=form)
            user = User()
            user.name = form.username.data
            user.email = form.email.data
            user.hashed_password = sha256(form.password.data.encode()).hexdigest()
            user.total_wishes = 0
            user.fulfilled_wishes = 0
            db_sess.add(user)
            db_sess.commit()
            login_user(user)
            return redirect('/')
        return render_template('registration.html', message="Эта эл. почта уже использована", form=form)
    return render_template('registration.html', title='Регистрация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/login")


def main():
    db_session.global_init("db/database.db")
    app.run(debug=True, port=7000, host="127.0.0.1")


if __name__ == '__main__':
    main()

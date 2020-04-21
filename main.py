from flask import Flask, render_template, redirect, abort, request, make_response, jsonify
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, FileField
from flask_restful import reqparse, abort, Api, Resource
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired
import sqlalchemy_serializer
from requests import get, put, delete
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from datetime import date
from data import db_session
from data.users import User
from data.categories import Categories
from data.INFORM import Info
from data.products import Product
from data.stories import Stories
from data.trainers import Trainer
from data.comments import Comment
from data import users_resource
from data import сategories_resource
from data import products_resource
from data import stories_resource
from data import trainers_resource

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
db_session.global_init("db/magazin.sqlite")
login_manager = LoginManager()
login_manager.init_app(app)
api = Api(app)
session = db_session.create_session()
inform = session.query(Info).get(1)


def abort_if_user_not_found(user_id):
    user = session.query(User).get(user_id)
    if not user:
        abort(404, message=f"User {user_id} not found")


def abort_if_products_not_found(products_id):
    products = session.query(Product).get(products_id)
    if not products:
        abort(404, message=f"Product {products_id} not found")


def pass_treners():
    list_clientele = []
    id_li_client = {}
    id_treners = {}
    for tran in session.query(Trainer):
        id_treners[str(tran.id)] = [tran.surname, tran.name, tran.age, tran.img_trainer, tran.email, tran.telefon]
        for cli in tran.clientele.split(', '):
            list_clientele.append(int(cli))
        id_li_client[str(tran.id)] = list_clientele
        list_clientele = []
    return [id_treners, id_li_client]


def pass_catal():
    id_product_list = []
    categorid = {}
    list_product = {}
    for cate in session.query(Categories):
        categorid[str(cate.id)] = [cate.name, cate.products]
        for prod in cate.products.split(', '):
            id_product_list.append(int(prod))
        list_product[str(cate.id)] = id_product_list
        id_product_list = []
    return [categorid, list_product]


class InfoForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    start_text = StringField('start_text', validators=[DataRequired()])
    telefon = StringField('telefon', validators=[DataRequired()])
    admin = StringField('admin', validators=[DataRequired()])
    derektor = StringField('derektor', validators=[DataRequired()])
    submit = SubmitField('применить')


class fileForm(FlaskForm):
    FILE = FileField('FILE', validators=[DataRequired()])
    submit = SubmitField('применить')


class RegisterForm(FlaskForm):
    login = StringField('login', validators=[DataRequired()])
    surname = StringField('surname', validators=[DataRequired()])
    name = StringField('name', validators=[DataRequired()])
    age = IntegerField('age', validators=[DataRequired()])
    address = StringField('address', validators=[DataRequired()])
    email = EmailField('email', validators=[DataRequired()])
    password_1 = PasswordField('password', validators=[DataRequired()])
    password_2 = PasswordField('loop password', validators=[DataRequired()])
    submit = SubmitField('setup')


class LoginForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class ProductForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    coin = IntegerField('coin', validators=[DataRequired()])
    count = IntegerField('count', validators=[DataRequired()])
    info = StringField('info', validators=[DataRequired()])
    submit = SubmitField('Add product')


class CategoriesForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    products = StringField('products_list', validators=[DataRequired()])
    submit = SubmitField('Add categories')


class TrainerForm(FlaskForm):
    surname = StringField('surname', validators=[DataRequired()])
    name = StringField('name', validators=[DataRequired()])
    age = IntegerField('age', validators=[DataRequired()])
    email = EmailField('email', validators=[DataRequired()])
    telefon = StringField('Телефон', validators=[DataRequired()])
    submit = SubmitField('Add trainer')


@app.route('/admin1234567', methods=['GET', 'POST'])
def adminka():
    global inform
    categorid = pass_catal()[0]
    list_product = pass_catal()[1]
    form = InfoForm()
    form_product = ProductForm()
    form_trainer = TrainerForm()
    form_categories = CategoriesForm()
    if form.validate_on_submit():
        try:
            inform.name = form.name.data
            inform.start_text = form.start_text.data
            inform.telefon = form.telefon.data
            inform.admin = form.admin.data
            inform.derektor = form.admin.data
            session.commit()
        except Exception as er:
            abort(404, message=f"Product {er} not found")
    if form_product.validate_on_submit():
        try:
            product = Product(
                name=form_product.name.data,
                coin=form_product.coin.data,
                count=form_product.count.data,
                info=form_product.info.data
            )
            session.add(product)
            session.commit()
        except Exception as ex:
            abort(404, message=f"Product {ex} not found")
    if form_trainer.validate_on_submit():
        try:
            trainer = Trainer(
                surname=form_trainer.surname.data,
                name=form_trainer.name.data,
                age=form_trainer.age.data,
                email=form_trainer.email.data,
                telefon=form_trainer.telefon.data
            )
            session.add(trainer)
            session.commit()
        except Exception as ex:
            abort(404, message=f"Product {ex} not found")
    if form_categories.validate_on_submit():
        try:
            categories = Categories(
                name=form_categories.name.data,
                products=form_categories.products.data
            )
            session.add(categories)
            session.commit()
        except Exception as ex:
            abort(404, message=f"categories {ex} not found")
    return render_template('adminka.html', title='adminka', form=form, form_product=form_product, message=None,
                           message_2=None, message_3=None, message_4=None, form_trainer=form_trainer,
                           form_categories=form_categories, inform=inform, categorid=categorid,
                           list_product=list_product)


@app.route('/img', methods=['GET', 'POST'])
def img():
    global inform
    form = fileForm()
    if form.validate_on_submit():
        open(form.FILE.data)
    return render_template('img.html', form=form, title='img', inform=inform)


@app.route('/buy/<int:user_id>/<int:product_id>', methods=['GET', 'POST'])
@login_required
def buy(user_id, product_id):
    global inform
    abort_if_user_not_found(user_id)
    abort_if_products_not_found(product_id)
    product = session.query(Product).get(product_id)
    if int(product.count) > 0:
        product.count = str(int(product.count) - 1)
        storiess = Stories(
            user_id=user_id,
            product_id=product_id
        )
        session.add(storiess)
        session.commit()
        return redirect(f'/profile/{user_id}')
    return redirect(f'/profile/{user_id}')


@app.route('/profile/<int:id>', methods=['GET', 'POST'])
@login_required
def prof(id):
    global inform
    abort_if_user_not_found(id)
    categorid = pass_catal()[0]
    list_product = pass_catal()[1]
    id_treners = pass_treners()[0]
    id_li_client = pass_treners()[1]

    user = session.query(User).get(id)
    stor = {}
    for stories in session.query(Stories).filter(Stories.user_id == id):
        stor[stories.id] = [session.query(User).get(stories.user_id), session.query(Product).get(stories.product_id),
                            stories.modified_date]
    lists_bascket = {}
    list_bascket = user.basket.split('|')
    for item in list_bascket:
        for product in session.query(Product).filter(Product.id == int(item)):
            lists_bascket[product.id] = [product.name, product.product_img, product.info, product.coin, product.count]
    return render_template('profile.html', categorid=categorid, lists_bascket=lists_bascket, stor=stor,
                           title='profile', user=user, inform=inform, list_product=list_product,
                           id_treners=id_treners, id_li_client=id_li_client)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    global inform
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password_1.data != form.password_2.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        session = db_session.create_session()
        if session.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            email=form.email.data,
            surname=form.surname.data,
            name=form.name.data,
            address=form.address.data,
            age=form.age.data,
            login=form.login.data
        )
        user.set_password(form.password_1.data)
        session.add(user)
        session.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form, message=None, inform=inform)




@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    return session.query(User).get(user_id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    global inform
    logout_user()
    form = LoginForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        user = session.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect(f"/profile/{user.id}")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form, message=None, inform=inform)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/catalog/<int:id>')
@login_required
def catalog_v(id):
    global inform
    categorid = pass_catal()[0]
    list_product = pass_catal()[1]
    id_treners = pass_treners()[0]
    id_li_client = pass_treners()[1]
    categories = session.query(Categories).get(int(id))
    product_data = {}
    for item in list_product[str(id)]:
        for product in session.query(Product).filter(Product.id == int(item)):
            product_data[product.id] = [product.name, product.product_img, product.info, product.coin, product.count]
    return render_template('catalog_v.html', title=categories.name, categories=categories,
                           product_data=product_data, categorid=categorid,
                           inform=inform, id_treners=id_treners, id_li_client=id_li_client)


@app.route('/catalog/catalog/<int:id_catalog>/in_bascket/<int:id_product>')
@login_required
def buy_product(id_catalog, id_product):
    user = session.query(User).get(current_user.id)
    user.basket += '|' + str(id_product)
    session.commit()
    return redirect(f"/catalog/{id_catalog}")

# @app.route('/add_job/<int:id>', methods=['GET', 'POST'])
# @login_required
# def edit_jobs(id):
#     form = AddjobsForm()
#     if request.method == "GET":
#         session = db_session.create_session()
#         job = session.query(Jobs).filter(Jobs.id == id,
#                                          Jobs.user == current_user).first()
#         if job:
#             job.team_leader = form.id_lead.data
#             job.job = form.job.data
#             job.work_size = form.w_size.data
#             job.collaborators = form.coll.data
#             job.is_finished = form.finished.data
#         else:
#             abort(404)
#     if form.validate_on_submit():
#         session = db_session.create_session()
#         job = session.query(Jobs).filter(Jobs.id == id,
#                                          Jobs.user == current_user).first()
#         if job:
#             job.team_leader = form.id_lead.data
#             job.job = form.job.data
#             job.work_size = form.w_size.data
#             job.collaborators = form.coll.data
#             job.is_finished = form.finished.data
#             session.commit()
#             return redirect('/works')
#         else:
#             abort(404)
#     return render_template('jobs.html', title='Редактирование работ', form=form)


# @app.route('/jobs_delete/<int:id>', methods=['GET', 'POST'])
# @login_required
# def news_delete(id):
#     session = db_session.create_session()
#     job = session.query(Jobs).filter(Jobs.id == id,
#                                      Jobs.user == current_user).first()
#     if job:
#         session.delete(job)
#         session.commit()
#     else:
#         abort(404)
#     return redirect('/works')


@app.route('/')
def start():
    global inform
    categorid = pass_catal()[0]
    list_product = pass_catal()[1]
    id_treners = pass_treners()[0]
    id_li_client = pass_treners()[1]

    return render_template('start.html', title='start', inform=inform, categorid=categorid,
                           list_product=list_product, id_treners=id_treners, id_li_client=id_li_client)


if __name__ == '__main__':
    app.run(port=7000, host='127.0.0.1')
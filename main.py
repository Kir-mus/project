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
token_adminki = 'secret_token0000'


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
            try:
                id_product_list.append(int(prod))
                list_product[str(cate.id)] = id_product_list
            except Exception as er:
                abort(404, message=f"fail prod list {er}")
        id_product_list = []
    return [categorid, list_product]


class InfoForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    start_text = StringField('start_text', validators=[DataRequired()])
    telefon = StringField('telefon', validators=[DataRequired()])
    admin = StringField('admin', validators=[DataRequired()])
    derektor = StringField('derektor', validators=[DataRequired()])
    submit = SubmitField('применить')


class Tokin_chek_Form(FlaskForm):
    tok = StringField('Ввод токена', validators=[DataRequired()])
    chek = SubmitField('применить')


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
    nameprod = StringField('name', validators=[DataRequired()])
    coin = IntegerField('coin', validators=[DataRequired()])
    count = IntegerField('count', validators=[DataRequired()])
    info = StringField('info', validators=[DataRequired()])
    submit = SubmitField('Add product')


class CategoriesForm(FlaskForm):
    namecat = StringField('name', validators=[DataRequired()])
    products = StringField('products_list (пр. заполнения "1, 2, 3, 4")', validators=[DataRequired()])
    submit = SubmitField('Add categories')


class TrainerForm(FlaskForm):
    surname = StringField('surname', validators=[DataRequired()])
    nametren = StringField('name', validators=[DataRequired()])
    age = IntegerField('age', validators=[DataRequired()])
    email = EmailField('email', validators=[DataRequired()])
    telefon = StringField('Телефон', validators=[DataRequired()])
    submit = SubmitField('Add trainer')


class RedprofnameForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    submit = SubmitField('apply')


class RedprofloginForm(FlaskForm):
    login = StringField('login', validators=[DataRequired()])
    submit = SubmitField('apply')


class RedprofsurnameForm(FlaskForm):
    surname = StringField('surname', validators=[DataRequired()])
    submit = SubmitField('apply')


class RedprofageForm(FlaskForm):
    age = IntegerField('age', validators=[DataRequired()])
    submit = SubmitField('apply')


class RedprofemailForm(FlaskForm):
    email = EmailField('email', validators=[DataRequired()])
    submit = SubmitField('apply')


class RedprofaddressForm(FlaskForm):
    address = StringField('address', validators=[DataRequired()])
    submit = SubmitField('apply')


class RedtrenForm(FlaskForm):
    id = IntegerField('id (Тренера)', validators=[DataRequired()])
    nam = StringField('name', validators=[DataRequired()])
    surnam = StringField('surname', validators=[DataRequired()])
    emai = EmailField('email', validators=[DataRequired()])
    ag = IntegerField('age', validators=[DataRequired()])
    telefo = StringField('telefon', validators=[DataRequired()])
    submi = SubmitField('apply')


class DeltrenForm(FlaskForm):
    id_trendelet = StringField('id тренера', validators=[DataRequired()])
    submitt = SubmitField('delete')


class RedprodForm(FlaskForm):
    idd = IntegerField('id (Продукта)', validators=[DataRequired()])
    namep = StringField('name', validators=[DataRequired()])
    infoo = StringField('info', validators=[DataRequired()])
    coins = IntegerField('coin', validators=[DataRequired()])
    counts = IntegerField('count', validators=[DataRequired()])
    submip = SubmitField('apply')


class DelprodForm(FlaskForm):
    idt = StringField('id Продукта', validators=[DataRequired()])
    submidd = SubmitField('delete')


class RedcateForm(FlaskForm):
    idcate = IntegerField('id (Категории)', validators=[DataRequired()])
    namecate = StringField('name', validators=[DataRequired()])
    productcate = StringField('продукт лист(пр. заполнения "1, 2, 3, 4")', validators=[DataRequired()])
    submitred = SubmitField('apply')


class DelcateForm(FlaskForm):
    iddelcate = StringField('id Категории', validators=[DataRequired()])
    submidelcate = SubmitField('delete')


@app.route('/admin1234567', methods=['GET', 'POST'])
def adminka():
    global inform, token_adminki
    categorid = pass_catal()[0]
    list_product = pass_catal()[1]
    id_treners = pass_treners()[0]
    message = None
    message_2 = None
    message_4 = None
    message_3 = None
    message_dop = None
    message_del = None
    message_prod = None
    message_prodel = None
    message_cate = None
    message_delcate = None
    redcate_form = RedcateForm()
    delcate_form = DelcateForm()
    delprod_form = DelprodForm()
    redprod_form = RedprodForm()
    form = InfoForm()
    form_product = ProductForm()
    form_trainer = TrainerForm()
    form_categories = CategoriesForm()
    redtren_form = RedtrenForm()
    deltren_form = DeltrenForm()
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
            if session.query(Product).filter(Product.name == form_product.nameprod.data).first():
                message_2 = f'такой Product уже есть'
            else:
                product = Product(
                    name=form_product.nameprod.data,
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
            if session.query(Trainer).filter(Trainer.email == form_trainer.email.data).first():
                message_3 = f'такой email уже есть'
            else:
                trainer = Trainer(
                    surname=form_trainer.surname.data,
                    name=form_trainer.nametren.data,
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
            for prod in form_categories.products.data.split(', '):
                try:
                    int(prod)
                except Exception as er:
                    abort(404, message=f'error prod_list')
            if session.query(Categories).filter(Categories.name == form_categories.namecat.data).first():
                message_4 = f'такая Categories уже есть'
            else:
                categories = Categories(
                    name=form_categories.namecat.data,
                    products=form_categories.products.data
                )
                session.add(categories)
                session.commit()
        except Exception as ex:
            abort(404, message=f"categories {ex} not found")
    if redtren_form.validate_on_submit():
        try:
            trainers = session.query(Trainer).get(int(redtren_form.id.data))
            if not trainers:
                message_dop = f'Такого id нет'
            elif session.query(Trainer).filter(Trainer.email == redtren_form.emai.data).first() \
                    and trainers.email != redtren_form.emai.data:
                message_dop = f'такой email уже есть'
            else:
                trainers.surname = redtren_form.surnam.data
                trainers.name = redtren_form.nam.data
                trainers.age = redtren_form.ag.data
                trainers.telefon = redtren_form.telefo.data
                trainers.email = redtren_form.emai.data
                session.commit()
        except Exception as ex:
            abort(404, message=f"error {ex} redtren")
    if deltren_form.validate_on_submit():
            trainersdel = session.query(Trainer).get(int(deltren_form.id_trendelet.data))
            if not trainersdel:
                message_del = f'Такого id нет'
            else:
                session.delete(trainersdel)
                session.commit()
    if redprod_form.validate_on_submit():
        try:
            prodct = session.query(Product).get(int(redprod_form.idd.data))
            if not prodct:
                message_prod = f'Такого id нет'
            else:
                if session.query(Product).filter(Product.name == redprod_form.namep.data).first() and \
                        prodct.name != redprod_form.namep.data:
                    message_prod = f'Такогй Product уже есть'
                else:
                    prodct.name = redprod_form.namep.data
                    prodct.info = redprod_form.infoo.data
                    prodct.count = redprod_form.counts.data
                    prodct.coin = redprod_form.coins.data
                    session.commit()
        except Exception as ex:
            abort(404, message=f'error {ex} prodel')
    if delprod_form.validate_on_submit():
        try:
            prodd = session.query(Product).get(int(delprod_form.idt.data))
            if not prodd:
                message_prodel = f'Такого id нет'
            else:
                session.delete(prodd)
                session.commit()
        except Exception as ex:
            abort(404, message=f'error {ex} prodel')

    if redcate_form.validate_on_submit():
        try:
            cate = session.query(Categories).get(int(redcate_form.idcate.data))
            if not cate:
                message_cate = f'Такого id нет'
            else:
                if session.query(Categories).filter(Categories.name == redcate_form.namecate.data).first() and \
                        cate.name != redcate_form.namecate.data:
                    message_cate = f'Такая категория уже есть'
                else:

                            cate.name = redcate_form.namecate.data
                            cate.products = redcate_form.productcate.data
                            session.commit()

        except Exception as ex:
            abort(404, message=f'error {ex} prodel')
    if delcate_form.validate_on_submit():
        try:
            dcate = session.query(Categories).get(int(delcate_form.iddelcate.data))
            if not dcate:
                message_delcate = f'Такого id нет'
            else:
                session.delete(dcate)
                session.commit()
        except Exception as ex:
            abort(404, message=f'error {ex} prodel')
    return render_template('adminka.html', title='adminka', form=form, form_product=form_product, message=message,
                           message_2=message_2, message_3=message_3, message_4=message_4, form_trainer=form_trainer,
                           form_categories=form_categories, inform=inform, categorid=categorid,
                           list_product=list_product, message_dop=message_dop, redtren_form=redtren_form,
                           message_del=message_del, deltren_form=deltren_form, delprod_form=delprod_form,
                           redprod_form=redprod_form, message_prod=message_prod, message_prodel=message_prodel,
                           message_cate=message_cate, message_delcate=message_delcate, redcate_form=redcate_form,
                           delcate_form=delcate_form, id_treners=id_treners)


@app.route('/img', methods=['GET', 'POST'])
def img():
    global inform
    form = fileForm()
    if form.validate_on_submit():
        open(form.FILE.data)
    return render_template('img.html', form=form, title='img', inform=inform)


@app.route('/buy/<int:user_id>/<int:product_id>/delete', methods=['GET', 'POST'])
@login_required
def del_prod(user_id, product_id):
    global inform
    abort_if_user_not_found(user_id)
    abort_if_products_not_found(product_id)
    user = session.query(User).get(user_id)
    li = user.basket.split('|')
    if str(product_id) in li:
        li.remove(str(product_id))
    user.basket = '|'.join(li)
    session.commit()
    return redirect(f'/profile/{user_id}')


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
    tokin_chek_form = Tokin_chek_Form()
    redprofnameform = RedprofnameForm()
    redprofloginform = RedprofloginForm()
    redprofsurnameform = RedprofsurnameForm()
    redprofageform = RedprofageForm()
    redprofemailform = RedprofemailForm()
    redprofaddressform = RedprofaddressForm()
    abort_if_user_not_found(current_user.id)
    user = session.query(User).get(current_user.id)
    message = None
    if tokin_chek_form.validate_on_submit():

            if tokin_chek_form.tok.data == token_adminki:
                user = session.query(Trainer).get(int(current_user.id))
                user.admin_chek = 'True'
                session.commit()
            else:
                pass
    if redprofnameform.validate_on_submit():
        try:
            user.name = redprofnameform.name.data
            session.commit()
        except Exception as er:
            abort(404, message=f"User {er} error redprof")

    if redprofloginform.validate_on_submit():
        try:
            if session.query(User).filter(User.login == redprofloginform.login.data).first():
                message = f'такой login уже есть'
            else:
                user.login = redprofloginform.login.data
                session.commit()
        except Exception as er:
            abort(404, message=f"User {er} error redprof")

    if redprofsurnameform.validate_on_submit():
        try:
            user.surname = redprofsurnameform.surname.data
            session.commit()
        except Exception as er:
            abort(404, message=f"User {er} error redprof")
    if redprofageform.validate_on_submit():
        try:
            user.age = redprofageform.age.data
            session.commit()
        except Exception as er:
            abort(404, message=f"User {er} error redprof")
    if redprofemailform.validate_on_submit():
        try:
            if session.query(User).filter(User.email == redprofemailform.email.data).first():
                message = f'такой email уже есть'
            else:
                user.email = redprofemailform.email.data
                session.commit()
        except Exception as er:
            abort(404, message=f"User {er} error redprof")
    if redprofaddressform.validate_on_submit():
        try:
            user.address = redprofaddressform.address.data
            session.commit()
        except Exception as er:
            abort(404, message=f"User {er} error redprof")

    categorid = pass_catal()[0]
    list_product = pass_catal()[1]
    id_treners = pass_treners()[0]
    id_li_client = pass_treners()[1]
    stor = {}
    for stories in session.query(Stories).filter(Stories.user_id == id):
        stor[stories.id] = [session.query(User).get(stories.user_id), session.query(Product).get(stories.product_id),
                            stories.modified_date]
    lists_bascket = {}
    list_bascket = user.basket.split('|')
    print(list_bascket)
    for item in list_bascket:
        for product in session.query(Product).filter(Product.id == int(item)):
            lists_bascket[product.id] = [product.name, product.product_img, product.info, product.coin, product.count]
    return render_template('profile.html', categorid=categorid, lists_bascket=lists_bascket, stor=stor,
                           title='profile', user=user, inform=inform, list_product=list_product,
                           id_treners=id_treners, id_li_client=id_li_client, redprofnameform=redprofnameform,
                           redprofloginform=redprofloginform, redprofsurnameform=redprofsurnameform,
                           redprofageform=redprofageform, redprofemailform=redprofemailform,
                           redprofaddressform=redprofaddressform, message=message, tokin_chek_form=tokin_chek_form)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    global inform
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password_1.data != form.password_2.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают", inform=inform)
        session = db_session.create_session()
        if session.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такая почта уже есть", inform=inform)
        if session.query(User).filter(User.login == form.login.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой login уже есть", inform=inform)
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
        else:
            return render_template('login.html',
                                   message="Неправильный логин или пароль",
                                   form=form, inform=inform)
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
    print(list_product)
    for item in list_product[str(id)]:
        for product in session.query(Product).filter(Product.id == int(item)):
            product_data[product.id] = [product.name, product.product_img, product.info, product.coin, product.count]
    print(product_data)
    return render_template('catalog_v.html', title=categories.name, categories=categories,
                           product_data=product_data, categorid=categorid,
                           inform=inform, id_treners=id_treners, id_li_client=id_li_client)


@app.route('/catalog/<int:id_catalog>/in_bascket/<int:id_product>')
@login_required
def buy_product(id_catalog, id_product):
    user = session.query(User).get(current_user.id)
    print('user', user.id)
    if str(id_product) in user.basket.split('|'):
        print('s', id_product, user.basket.split('|'), current_user.id)
        pass
    else:
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

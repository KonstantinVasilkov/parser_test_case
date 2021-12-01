import os
from datetime import datetime

from flask import Flask, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from forms import CompanyMainInfoForm

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(os.path.join(BASE_DIR, 'output'), 'reestr_nostroy.db')
CONNECTION_STRING = f'sqlite:///{DB_PATH}'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = CONNECTION_STRING
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['CSRF_ENABLED'] = True
app.config['SECRET_KEY'] = 'My_Super_puper_secret_string'

db = SQLAlchemy(app)
db.Model.metadata.reflect(db.engine)


class Reestr(db.Model):
    __table__ = db.Model.metadata.tables['reestr']

    def __init__(self, company_inn, sro_reg_number, sro_status,
                 comments, company_short_name):
        self.company_inn = company_inn
        self.sro_reg_number = sro_reg_number
        self.sro_status = sro_status
        self.comments = comments
        self.company_short_name = company_short_name


class RegistrationDates(db.Model):
    __table__ = db.Model.metadata.tables['registration_dates']

    def __init__(self, sro_start_date, sro_end_date):
        self.sro_start_date = sro_start_date
        self.sro_end_date = sro_end_date


class Rights(db.Model):
    __table__ = db.Model.metadata.tables['rights']


class Certificates(db.Model):
    __table__ = db.Model.metadata.tables['certificates']


def get_full_card(uid):
    full_card = Reestr.query.join(
        RegistrationDates).join(Rights).join(Certificates).add_columns(
        Reestr.uid,
        Reestr.short_name_of_sro_member,
        Reestr.full_name_of_sro_member,
        Reestr.inn,
        Reestr.ogrn,
        Reestr.status,
        Reestr.comments,
        Reestr.organization_type,
        Reestr.sro_registration_number,
        RegistrationDates.start_date,
        RegistrationDates.end_date,
        Certificates.certificate_number,
        Certificates.certificate_issued_date,
        Certificates.max_price_per_one_contract,
        Certificates.certificate_status).filter_by(uid=uid).all()
    return full_card


def get_main_info(uid):
    main_info_card = Reestr.query.join(
        RegistrationDates).add_columns(
        Reestr.uid,
        Reestr.short_name_of_sro_member,
        Reestr.inn,
        Reestr.ogrn,
        Reestr.status,
        Reestr.comments,
        Reestr.organization_type,
        Reestr.sro_registration_number,
        RegistrationDates.start_date,
        RegistrationDates.end_date, ).filter_by(uid=uid).all()
    return main_info_card


@app.template_filter('dt')
def _jinja2_filter_datetime(date, frm='%d-%m-%Y'):
    return date.strftime(frm)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/', methods=['GET', 'POST'])
@app.route('/<int:page>', methods=['GET', 'POST'])
def index(page=1):
    if request.method == "POST":
        inn = request.form.get('inn')
        organizations = Reestr.query.filter_by(
            inn=inn).paginate(page, 10, False)

        return render_template('index.html', organizations=organizations)

    organizations = Reestr.query.paginate(page, 10, False)
    return render_template('index.html', organizations=organizations)


@app.route('/details/<uid>')
def details(uid):
    full_card_of_organization = get_full_card(uid)
    return render_template('organization_detail.html',
                           card=full_card_of_organization)


@app.route('/modify/<int:uid>', methods=['POST', 'GET'])
def modify_main_info(uid):
    def convert_date(text):
        if text:
            text = text.strip()
            return datetime.strptime(text, '%Y-%m-%d')
        return None

    if request.method == 'GET':
        main_info_card = get_main_info(uid)
        form = CompanyMainInfoForm()
        form.company_short_name.data = main_info_card[
            0].short_name_of_sro_member
        form.company_inn.data = main_info_card[0].inn
        form.sro_reg_number.data = main_info_card[0].sro_registration_number
        form.sro_start_date.data = main_info_card[0].start_date
        form.sro_end_date.data = main_info_card[0].end_date
        form.sro_status.data = main_info_card[0].status
        form.comments.data = main_info_card[0].comments
        return render_template('edit_main_info.html',
                               card=main_info_card,
                               form=form)
    if request.method == 'POST':
        main_info_card = get_main_info(uid)
        reestr = Reestr.query.filter_by(uid=uid).all()
        reestr[0].short_name_of_sro_member = request.form.get(
            'company_short_name')
        reestr[0].inn = request.form.get('company_inn')
        reestr[0].sro_registration_number = request.form.get('sro_reg_number')
        reestr[0].status = request.form.get('sro_status')
        reestr[0].comments = request.form.get('comments')

        registration_dates = RegistrationDates.query.filter_by(uid=uid).all()
        registration_dates[0].start_date = convert_date(
            request.form.get('sro_start_date')
        )
        registration_dates[0].end_date = convert_date(
            request.form.get('sro_end_date')
        )

        form = CompanyMainInfoForm()
        if form.validate_on_submit():
            db.session.commit()
            return redirect(url_for('details', uid=uid))
        return render_template('edit_main_info.html',
                               card=main_info_card,
                               form=form)


@app.route('/delete/<int:uid>', methods=['POST'])
def delete(uid):
    if request.method == 'POST':
        company_record = Reestr.query.filter(Reestr.uid == uid).first()
        db.session.delete(company_record)
        db.session.commit()
    organizations = Reestr.query.paginate(1, 10, False)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)

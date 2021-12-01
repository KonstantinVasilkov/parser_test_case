from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from scrapy.utils.project import get_project_settings

app = Flask(__name__)
settings = get_project_settings()
app.config['SQLALCHEMY_DATABASE_URI'] = settings.get('CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['CSRF_ENABLED'] = True
app.config['SECRET_KEY'] = 'My_Super_puper_secret_string'

db = SQLAlchemy(app)
db.Model.metadata.reflect(db.engine)


class Reestr(db.Model):
    __table__ = db.Model.metadata.tables['reestr']

    def __repr__(self):
        return self.short_name_of_sro_member


class RegistrationDates(db.Model):
    __table__ = db.Model.metadata.tables['registration_dates']


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
        Reestr.organization_type,
        Reestr.sro_registration_number,
        RegistrationDates.start_date,
        RegistrationDates.end_date,
        Certificates.certificate_number,
        Certificates.certificate_issued_date,
        Certificates.max_price_per_one_contract,
        Certificates.certificate_status).filter_by(uid=uid).all()
    return full_card


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

#
# @app.route('/modify/<int:uid>', methods=['POST', 'GET'])
# def modify_main_info(uid):
#     if request.method == 'GET':
#
#     if request.method == 'POST':
#         form = request.form
#     return
#



if __name__ == '__main__':
    app.run(debug=True)

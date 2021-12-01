from flask_wtf import FlaskForm
from wtforms import (BooleanField, DateField, StringField, SubmitField,
                     TextAreaField)
from wtforms.validators import InputRequired


class CompanyMainInfoForm(FlaskForm):
    company_short_name = StringField('Название организации: ',
                                     validators=[InputRequired('not valid 1')])
    company_inn = StringField('ИНН организации: ',
                              validators=[InputRequired('not valid 2')])
    sro_reg_number = StringField('Регистрационный номер в СРО: ')
    sro_start_date = DateField('Дата регистрации в СРО: ')
    sro_end_date = DateField('Дата исключения из в СРО: ')
    sro_status = StringField('Статус членства в СРО: ')
    comments = TextAreaField('Комментарии:')

from scrapy.utils.project import get_project_settings
from sqlalchemy import (Column, DateTime, ForeignKey, Integer, Text,
                        create_engine)
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


def db_connect():
    return create_engine(get_project_settings().get('CONNECTION_STRING'))


def create_table(engine):
    Base.metadata.create_all(engine)


class Reestr(Base):
    __tablename__ = 'reestr'

    uid = Column('uid', Integer(), unique=True, primary_key=True)
    full_name_of_sro_member = Column('full_name_of_sro_member', Text())
    short_name_of_sro_member = Column('short_name_of_sro_member', Text())
    inn = Column('inn', Text())
    ogrn = Column('ogrn', Text())
    status = Column('status', Text())
    organization_type = Column('organization_type', Text())
    sro_registration_number = Column('sro_registration_number', Text())


class RegistrationDates(Base):
    __tablename__ = 'registration_dates'

    id = Column(Integer, primary_key=True)
    uid = Column(Integer, ForeignKey('reestr.uid'))
    start_date = Column('start_date', DateTime)
    end_date = Column('end_date', DateTime, nullable=True)


class Rights(Base):
    __tablename__ = 'rights'

    id = Column(Integer, primary_key=True)
    uid = Column(Integer, ForeignKey('reestr.uid'))
    max_price_per_one_contract = Column('max_price_per_one_contract', Text())
    size_of_obligations = Column('size_of_obligations', Text())
    date_of_suspension = Column('date_of_suspension', DateTime)
    status_of_suspension = Column('status_of_suspension', Text())


class Certificates(Base):
    __tablename__ = 'certificates'

    id = Column(Integer, primary_key=True)
    uid = Column(Integer, ForeignKey('reestr.uid'))
    certificate_number = Column('certificate_number', Text())
    certificate_issued_date = Column('certificate_issued_date', DateTime)
    max_price_per_one_contract = Column('max_price_per_one_contract', Text())
    certificate_status = Column('certificate_status', Text())

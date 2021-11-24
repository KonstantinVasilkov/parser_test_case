from sqlalchemy.orm import sessionmaker

from .items import (CertificatesItem, ReestrNostroyItem, RegistrationDatesItem,
                    RightsItem)
from .models import (Certificates, Reestr, RegistrationDates, Rights,
                     create_table, db_connect)


class SaveReestrPipeline(object):
    def __init__(self):
        engine = db_connect()
        create_table(engine)
        self.Session = sessionmaker(bind=engine)

    def process_item(self, item, spider):
        if isinstance(item, ReestrNostroyItem):
            return self.handle_reestr_item(item, spider)
        if isinstance(item, RegistrationDatesItem):
            return self.handle_registration_date_item(item, spider)
        if isinstance(item, RightsItem):
            return self.handle_rights_item(item, spider)
        if isinstance(item, CertificatesItem):
            return self.handle_certificate_item(item, spider)

    def handle_reestr_item(self, item, spider):
        session = self.Session()
        reestr = Reestr()
        reestr.full_name_of_sro_member = item['full_name_of_sro_member']
        reestr.short_name_of_sro_member = item['short_name_of_sro_member']
        reestr.inn = item['inn']
        reestr.ogrn = item['ogrn']
        reestr.status = item['status']
        reestr.organization_type = item['organization_type']
        reestr.sro_registration_number = item['sro_registration_number']
        reestr.uid = item['uid']

        try:
            session.add(reestr)
            session.commit()

        except:
            session.rollback()
            raise

        finally:
            session.close()

        return item

    def handle_registration_date_item(self, item, spider):
        session = self.Session()
        registration_dates = RegistrationDates()
        registration_dates.start_date = item.get('start_date')
        registration_dates.end_date = item.get('end_date')
        registration_dates.uid = item['uid']

        try:
            session.add(registration_dates)
            session.commit()

        except:
            session.rollback()
            raise

        finally:
            session.close()

        return item

    def handle_rights_item(self, item, spider):
        session = self.Session()
        rights = Rights()
        rights.max_price_per_one_contract = item.get(
            'max_price_per_one_contract'
        )
        rights.size_of_obligations = item.get('size_of_obligations')
        rights.date_of_suspension = item.get('date_of_suspension')
        rights.status_of_suspension = item.get('status_of_suspension')
        rights.uid = item['uid']

        try:
            session.add(rights)
            session.commit()

        except:
            session.rollback()
            raise

        finally:
            session.close()

        return item

    def handle_certificate_item(self, item, spider):
        session = self.Session()
        certificates = Certificates()
        certificates.certificate_number = item.get(
            'certificate_number'
        )
        certificates.certificate_issued_date = item.get(
            'certificate_issued_date'
        )
        certificates.max_price_per_one_contract = item.get(
            'max_price_per_one_contract'
        )
        certificates.certificate_status = item.get('certificate_status')
        certificates.uid = item['uid']

        try:
            session.add(certificates)
            session.commit()

        except:
            session.rollback()
            raise

        finally:
            session.close()

        return item

import re
from datetime import datetime

from itemloaders.processors import Compose, MapCompose, TakeFirst
from scrapy.item import Field, Item


def remove_service_characters(list_of_all_characters):
    text = ' '.join(map(str.strip, list_of_all_characters))
    text = re.sub('\\t|\\n|\\r|&downarrow;|№|#|\\"|\'', '', text)
    return text


def create_uid(text):
    uid = []
    for element in text[0].split('/'):
        if element.isnumeric():
            uid.append(element)
    return int(''.join(uid))


def convert_date(text):
    text = text.strip()
    return datetime.strptime(text, '%d.%m.%Y')


class ReestrNostroyItem(Item):
    full_name_of_sro_member = Field(
        input_processor=Compose(remove_service_characters),
        output_processor=TakeFirst(),
    )
    short_name_of_sro_member = Field(
        input_processor=Compose(remove_service_characters),
        output_processor=TakeFirst(),
    )
    inn = Field(
        output_processor=TakeFirst(),
    )
    ogrn = Field(
        output_processor=TakeFirst(),
    )
    status = Field(
        input_processor=Compose(remove_service_characters),
        output_processor=TakeFirst(),
    )
    organization_type = Field(
        output_processor=TakeFirst(),
    )
    sro_registration_number = Field(
        input_processor=Compose(remove_service_characters),
        output_processor=TakeFirst(),
    )
    uid = Field(
        input_processor=Compose(create_uid),
        output_processor=TakeFirst(),
    )


class RegistrationDatesItem(Item):
    start_date = Field(
        input_processor=MapCompose(convert_date),
        output_processor=TakeFirst()
    )
    end_date = Field(
        input_processor=MapCompose(convert_date),
        output_processor=TakeFirst()
    )
    uid = Field(
        output_processor=TakeFirst(),
    )


class RightsItem(Item):
    uid = Field(
        output_processor=TakeFirst(),
    )
    max_price_per_one_contract = Field(
        input_processor=Compose(remove_service_characters),
        output_processor=TakeFirst(),
    )
    size_of_obligations = Field(
        input_processor=Compose(remove_service_characters),
        output_processor=TakeFirst(),
    )
    date_of_suspension = Field(
        input_processor=MapCompose(convert_date),
        output_processor=TakeFirst(),
    )
    status_of_suspension = Field(
        input_processor=Compose(remove_service_characters),
        output_processor=TakeFirst(),
    )


class CertificatesItem(Item):
    uid = Field(
        output_processor=TakeFirst(),
    )
    certificate_number = Field(
        input_processor=Compose(remove_service_characters),
        output_processor=TakeFirst(),
    )
    certificate_issued_date = Field(
        input_processor=MapCompose(convert_date),
        output_processor=TakeFirst(),
    )
    max_price_per_one_contract = Field(
        input_processor=Compose(remove_service_characters),
        output_processor=TakeFirst(),
    )
    certificate_status = Field(
        input_processor=Compose(remove_service_characters),
        output_processor=TakeFirst(),
    )

import os

import scrapy
from scrapy.loader import ItemLoader
from scrapy.utils.project import get_project_settings

from reestr_nostroy.items import (CertificatesItem, ReestrNostroyItem,
                                  RegistrationDatesItem, RightsItem)


def get_list_of_inns():
    settings = get_project_settings()
    input_file = os.path.join(settings.get('BASE_DIR'), 'inns.txt')
    with open(input_file, 'r') as file:
        incoming_inns = file.read().splitlines()
    return incoming_inns


class ReestrSpider(scrapy.Spider):
    name = 'reestr_nostroy'
    allowed_domains = [
        'reestr.nostroy.ru'
    ]
    inns = get_list_of_inns()
    # inns = ['2308111839']
    start_urls = [
        f'https://reestr.nostroy.ru/reestr?m.inn={inns[0]}',
    ]

    def parse(self, response, **kwargs):

        for row in response.xpath(
                '//*[@class="items table table-selectable-row '
                'table-striped"]//tbody//tr'
        ):
            loader = ItemLoader(item=ReestrNostroyItem(), selector=row)
            loader.add_xpath('full_name_of_sro_member', 'td[1]//text()')
            loader.add_xpath('short_name_of_sro_member', 'td[2]//text()')
            loader.add_xpath('inn', 'td[3]//text()')
            loader.add_xpath('ogrn', 'td[4]//text()')
            loader.add_xpath('status', 'td[5]//text()')
            loader.add_xpath('organization_type', 'td[6]//text()')
            loader.add_xpath('sro_registration_number', 'td[7]//text()')
            loader.add_value('uid', row.attrib['rel'])
            details_url = row.attrib['rel']

            yield loader.load_item()
            yield response.follow(
                details_url,
                self.parse_details,
                meta={'uid': loader.get_collected_values('uid')}
            )

        for inn in self.inns[1:]:
            next_page = f'https://reestr.nostroy.ru/reestr?m.inn={inn}'
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)

    def parse_details(self, response):
        loader = ItemLoader(item=RegistrationDatesItem(),
                            selector=response.xpath('//*[@class="items '
                                                    'table"]//tbody'))
        loader.add_xpath(
            'start_date',
            'tr[8]//td//text()'
        )
        loader.add_xpath(
            'end_date',
            'tr[9]//td//text()'
        )
        loader.add_value('uid', response.meta['uid'])
        yield loader.load_item()

        rights_page = response.url + '/rights'
        certificates_page = response.url + '/certificates'
        yield scrapy.Request(
            rights_page,
            callback=self.parse_rights,
            meta={'uid': loader.get_collected_values('uid')}
        )
        yield scrapy.Request(
            certificates_page,
            callback=self.parse_certificates,
            meta={'uid': loader.get_collected_values('uid')}
        )

    def parse_rights(self, response):
        loader = ItemLoader(item=RightsItem(),
                            selector=response.xpath('//*[@id="filter_form"]'))
        loader.add_xpath('max_price_per_one_contract',
                         '//*[@class="table table-bordered"]//tbody//'
                         'tr[4]//td[2]//text()')
        loader.add_xpath('size_of_obligations',
                         '//*[@class="table table-bordered"]//tbody//'
                         'tr[5]//td[2]//text()')
        loader.add_xpath('date_of_suspension',
                         '//*[@class="table"]//tr[1]//td[1]//text()')
        loader.add_xpath(
            'status_of_suspension',
            '//*[@class="table"]//tr[1]//td[2]//text()')

        loader.add_value('uid', response.meta['uid'])

        yield loader.load_item()

    def parse_certificates(self, response):
        selector = response.xpath('//*[@class="items table"]//tbody//tr')
        table = response.xpath(
            '//*[@id="filter_form"]//table//tbody//tr//td//text()'
        ).getall()[54:]
        clear_table = []
        for element in table:
            if element.strip():
                clear_table.append(element.strip())
        counter = 0
        while counter < len(clear_table):
            bach = clear_table[counter:counter+7]
            loader = ItemLoader(item=CertificatesItem(), selector=selector)
            loader.add_value('certificate_number', bach[1])
            loader.add_value('certificate_issued_date', bach[2])
            loader.add_value('uid', response.meta['uid'])
            if clear_table[counter+5] == 'Загрузка...':
                loader.add_value('max_price_per_one_contract', None)
                loader.add_value('certificate_status', bach[4])
                counter += 7
                yield loader.load_item()
            else:
                loader.add_value('max_price_per_one_contract', bach[4])
                loader.add_value('certificate_status', bach[5])
                counter += 8
                yield loader.load_item()

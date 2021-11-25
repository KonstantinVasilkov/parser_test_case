from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from utils import results_to_csv

from reestr_nostroy.spiders.reestr_spyder import ReestrSpider

if __name__ == '__main__':
    process = CrawlerProcess(settings=get_project_settings())
    process.crawl(ReestrSpider)
    process.start()

    results_to_csv()

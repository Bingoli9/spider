# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from DajieCrawl.items import DajieWorkListItem
from scrapy.http import Request, FormRequest

class DajieSpider(CrawlSpider):
    name = 'DajieSpider'
    allowed_domains = ['job.dajie.com']
    start_urls = ['https://job.dajie.com/e018b595-2e5a-44e6-bf9d-dca5dc260bc5.html?jobsearch=0&pagereferer=blank&keyword=%E5%90%8E%E7%AB%AF%E5%BC%80%E5%8F%91&clicktype=job']

    def parse_work_list(self,response):
        text_top = response.xpath(".//*[@id='jp-app-wrap']/div[2]/div[2]/div[1]/div[1]").extract_first()
        workName = text_top.xpath("./div/span[1]/text()").extract_first()
        workSalary = text_top.xpath("./span[1]/text()").extract_first()
                   
        workDescription = response.xpath(".//*[@id='jp_maskit']/pre[2]/text()").extract_first()

        workCompany = response.xpath(".//*[@id='jp-app-wrap']/div[2]/div[2]/div[3]/dl/a/dd/p[2]/span/text()").extract_first()

        workListItem = DajieWorkListItem(workName=workName, workSalary=workSalary, 
            workDescription=workDescription, workCompany=workCompany)
        yield workListItem

        similary_urls = response.xpath(".//*[@id='panel_id_0']/ul/li/a/@href")
        for url in similary_urls:
            url = "https:" + url
            yield Request(response.urljoin(url=url),
                callback=self.parse_work_list,
                errback=self.parse_err)

        suggest_urls = response.xpath(".//*[@id='panel_id_1']/ul/li/a/@href")
        for url in suggest_urls:
            url = "https:" + url
            yield Request(response.urljoin(url=url), 
                callback=self.parse_work_list,
                errback=self.parse_err)

        nearby_urls = response.xpath(".//*[@id='panel_id_1']/ul/li/a/@href")
        for url in nearby_urls:
            url = "https:" + url
            yield Request(response.urljoin(url=url), 
                callback=self.parse_work_list,
                errback=self.parse_err)

     def parse_err(self,response):
        self.logger.error('crawl %s fail'%response.url)

if __name__=='__main__':
	process = CrawlerProcess(get_project_settings())
	process.crawl('DajieCrawler')
	process.start()
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.spider import BaseSpider
from fbnames.items import FbnamesItem
from scrapy.contrib.linkextractors import LinkExtractor

class MySpider(CrawlSpider):
    name = "fb"
    allowed_domains = ["uphail.com"]
    start_urls = ["http://www.uphail.com"]

    # rules = (Rule (LxmlLinkExtractor(allow=(r"",) deny=())
    # , callback="parseo", follow= False),
    # )

    rules = (

        Rule(
            LinkExtractor(allow=('',),

                          deny=('vt/',
                          ),
            ),
            callback='parse_item',
            follow=True
        ),

    )

    def parse_item(self, response):
        hxs = HtmlXPathSelector(response)
        urls = hxs.xpath('//a')
        items = []
        for url in urls:
            item = FbnamesItem()
            item["anchor"] = url.xpath("text()").extract()
            item["link"] = url.xpath("@href").extract()
            items.append(item)
        return items


        #crawls
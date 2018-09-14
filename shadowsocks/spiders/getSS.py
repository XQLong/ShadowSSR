import scrapy
from scrapy import Request
from scrapy.loader import ItemLoader

from shadowsocks.items import ShadowsocksItem


class getSSSpider(scrapy.Spider):

    name = 'getSS'
    allowed_domains = ["doub.io"]
    base_url = "https://www.microsofttranslator.com/bv.aspx?from=&to=cn&a=https://doub.io/sszhfx/"

    def start_requests(self):
        url = self.base_url
        yield Request(url=url, callback=self.parse,dont_filter=True)

    def parse(self, response):
        ssURL = response.xpath("//tbody/tr/td/a[contains(@class,'dl1')]/@href").extract()
        print(len(ssURL))
        if len(ssURL)>0:
            with open('SSR.txt', 'w') as f:
                f.write('')
            for getSS in ssURL:
                yield Request(url=getSS, callback=self.parse_geturl,dont_filter=True)
                print(ssURL)

    def parse_geturl(self,response):
        ssURL = response.xpath("//body/p/a/text()").extract()
        ss = ItemLoader(item=ShadowsocksItem(), response=response)
        if 'ss' in ssURL[0]:
            ss.add_value('ssURL',ssURL[0])
            print(ssURL[0])
        return ss.load_item()

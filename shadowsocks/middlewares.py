# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html
import random
import time

from scrapy import signals
from scrapy.http import HtmlResponse
from selenium import webdriver

from shadowsocks.settings import USER_AGENT_LIST


class JsPageSpiderMiddleware(object):
    def __init__(self):
        option = webdriver.ChromeOptions()
        #proxyaddress = "--proxy-server="+self.get_random_proxy()
        #print(proxyaddress)
        #option.add_argument(proxyaddress)
        option.add_argument('--headless')
        prefs = {"profile.managed_default_content_settings.images": 2}
        # 不加载图片
        option.add_experimental_option("prefs", prefs)
        self.browser = webdriver.Chrome(executable_path="E:\machine_learning\chromedriver.exe",chrome_options=option)
        super(JsPageSpiderMiddleware, self).__init__()

    def process_request(self,request,spider):
        if spider.name == "getSS":
            browser = self.browser
            browser.get(request.url)
            browser.implicitly_wait(10)
            #time.sleep(1)
            try:
                browser.switch_to.frame("frmTgt")
            except:
                print("have no frame contentFrame")
                # os.system("python E:\machine_learning\workplace\getUserInfo\getUserInfo\proxies.py")
            return HtmlResponse(url=browser.current_url, body=browser.page_source, encoding="utf-8")

    def process_response(self,request, response, spider):
        browser = self.browser
        sta1 = response.xpath("//div[contains(@class,'error-code')]")
        # print(len(sta1))
        if len(sta1)>0:
            print('proxy wrong change proxy')
            browser.delete_all_cookies()
            browser.close()
            browser.quit()
            # os.system("python E:\machine_learning\workplace\FreeSahdowSocks\Feess\proxies.py")
            self.__init__()
            return request
        else:
            return response

    def process_exception(self,request, exception, spider):
        print('exception exception'+str(exception))
        try:
            browser = self.browser
            browser.close()
            browser.delete_all_cookies()
            browser.quit()
            # os.system("python E:\machine_learning\workplace\FreeSahdowSocks\Freess\proxies.py")
        except:
            print("浏览器...")
        self.__init__()
        return request

    def get_random_proxy(self):
        '''随机从文件中读取proxy'''
        while 1:
            with open('E:\machine_learning\workplace\FreeSahdowSocks\Freess\proxies.txt', 'r') as f:
                proxies = f.readlines()
            if proxies:
                break
            else:
                time.sleep(1)
        proxy = random.choice(proxies).strip()
        return proxy

    def get_random_user_agent(self):
        ua = random.choice(USER_AGENT_LIST)
        if ua:
            return ua

class ShadowsocksSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class ShadowsocksDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)

import re
from scrapy import Spider, Request, log, FormRequest
from fbnames.items import FbnamesItem
from scrapy.exceptions import CloseSpider
from redis import StrictRedis

import requests
from StringIO import StringIO
import lxml.html as lx
from urlparse import urljoin

from scripts.aws import start_instances, stop_instance_by_ip

class FacebookSpider(Spider):
  name = 'fb_spider'
  allowed_domains = ["facebook.com"]
  count = 0
  start_urls = ["https://www.facebook.com/directory/people"]
  redis = StrictRedis()

  directory_links_regex = r'.*/directory/people.*'
  people_links_regex = r'.*\.facebook\.com/[a-zA-Z0-9\.]+$'

  # proxy_ips = [
  #   'https://54.172.41.190',
  #   'https://54.174.135.141',
  #   'https://54.175.43.166',
  # ]

  def remove_proxy(self, ip):
    # remove the proxy from the list;
    # terminate proxy;
    # fire up a new proxy
    redis.lrem('plist', 0, ip)
    stop_instance_by_ip(ip)
    start_instances(1)

  def start_requests(self):
    r = Request(
      url='https://www.facebook.com/directory/people',
    )
    return [r]

  def parse(self, response):
    lh = lx.fromstring(response.body)

    # handle potential Captchas here
    if 'Security Check' in response.body:
      # resubmit request & stop processing
      print '>>> hit a security check... removing proxy'
      proxy = response.request.meta.get('proxy')
      if proxy:
        self.remove_proxy(proxy)
      yield response.request
      return

    ###########################

    links = lh.xpath('//a')
    for l in links:
      href = l.attrib.get('href')
      if href:
        absolute_href = urljoin(response.url, href)
        if re.match(self.directory_links_regex, absolute_href):
          self.count += 1
          request = Request(absolute_href, callback=self.parse, meta={'count': self.count})
          yield request
        elif re.match(self.people_links_regex, href):
          item = FbnamesItem()
          item['anchor'] = l.text_content().strip()
          item['link'] = absolute_href
          yield item
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
  count = 0

  directory_links_regex = r'.*/directory/people.*'
  people_links_regex = r'.*\.facebook\.com/[a-zA-Z0-9\.]+$'

  def __init__(self, debug=None, remote=False, *args, **kwargs):
    if debug:
      print 'debug mode on'
      self.allowed_domains = ["localhost:5000"]
      self.start_urls = ["http://localhost:5000/directory/people"]
    else:
      self.allowed_domains = ["facebook.com"]
      self.start_urls = ["https://www.facebook.com/directory/people"]

    if remote:
      self.redis = StrictRedis('54.172.41.190')
    else:
      self.redis = StrictRedis()

  def remove_proxy(self, ip):
    # remove the proxy from the list;
    # terminate proxy;
    # fire up a new proxy
    res = self.redis.lrem('plist', 0, ip)
    if res > 0:
      # only start a new instance if the remove actually worked
      print 'removing proxy', ip
      stop_instance_by_ip(ip)
      print 'starting new proxy...'
      start_instances(1)

  def start_requests(self):
    r = Request(
      url='https://www.facebook.com/directory/people',
      meta={'count': 0}
    )
    return [r]

  def parse(self, response):
    lh = lx.fromstring(response.body)

    # handle potential Captchas here
    if 'Security Check' in response.body:
      # resubmit request & stop processing
      print 'hit a security check...'
      proxy = response.request.meta.get('proxy')
      if proxy:
        print 'attemping to remove proxy', proxy
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
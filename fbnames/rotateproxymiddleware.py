from scripts.aws import start_instances, stop_instances

class RotateProxyMiddleware(object):
  def process_request(self, request, spider):
    proxy = self._get_next_proxy(spider)
    request.meta['proxy'] = proxy

  def _get_next_proxy(self, spider):
    redis = spider.redis
    size = redis.llen('plist')
    if size == 0:
      print 'no available proxies.'
      print 'firing up 3 new AWS instances...'
      i = start_instances(3)
      q, next_proxy = redis.blpop('plist') # wait until one is online
      # immediately push it back onto the list
      redis.rpush('plist', next_proxy)
    else:
      index = spider.state['count'] % size
      next_proxy = redis.lindex('plist', index)
    proxy = "https://%s:6969" % next_proxy
    return proxy
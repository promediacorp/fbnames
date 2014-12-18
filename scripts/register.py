from urllib import urlopen
from redis import StrictRedis

# connect to redis
r = StrictRedis(host='54.172.41.190')

# get my ip
u = urlopen('http://ifconfig.me/ip')
ip = u.read()[:-1]

r.rpush('plist', ip)
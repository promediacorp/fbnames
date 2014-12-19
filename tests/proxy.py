from flask import Flask, g, render_template
from redis import StrictRedis

import random

app = Flask(__name__)
redis = StrictRedis(host='54.172.41.190')
redis.set('proxy_test_count', 0)

@app.route("/directory/people")
@app.route("/directory/people/<x>")
def home(x="something"):
  return something(x)

@app.route("/facebook.com/<anything>")
def something(anything):
  count = redis.incr('proxy_test_count')

  check = False
  if count > 5 and count <= 10:
    check = True

  progrm = "wertyuiopasdfghjklzxcvbnm"
  links = []
  for x in range(5):
    link = {}
    rnd = ''.join([random.choice(progrm) for z in range(32)])
    if x > 3:
      href = "/facebook.com/" + rnd
    else:
      href = "/directory/people/" + rnd
    link['href'] = href
    link['text'] = ''.join([random.choice(progrm) for z in range(32)])
    links.append(link)

  return render_template("links.html", check=check, links=links, count=count)

if __name__ == "__main__":
  app.run('0.0.0.0', debug=True)
# special dupe filter that ignores dupes when
# request.meta['dont_dedupe'] = True
from scrapy.dupefilter import RFPDupeFilter

class FBDupeFilter(RFPDupeFilter):
  def request_seen(self, request):
    fp = self.request_fingerprint(request)
    if request.meta.get('dont_dedupe'):
      print "Don't dedupe meta is ON!"
      return False
    elif fp in self.fingerprints:
      return True
    self.fingerprints.add(fp)
    if self.file:
      self.file.write(fp + os.linesep)
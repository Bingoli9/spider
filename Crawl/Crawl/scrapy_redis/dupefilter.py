import time

from scrapy.dupefilters import BaseDupeFilter
from scrapy.utils.request import request_fingerprint
from BloomfilterOnRedis import BloomFilter

from . import connection


class RFPDupeFilter(BaseDupeFilter):
    """Redis-based request duplication filter"""

    def __init__(self, server, key):
        self.server = server
        self.key = key
        self.bf = BloomFilter(server, key, blockNum=1)  # you can increase blockNum if your are filtering too many urls

    @classmethod
    def from_settings(cls, settings):
        server = connection.from_settings_filter(settings)
        # 去重过滤器
        key = "dupefilter:%s" % int(time.time())
        return cls(server, key)

    @classmethod
    def from_crawler(cls, crawler):
        return cls.from_settings(crawler.settings)

    def request_seen(self, request):
        fp = request_fingerprint(request)
        if self.bf.isContains(fp):
            return True
        else:
            self.bf.insert(fp)
            return False

    def close(self, reason):
        """Delete data on close. Called by scrapy's scheduler"""
        self.clear()

    def clear(self):
        """Clears fingerprints data"""
        self.server.delete(self.key)

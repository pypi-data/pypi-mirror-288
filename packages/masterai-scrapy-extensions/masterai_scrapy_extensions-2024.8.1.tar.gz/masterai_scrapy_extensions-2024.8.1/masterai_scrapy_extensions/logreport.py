# -*- coding:utf-8 -*-
import logging
import os
from datetime import datetime

import requests
from scrapy import signals
from scrapy.exceptions import NotConfigured
from twisted.internet import task

logger = logging.getLogger(__name__)


class ReportStats:
    def __init__(self, stats, interval=60.0):
        self.stats = stats
        self.interval = interval
        self.multiplier = 60.0 / self.interval
        self.task = None
        self.task_id = 0
        self.pod_name = ""
        self.report_url = ""

    @classmethod
    def from_crawler(cls, crawler):
        task_id = os.getenv("CMS_TASK_ID")
        if not task_id:
            raise NotConfigured
        pod_name = os.getenv("POD_NAME")
        if not pod_name:
            raise NotConfigured
        interval = crawler.settings.getfloat("LOGSTATS_INTERVAL", 60.0)
        report_url = crawler.settings.get("LOGREPORT_URL")
        if not report_url:
            raise NotConfigured

        o = cls(crawler.stats, interval)
        o.task_id = task_id
        o.pod_name = pod_name
        o.report_url = report_url
        crawler.signals.connect(o.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(o.spider_closed, signal=signals.spider_closed)
        crawler.signals.connect(o.item_scraped, signal=signals.item_scraped)
        crawler.signals.connect(o.item_dropped, signal=signals.item_dropped)
        crawler.signals.connect(o.response_received, signal=signals.response_received)
        return o

    def cal_key_inc_rate(self, key):
        # 现值
        value = self.stats.get_value(f"{key}_count", 0)
        # 前值
        pre_value = getattr(self, f"{key}_prev", 0)
        # 增量
        inc_value = value - pre_value
        # 增速
        inc_rate = inc_value * self.multiplier
        self.stats.set_value(f"{key}_inc", inc_value)
        self.stats.set_value(f"{key}_rate", inc_rate)
        # 重新赋值
        setattr(self, f"{key}_prev", value)

    def log(self, spider):
        self.cal_key_inc_rate("item_scraped")
        self.cal_key_inc_rate("response_received")
        child_keys = []
        crawl_detail = {"spider_name": spider.name}
        for key in self.stats.get_stats(spider=spider):
            if key.startswith("downloader"):
                crawl_detail[key] = self.stats.get_value(key, 0)
            elif key.startswith("item_scraped"):
                crawl_detail[key] = self.stats.get_value(key, 0)
                if "/" in key and key.endswith("_count"):
                    key = key.replace("_count", "")
                    child_keys.append(key)
            elif key.startswith("item_dropped"):
                crawl_detail[key] = self.stats.get_value(key, 0)
                if "/" in key and key.endswith("_count"):
                    key = key.replace("_count", "")
                    child_keys.append(key)
            elif key.startswith("response_received"):
                crawl_detail[key] = self.stats.get_value(key, 0)
            elif key.startswith("scheduler"):
                crawl_detail[key] = self.stats.get_value(key, 0)
            elif key.startswith("log_count"):
                crawl_detail[key] = self.stats.get_value(key, 0)

        for key in child_keys:
            self.cal_key_inc_rate(key)
            inc_key = f"{key}_inc"
            crawl_detail[inc_key] = self.stats.get_value(inc_key, 0)
            rate_key = f"{key}_rate"
            crawl_detail[rate_key] = self.stats.get_value(rate_key, 0)

        report_msg = {"task_id": self.task_id, "pod_name": self.pod_name, "status": crawl_detail}
        try:
            requests.post(self.report_url, json=report_msg)
        except Exception as e:
            logger.error(f"report error: {e}")

    def spider_opened(self, spider):
        self.start_time = datetime.now()
        self.stats.set_value("start_time", self.start_time, spider=spider)

        self.task = task.LoopingCall(self.log, spider)
        self.task.start(self.interval)

    def spider_closed(self, spider, reason):
        finish_time = datetime.now()
        elapsed_time = finish_time - self.start_time
        elapsed_time_seconds = elapsed_time.total_seconds()
        self.stats.set_value("elapsed_time_seconds", elapsed_time_seconds, spider=spider)
        self.stats.set_value("finish_time", finish_time, spider=spider)
        self.stats.set_value("finish_reason", reason, spider=spider)

    def item_scraped(self, item, spider):
        self.stats.inc_value(f"item_scraped_count", spider=spider)
        # add item class count
        self.stats.inc_value(f"item_scraped/{item.__class__.__name__}_count", spider=spider)

    def item_dropped(self, item, spider, exception):
        self.stats.inc_value("item_dropped_count", spider=spider)
        # add item class count
        self.stats.inc_value(f"item_dropped/{item.__class__.__name__}_count", spider=spider)
        # add item class and exception count
        self.stats.inc_value(
            f"item_dropped_reasons/{item.__class__.__name__}/{exception.__class__.__name__}_count", spider=spider
        )

    def response_received(self, spider):
        self.stats.inc_value("response_received_count", spider=spider)

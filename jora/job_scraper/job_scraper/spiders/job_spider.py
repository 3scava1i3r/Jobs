# import scrapy
# from scrapy.crawler import CrawlerProcess
# import json
# import os
# import time

# class JobSpider(scrapy.Spider):
#     name = 'job_spider'
    
#     def __init__(self, *args, **kwargs):
#         super(JobSpider, self).__init__(*args, **kwargs)
#         script_dir = os.path.dirname(os.path.abspath(__file__))
#         file_path = os.path.join(script_dir, 'unique_urls.json')
#         with open(file_path, 'r') as f:
#             self.start_urls = json.load(f)
#             self.results = []
#             self.total_urls = len(self.start_urls)
#             self.processed_count = 0
#             self.save_threshold = self.total_urls // 20  # 5% of total URLs

#     def parse(self, response):
#         job_description = response.css('#job-description-container::text').get()
#         job_info = response.css('#job-info-container::text').get()
#         job_link = response.css('.job-view-actions-container.bottom-actions-container a::attr(href)').get()

#         data = {
#             'url': response.url,
#             'job_description': job_description.strip() if job_description else None,
#             'job_info': job_info.strip() if job_info else None,
#             'job_link': job_link
#         }

#         self.results.append(data)
#         self.processed_count += 1
#         percentage = (self.processed_count / self.total_urls) * 100
#         print(f'Percentage done: {percentage:.2f}%')

#         if self.processed_count % self.save_threshold == 0:
#             self.save_progress(int(percentage))

#     def closed(self, reason):
#         self.save_progress(100)

#     def save_progress(self, percentage):
#         os.makedirs('step_3_folder', exist_ok=True)
#         filename = f'step_3_folder/job_data_{percentage}percent.json'
#         with open(filename, 'w') as f:
#             json.dump(self.results, f, indent=2)
#         print(f"Saved progress: {filename}")

# if __name__ == "__main__":
#     start_time = time.time()
#     process = CrawlerProcess({
#         'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
#         'DOWNLOAD_DELAY': 10,
#         'RANDOMIZE_DOWNLOAD_DELAY': True,
#         'AUTOTHROTTLE_ENABLED': True,
#         'AUTOTHROTTLE_START_DELAY': 1,
#         'AUTOTHROTTLE_MAX_DELAY': 60,
#         'AUTOTHROTTLE_TARGET_CONCURRENCY': 1.0,
#     })
#     process.crawl(JobSpider)
#     process.start()
#     print(f"Total execution time: {time.time() - start_time} seconds")


import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.downloadermiddlewares.retry import RetryMiddleware
from scrapy.utils.response import response_status_message
import json
import os
import time
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError, TimeoutError, TCPTimedOutError

class CustomRetryMiddleware(RetryMiddleware):
    def __init__(self, settings):
        super().__init__(settings)
        self.max_retry_times = settings.getint('RETRY_TIMES')

    def process_response(self, request, response, spider):
        if response.status in [429, 503]:
            return self._retry(request, response.status, spider) or response
        return response

    def process_exception(self, request, exception, spider):
        if isinstance(exception, (TimeoutError, TCPTimedOutError)):
            return self._retry(request, exception, spider)
        return None

class JobSpider(scrapy.Spider):
    name = 'job_spider'
    custom_settings = {
        'CONCURRENT_REQUESTS': 16,
        'DOWNLOAD_DELAY': 0.5,
        'RANDOMIZE_DOWNLOAD_DELAY': True,
        'RETRY_TIMES': 5,
        'RETRY_HTTP_CODES': [500, 502, 503, 504, 522, 524, 408, 429],
        'DOWNLOADER_MIDDLEWARES': {
            'scrapy.downloadermiddlewares.retry.RetryMiddleware': None,
            'job_scraper.spiders.job_spider.CustomRetryMiddleware': 550,
        },
    }
    
    def __init__(self, *args, **kwargs):
        super(JobSpider, self).__init__(*args, **kwargs)
        script_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(script_dir, 'unique_urls.json')
        with open(file_path, 'r') as f:
            self.start_urls = json.load(f)
        self.results = []
        self.total_urls = len(self.start_urls)
        self.processed_count = 0
        self.save_threshold = self.total_urls // 20  # 5% of total URLs

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, callback=self.parse, errback=self.errback_httpbin)


    def parse(self, response):
        job_description = response.xpath('//div[@id="job-description-container"]//text()').getall()
        job_description = ' '.join([text.strip() for text in job_description if text.strip()])
        
        job_info = response.xpath('//div[@id="job-info-container"]//text()').getall()
        job_info = ' '.join([text.strip() for text in job_info if text.strip()])
        
        job_link = response.xpath('//div[contains(@class, "job-view-actions-container")]//a/@href').get()

        data = {
            'url': response.url,
            'job_description': job_description if job_description else None,
            'job_info': job_info if job_info else None,
            'job_link': response.urljoin(job_link) if job_link else None
        }

        self.results.append(data)

        self.processed_count += 1
        percentage = (self.processed_count / self.total_urls) * 100
        print(f'Percentage done: {percentage:.2f}%')

        if self.processed_count % self.save_threshold == 0:
            self.save_progress(int(percentage))

    def errback_httpbin(self, failure):
        if failure.check(HttpError):
            response = failure.value.response
            self.logger.error(f'HttpError on {response.url}')
        elif failure.check(DNSLookupError):
            request = failure.request
            self.logger.error(f'DNSLookupError on {request.url}')
        elif failure.check(TimeoutError, TCPTimedOutError):
            request = failure.request
            self.logger.error(f'TimeoutError on {request.url}')

    def closed(self, reason):
        self.save_progress(100)

    def save_progress(self, percentage):
        os.makedirs('step_3_folder', exist_ok=True)
        filename = f'step_3_folder/job_data_{percentage}percent.json'
        with open(filename, 'w') as f:
            json.dump(self.results, f, indent=2)
        print(f"Saved progress: {filename}")

if __name__ == "__main__":
    start_time = time.time()
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    })
    process.crawl(JobSpider)
    process.start()
    print(f"Total execution time: {time.time() - start_time} seconds")

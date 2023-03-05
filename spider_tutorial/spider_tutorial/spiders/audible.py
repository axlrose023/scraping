import scrapy
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor


class AudibleSpider(scrapy.Spider):
    name = "audible"
    allowed_domains = ["www.audible.com"]
    start_urls = ["https://www.audible.com/search/"]
    rules = (
        Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True)
    )

    def start_requests(self):
        yield scrapy.Request(url="https://www.audible.com/search/", callback=self.parse, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'})

    def parse(self, response):
        container = response.xpath("//div[@class='adbl-impression-container ']/div/span/ul/li")
        for product in container:
            title = product.xpath(".//h3[contains(@class, 'bc-heading')]/a/text()").get()
            author = product.xpath(".//li[contains(@class, 'authorLabel')]/span/a/text()").getall()
            length = product.xpath(".//li[contains(@class, 'runtimeLabel')]/span/text()").get()
            yield {'title': title, 'author': author, 'length': length,
                   'User-Agent': response.request.headers['User-Agent']}

        pagination = response.xpath("//ul[contains(@class, 'pagingElements ')]")
        next_page_url = pagination.xpath(".//span[contains(@class, 'nextButton')]/a/@href").get()
        if next_page_url:
            yield response.follow(url=next_page_url, callback=self.parse, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'})

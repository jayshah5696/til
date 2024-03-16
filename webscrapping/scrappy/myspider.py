import scrapy

class MySpider(scrapy.Spider):
    name = 'myspider'
    start_urls = ['https://www.constitutionofindia.net/']

    def parse(self, response):
        # Extract all the links from the page
        links = response.css('a::attr(href)').getall()

        # Follow each link and parse the content
        for link in links:
            yield response.follow(link, callback=self.parse_content)

    def parse_content(self, response):
        # Extract the desired data from the page
        title = response.css('h1::text').get()
        content = response.css('p::text').getall()

        # Yield the extracted data as a dictionary
        yield {
            'url': response.url,
            'title': title,
            'content': ' '.join(content)
        }
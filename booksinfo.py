from scrapy import Spider
from scrapy.http import Request


def product_info(response,value):
    return response.xpath('//th[text()="' +value+'"]/following-sibling::td/text()').extract_first()

class BooksSpider(Spider):
    name="booksinfo"
    allowed_domains=['books.toscrape.com']
    start_urls=['http://books.toscrape.com']


    def parse(self,response):
        books=response.xpath('//h3/a/@href').extract()
        for book in books:
            absolute_url=response.urljoin(book)
            yield Request(absolute_url,callback=self.parse_book)
        nextpg_url=response.xpath('//a[text()="next"]/@href').extract_first()
        absolute_nextpg_url=response.urljoin(nextpg_url)
        yield Request(absolute_nextpg_url)
    def parse_book(self,response):
        title=response.css('h1::text').extract_first()
        price=response.xpath("//*[@class='price_color']/text()").extract_first()
        img_url=response.xpath("//img/@src").extract_first()

        img_url=img_url.replace('../..','http://books.toscrape.com/')
        rating=response.xpath('//*[contains(@class,"star-rating")]/@class').extract_first()
        rating=rating.replace('star-rating ','')
        description=response.xpath('//*[@id="product_description"]/following-sibling::p/text()').extract_first()
        upc=product_info(response,'UPC')
        product_type=product_info(response,'Product Type')
        price_withtax=product_info(response,'Price (incl. tax)')
        tax=product_info(response,'Tax')
        
        # yield{
        # 'title' :title ,
        # 'price':price,
        # 'img_url':img_url,
        # 'rating':rating,
        # 'description':description,
        # 'UPC':upc,
        # 'product_type':product_type,
        # 'price_withtax':price_withtax,
        # 'tax':tax,
        # 'no_of_reviews':nofreviews
        # }
        yield{ 'title':title,
        'rating':rating,
        'upc':upc,
        'product_type':product_type}

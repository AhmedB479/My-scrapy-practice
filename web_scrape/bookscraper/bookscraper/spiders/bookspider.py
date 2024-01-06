import scrapy
from bookscraper.items import BookItem

class BookspiderSpider(scrapy.Spider):
    name = "bookspider"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com/"]

    #first time response goes into parse function
    def parse(self, response):
        #used to get details from each page
        #this will get details of all the books on the main page
        books = response.css('article.product_pod')
    
             #upon next iteration the next book is chosen here
        for book in books.css('h3 a::attr(href)'):
            #we get the relative URL and turn into the book URL
            #The .extract() method in Scrapy is used to extract the text content or attribute value of a Selector object. When you perform a CSS or XPath selection on a web page using Scrapy, you get a Selector object that represents the HTML element(s) matching your query. For example, when you use response.css('h3 a::attr(href)'), you get a Selector object that represents the href attribute of the a element inside an h3 element.The .extract() method is then used to get the actual string content or attribute value.
            relative_url = book.extract()
            if 'catalogue/' in relative_url:
                book_url = 'https://books.toscrape.com/' + relative_url
            else:
                #upon getting the first code the URL jumps to the main BOOKS page
                book_url = 'https://books.toscrape.com/catalogue/' + relative_url
                #goes to the call back function toward parse book page function
            yield response.follow(book_url, callback= self.parse_book_page)

        #upon completion of one page the whole thing jumps to the next page using the following
        next_page = response.css('li.next a ::attr(href)').get()
        if next_page is not None:
            if 'catalogue/' in next_page:
                next_page_url = 'https://books.toscrape.com/' + next_page
            else:
                next_page_url = 'https://books.toscrape.com/catalogue/' + next_page
            yield response.follow(next_page_url, callback= self.parse)

    def parse_book_page(self, response):

        table_rows = response.css("table tr")
        book_item = BookItem()
        
        #gets all the details about individual books here
        book_item['url'] = response.url,
        book_item['title'] = response.css('.product_main h1::text').get(),
        book_item['upc'] = table_rows[0].css("td ::text").get(),
        book_item['product_type'] = table_rows[1].css("td ::text").get(),
        book_item['price_excl_tax'] = table_rows[2].css("td ::text").get(),
        book_item['price_incl_tax'] = table_rows[3].css("td ::text").get(),
        book_item['tax'] = table_rows[4].css("td ::text").get(),
        book_item['availability'] = table_rows[5].css("td ::text").get(),
        book_item['num_reviews'] = table_rows[6].css("td ::text").get(),
        book_item['stars'] = response.css("p.star-rating").attrib['class'],
        book_item['category'] = response.xpath("//ul[@class='breadcrumb']/li[@class='active']/preceding-sibling::li[1]/a/text()").get(),
        book_item['description'] = response.xpath("//div[@id='product_description']/following-sibling::p/text()").get(),
        book_item['price'] = response.css('p.price_color ::text').get(),

        yield book_item

##used to get overall name price and url only, here parse is supposed to loop itself
            # yield{
            #     'name' : book.css('h3 a::text').get(),
            #     'price' : book.css('.product_price .price_color::text').get(),
            #     'url' : book.css('h3 a').attrib['href'],
            # }
        # next_page = response.css('li.next a ::attr(href)').get()

        # if next_page is not None:
        #     if 'catalogue/' in next_page:
        #         next_page_url = 'https://books.toscrape.com/' + next_page
        #     else:
        #         next_page_url = 'https://books.toscrape.com/catalogue/' + next_page
        #     yield response.follow(next_page_url, callback= self.parse)



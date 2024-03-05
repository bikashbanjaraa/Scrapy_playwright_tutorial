import scrapy

from scrapy_playwright.page import PageMethod

from scrapy_playwright.page import PageMethod

    
scrolling_script = """
const scrolls = 8
let scrollCount = 0
    
// scroll down and then wait for 0.5s
const scrollInterval = setInterval(() => {
     window.scrollTo(0, document.body.scrollHeight)
    scrollCount++
    
    if (scrollCount === numScrolls) {
    clearInterval(scrollInterval)
    }
}, 500)
    """ # instruct a browser to perform infinite scrolling in JavaScript by automatically scrolling down the page eight times at an interval of 0.5 seconds in the browser


class BikiScrapingSpider(scrapy.Spider):
    name = "biki_scraping"
    allowed_domains = ["scrapingclub.com"]
    # start_urls = ["https://scrapingclub.com/exercise/list_infinite_scroll/"]



    def start_requests(self):
        url = "https://scrapingclub.com/exercise/list_infinite_scroll/" # mathi url rakhe dekhi yo pardaina else we can also do like this.
        yield scrapy.Request(url,
                             meta={"playwright":True, #it tells Scrapy to route the request through scrapy-playwright
                                   "playwright-page-method":[
                                       PageMethod("evaluate",scrolling_script),
                                       PageMethod("wait_for_timeout", 5000)

                                   ],
                                   }) 

    def parse(self, response):
        for product in response.css(".post"):
             # .post is a css class selector. .post ma nai sabai images haru dekhai rako xa after inspecting.
            url = product.css("a").attrib["href"] # this line finds the tag <a> within the '.post' elements and extract the value of the href, which usually points to the url of the product.
            image = product.css(".card-img-top").attrib["src"] #  since this is class so we used dot(.) inside css but in url 'a' is a tag so not used dot(.)
            name =product.css("h4 a::text").get()

            price = product.css("h5::text").get()

        # add the data to the list of scraped items
        yield{
            "url":url,
            "image":image,
            "name":name,
            "price":price
        }



        

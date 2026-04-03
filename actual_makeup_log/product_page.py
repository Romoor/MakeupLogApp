import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


#CrawlSpider means it can look through the entire website, not just one page
#start_urls is just the url (website) we are looking through
class UltaSpider(CrawlSpider):
   name = 'ultaspider'


   #dont need the settings file now
   custom_settings = {
       'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
       'ROBOTSTXT_OBEY': False, # Ulta's robots.txt might block crawlers
       'DEPTH_LIMIT': 10, #let it go 10 links deep for safety
       'CLOSESPIDER_ITEMCOUNT': 1, #get it to stop once it finds the product
       'DOWNLOADER_MIDDLEWARES': {
       'actual_makeup_log.middleware.SeleniumMiddleWare': 491,
       }

   }


   start_urls = ['https://ulta.com']


   #leaving LinkExtractor() empty makes it so it can find every clickable tab
   rules = (
       #callback='parse_item' means parse_item is assigned to the info linkextractor finds
       #follow = True means it is just limited to the homepage, it also can follow every link
       #to their pages, then keep going after that
       Rule(LinkExtractor(
            allow=r'/p/',
            deny=[r'/write-a-review/', r'/ask-a-question/', r'sku='] #ignore unneccessary information
            ),
            callback='parse_item',
            follow=True),
   )


   #makes it so the brand you are searching for is user input
   #__init__ is the constructor
   #self refers to this specific instance of the object
   # *args allows custom arguments that aren't specifically defines
   # **kwargs means it will allow named arguments too
   def __init__(self, brand='', search_term='', *args, **kwargs):
      
       #super means other classes can use this class (MySpider)
       super(UltaSpider, self).__init__(*args, **kwargs)


       #assign brand value
       self.brand = brand
       # Store the user input
       self.search_term = search_term


       #making sure its starting at the right place
       print(f"DEBUG: Starting at {self.start_urls}")


       #make  url based on user input of brand
       #.lower() lowercases the string for consistency and no case issues
       #.replace() replaces var brand with the user input
       #replaces any possible spaces with hyphens for consistency
       self.start_urls = [f'https://www.ulta.com/brand/{brand.lower().replace(" ", "-")}']


       print(f"DEBUG: Page found {self.start_urls}")



   def start_requests(self):
        # Ulta's search endpoint returns JSON — no JS rendering needed
        query = f'{self.brand} {self.search_term}'
        url = (
            f'https://www.ulta.com/dxl/graphql?ultasite=en-us&user-agent=gomez'
        )
        # Use the simpler search URL instead
        search_url = f'https://www.ulta.com/search?search={query.replace(" ", "+")}'
        print(f"DEBUG: Searching for '{query}' at {search_url}")
        yield scrapy.Request(url=search_url, callback=self.parse_search)
      
  


def parse_item(self, response):
   import scrapy
import json

class UltaSpider(scrapy.Spider):
    name = 'ultaspider'

    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'ROBOTSTXT_OBEY': False,
    }

    def __init__(self, brand='', search_term='', *args, **kwargs):
        super(UltaSpider, self).__init__(*args, **kwargs)
        self.brand = brand
        self.search_term = search_term

    def start_requests(self):
        # Ulta's search endpoint returns JSON — no JS rendering needed
        query = f'{self.brand} {self.search_term}'
        url = (
            f'https://www.ulta.com/dxl/graphql?ultasite=en-us&user-agent=gomez'
        )
        # Use the simpler search URL instead
        search_url = f'https://www.ulta.com/search?search={query.replace(" ", "+")}'
        print(f"DEBUG: Searching for '{query}' at {search_url}")
        yield scrapy.Request(url=search_url, callback=self.parse_search)

    def parse_search(self, response):
        print(f"DEBUG: Got response from {response.url}, status {response.status}")
        print(f"DEBUG: Response snippet: {response.text[:300]}")

        # Product cards on search/brand pages use these selectors
        products = response.css('div.ProductCard, li.ProductCard, [class*="ProductCard"]')
        print(f"DEBUG: Found {len(products)} product cards")

        for product in products:
            name = (
                product.css('[class*="product-name"]::text').get()
                or product.css('h3::text').get()
                or product.css('h2::text').get()
                or ""
            ).strip()

            if self.search_term.lower() in name.lower():
                price = product.css('[class*="price"]::text').get() or ""
                link = product.css('a::attr(href)').get() or ""
                yield {
                    'brand_searched': self.brand,
                    'product_found': name,
                    'price': price.strip(),
                    'url': response.urljoin(link),
                }
        with open('debug_response.html', 'w') as f:
            f.write(response.text)
#you will then run scrapy runspider actual_makeup_log/product_page.py -a brand="morphe" -a search_term="ChromaPlus"
#need to navigate to actutal file to run
#need -a for multiple searches
#need settings.py and scrapy.cfg

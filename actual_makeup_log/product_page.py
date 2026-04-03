
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
        'CLOSESPIDER_ITEMCOUNT': 1 #get it to stop once it finds the product
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


        
    

    def parse_item(self, response):
        print(f"Reached parse_item")

        #look at page title or main header for the product name
        product_name_on_page = response.css('title span::text').get() or ""
        print(f"DEBUG: Page title {response.start_urls} - Content snippet: {response.text[:500]}")


        #if the page does have the product name return the brand, the product, and the url
        if self.search_term.lower() in product_name_on_page.lower():
               
               #find the actual title of the product
               title = response.css('title ::text').get() or ""

               print(f"DEBUG: Visiting {response.start_urls} - Content snippet: {response.text[:500]}")

               #.join() puts it all together into one string
               #.strip gets rid of whitespace before and after the title
               clean_title = " ".join(title).strip()
               return {
                'brand_searched': self.brand, 
                'product_found': product_name_on_page.strip(),
                'url': response.start_urls
            }

        
        
#you will then run scrapy runspider actual_makeup_log/product_page.py -a brand="morphe" -a search_term="ChromaPlus"
#need to navigate to actutal file to run
#need -a for multiple searches
#need settings.py and scrapy.cfg
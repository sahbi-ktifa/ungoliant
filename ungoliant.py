import scrapy;

class CSSUngoliant(scrapy.Spider):
    name = 'cssUngoliant'
    start_urls = ['https://developer.mozilla.org/en-US/docs/Web/CSS/Reference']

    def parse(self, response):
        for keyword in response.css('article#wikiArticle div.index > ul > li a::attr(href)'):
            yield response.follow(keyword, self.parseDetails)
    
    def parseDetails(self, response):
        def extract_with_css(query):
            return response.css(query).get(default='').strip()
        
        def extract_with_css_to_list(query):
            return response.css(query).getall()
            
        yield {
            'keyword': extract_with_css('.document-title h1 ::text'),
            'details': extract_with_css('article#wikiArticle > p'),
            'experimental': 'true' if extract_with_css('article#wikiArticle .blockIndicator.experimental') != '' else 'false',
            'url': response.request.url,
            'tags': extract_with_css_to_list('.wiki-block .tags > li ::text'),
            'last-modified': extract_with_css('.wiki-block time::text'),
            'type': response.css('.quick-links > ol > li:not(.toggle) ::text')[-1].extract(),
            'see_also': extract_with_css_to_list('article#wikiArticle > h2#See_also + ul > li')
        }
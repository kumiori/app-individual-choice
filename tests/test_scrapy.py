import scrapy

class JournalSpider(scrapy.Spider):
    name = "journal_spider"
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'ROBOTSTXT_OBEY': False,
        'DOWNLOAD_DELAY': 3,
    }
    start_urls = [
        'https://www.sciencedirect.com/journal/journal-of-the-mechanics-and-physics-of-solids'
    ]
    def start_requests(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Referer': 'https://www.google.com/',
        }
        yield scrapy.Request(
            url=self.start_urls[0], 
            headers=headers
        )
        
    def parse(self, response):
        # Extract journal title
        title = response.css('span.title-text::text').get()
        yield {'Journal Title': title}

        # Extract journal scope
        scope = response.css('div.aims-scope').get()
        yield {'Scope': scope.strip() if scope else "No scope information found"}

        # Follow the link to the editorial board page, if available
        editorial_board_link = response.url + "/editorial-board"
        if editorial_board_link:
            yield scrapy.Request(editorial_board_link, callback=self.parse_editorial_board)

    def parse_editorial_board(self, response):
        # Extract editorial board members
        editorial_board_section = response.css('section#editorial-board')
        if editorial_board_section:
            for member in editorial_board_section.css('div.person'):
                name = member.css('h3.name::text').get().strip()
                role = member.css('p.role::text').get().strip() if member.css('p.role::text').get() else "No role specified"
                affiliation = member.css('p.affiliation::text').get().strip() if member.css('p.affiliation::text').get() else "No affiliation specified"
                yield {
                    'Name': name,
                    'Role': role,
                    'Affiliation': affiliation
                }
        else:
            yield {'Editorial Board': 'Information not found'}
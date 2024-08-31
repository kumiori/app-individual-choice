import scrapy


# class JournalSpiderSpider(scrapy.Spider):
#     name = "journal_spider"
#     allowed_domains = ["sciencedirect.com"]
#     start_urls = ["https://sciencedirect.com"]

#     def parse(self, response):
#         pass


class JournalSpider(scrapy.Spider):
    name = "journal_spider"
    start_urls = [
        'https://www.sciencedirect.com/journal/journal-of-the-mechanics-and-physics-of-solids'
    ]

    def parse(self, response):
        # Extract journal title
        title = response.css('span.title-text::text').get()
        yield {'Journal Title': title}

        # Extract journal scope
        scope = response.css('div.aims-scope').get()
        yield {'Scope': scope.strip() if scope else "No scope information found"}

        # Follow the link to the editorial board page, if available
        editorial_board_link = response.url + "/about/editorial-board"
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
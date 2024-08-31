import scrapy

class JournalSpider(scrapy.Spider):
    name = "journal_spider"
    start_urls = [
        'https://www.sciencedirect.com/journal/journal-of-the-mechanics-and-physics-of-solids'
    ]

    def parse(self, response):
        # Extract the editor's name
        editor = response.css('h3.js-editor-name.name::text').get()
        if editor:
            editor = editor.strip()

        # Extract the article publishing charge for open access
        apc = response.css('div.article-publishing-charge .list-price.u-h2::text').get()
        if apc:
            apc = apc.strip()

        # Extract the time to first decision
        time_to_first_decision = response.css('div.metric .value.u-h2::text').getall()[1]
        if time_to_first_decision:
            time_to_first_decision = time_to_first_decision.strip()

        # Extract the review time
        review_time = response.css('div.metric .value.u-h2::text').getall()[2]
        if review_time:
            review_time = review_time.strip()

        # Extract the submission to acceptance time
        submission_to_acceptance = response.css('div.metric .value.u-h2::text').getall()[3]
        if submission_to_acceptance:
            submission_to_acceptance = submission_to_acceptance.strip()

        # Extract the Impact Factor
        impact_factor = response.css('div.js-impact-factor .text-l.u-display-block::text').get()
        if impact_factor:
            impact_factor = impact_factor.strip()

        # Extract the CiteScore
        citescore = response.css('div.js-cite-score .text-l.u-display-block::text').get()
        if citescore:
            citescore = citescore.strip()

        # Extract the "About the journal" section
        about_the_journal = response.css('div.about-container p.js-content-container::text').getall()
        about_the_journal = " ".join(about_the_journal).strip()

        yield {
            'Editor': editor,
            'Article Publishing Charge': apc,
            'Time to First Decision': time_to_first_decision,
            'Review Time': review_time,
            'Submission to Acceptance': submission_to_acceptance,
            'Impact Factor': impact_factor,
            'CiteScore': citescore,
            'About the Journal': about_the_journal,
        }
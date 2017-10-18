from indeed_scrapy.items import IndeedCompanyReview
import scrapy

class indeed_review_spider(scrapy.Spider):
    name = 'indeed_scrapy'
    allowed_urls = ['https://www.indeed.com/']
    start_urls = ['https://www.indeed.com/Best-Places-to-Work/2017-US-Fortune-500-Companies']
    #early stage of project (oct17) starting at company review page

    def parse(self, response):
        url_list = response.xpath('//div[@id = "cmp-curated"]/div[@class = "cmp-company-tile-name"]/a/@href').extract()
        # SEAN - how would I get page 2 at the same time? Selenium?
        pageurl = ['https://www.indeed.com' + l for l in url_list]
        top_list = response.xpath('//div[@id = "cmp-discovery-body"]//h1[@class = "cmp-discovery-title"]/text()').extract_first()

        for url in pageurl[0:10]:
            yield scrapy.Request(url, callback=self.parse_company, meta={'top_list':top_list})

        #scrapy.Request(url, callback=self.parse, meta={'top_list':top_list})


    def parse_company(self, response):

        top_list = response.meta['top_list']

        company_name = response.xpath('//div[@id="cmp-name-and-rating"]/div[@class = "cmp-company-name"]/text()').extract_first()
        company_count_salaries = response.xpath('//li[@class = "cmp-menu--salaries"]//div[@class = "cmp-note"]/text()').extract_first()
        company_count_jobs = response.xpath('//li[@class = "cmp-menu--salaries"]//div[@class = "cmp-note"]/text()').extract_first()
        company_count_photos = response.xpath('//li[@class = "cmp-menu--jobs"]//div[@class = "cmp-note"]/text()').extract_first()
        company_count_QnA = response.xpath('//li[@class = "cmp-menu--qna"]//div[@class = "cmp-note"]/text()').extract_first()
        company_url = response.url

        company_count_reviews = response.xpath('//li[@class = "cmp-menu--reviews"]//a/div[@class = "cmp-note"]/text()').extract_first()

        item = IndeedCompanyReview()
        item['top_list'] = top_list
        item['company_name'] = company_name
        item['company_count_reviews'] = company_count_reviews
        item['company_count_salaries'] = company_count_salaries
        item['company_count_jobs'] = company_count_jobs
        item['company_count_photos'] = company_count_photos
        item['company_count_QnA'] = company_count_QnA
        item['company_url'] = company_url


        review_page_urls = [response.url]


        review_count  = int(company_count_reviews.replace('K','00').replace('.',''))
        review_page_urls = review_page_urls + \
                          [response.url + '/reviews?start=' + str(ls * 20) for ls in range(1, review_count // 20 + 1)]

        #iterate through review pages
        for url in review_page_urls:
            yield scrapy.Request(url, callback = self.parse_review_page, meta={'item': item})

    def parse_review_page(self, response):
        item_co = response.meta['item']

        reviews = response.xpath('//div[@class = "cmp-review-container"]')
        for review in reviews:
            item = item_co

            review_title = review.xpath('.//span[@itemprop = "name"]/text()').extract()
            # reviewer_job_title = scrapy.Field()
            # reviewer_company_empl_status = scrapy.Field()
            # reviewer_job_location = scrapy.Field()
            # review_date = scrapy.Field()
            #
            # agg_rating = scrapy.Field()
            # # optional ratings
            # work_life_rating = scrapy.Field()
            # comp_ben_rating = scrapy.Field()
            # jobsec_advancement_rating = scrapy.Field()
            # management_rating = scrapy.Field()
            # culture_rating = scrapy.Field()
            #
            # main_text = scrapy.Field()
            # # optional text
            # pro_text = scrapy.Field()
            # con_text = scrapy.Field()
            #
            # # optional up/down votes on helpfulness
            # helpful_upvote_count = scrapy.Field()
            # helpful_downvote_count = scrapy.Field()


            item['review_title'] = review_title

            yield item


    #def parse_review(self, response):
        #########
        # for later
        ####


        #
        # app_links = ['https://play.google.com/store/apps/details?id='+ id_ for id_ in app_id]
        #
        # for link in app_links:
        #     yield scrapy.Request(link, callback=self.parse_each)
        #
        # name = response.xpath('//div[@class="id-app-title"]/text()').extract_first()
        # company = response.xpath('//span[@itemprop="name"]/text()').extract_first()
        # category = response.xpath('//span[@itemprop="genre"]/text()').extract_first()
        #
        # reviews = response.xpath('//div[@class="single-review"]')
        #
        # for review in reviews:
        #     content = review.xpath('./div[@class="review-body with-review-wrapper"]/text()').extract()
        #     content = ''.join(content).strip()
        #     rating = review.xpath(
        #         './/div[@class="tiny-star star-rating-non-editable-container"]/@aria-label').extract_first()
        #
        #     item = GooglePlayItem()
        #     item['top_list'] = top_list
        #     item['name'] = name
        #     item['company'] = company
        #     item['content'] = content
        #     item['rating'] = rating
        #     item['category'] = category
        #
        #     yield item
        #
        #

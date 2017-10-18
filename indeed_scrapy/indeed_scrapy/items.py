# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class IndeedCompanyReview(scrapy.Item):
    # this Item will record a review of a company by a reviewer who claims to be an an employee, on indeed.com:
    # should follow up by scraping company specific data like number of reviews, agg rating, salaries

    #company fields. SEAN - can this be counted at a higher level?
    company_name = scrapy.Field()
    company_count_reviews = scrapy.Field()
    company_count_salaries = scrapy.Field()
    company_count_jobs = scrapy.Field()
    company_count_photos = scrapy.Field()
    company_count_QnA = scrapy.Field()
    company_url = scrapy.Field()

    top_list = scrapy.Field()
    review_title = scrapy.Field()
    reviewer_job_title = scrapy.Field()
    reviewer_company_empl_status = scrapy.Field()
    reviewer_job_location = scrapy.Field()
    review_date = scrapy.Field()



    agg_rating = scrapy.Field()
    # optional ratings
    work_life_rating = scrapy.Field()
    comp_ben_rating = scrapy.Field()
    jobsec_advancement_rating = scrapy.Field()
    management_rating = scrapy.Field()
    culture_rating = scrapy.Field()

    main_text = scrapy.Field()
    #optional text
    pro_text = scrapy.Field()
    con_text = scrapy.Field()

    # optional up/down votes on helpfulness
    helpful_upvote_count = scrapy.Field()
    helpful_downvote_count = scrapy.Field()
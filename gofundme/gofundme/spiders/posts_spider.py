import json
import scrapy
import pandas as pd
class PostsSpider(scrapy.Spider):
    name = 'posts'
    page=0
    data = pd.read_csv('url_list_final.csv', header=0, names=['url'])

    start_urls = []
    name_list =[]
    for url in data['url']:
        name = url.split('/')
        name = name[len(name)-1]
        name_list.append(name)
        start_urls.append(url)

    page=0
    api_url='https://gateway.gofundme.com/web-gateway/v1/feed/help-a-front-line-nurse-and-baby-get-proper-care/donations?limit=20&offset={}&sort=recent'
    start_urls=[api_url.format(page)]

    def parse(self, response):
        data=json.loads(response.text)
        for donation in data['references']['donations']:
            yield {
                'donation_id':donation['donation_id'],
                'amount':donation['amount'],
                'is_offline':donation['is_offline'],
                'is_anonymous':donation['is_anonymous'],
                'name':donation['name'],
                'created_at':donation['created_at'],
                'profile_url':donation['profile_url'],
                'verified':donation['verified']
            }
        if data['meta']['has_next']:
            self.page += 20
            yield scrapy.Request(url=self.api_url.format(self.page),callback=self.parse)






    # colnames = ['index', 'url', 'cat', 'pos']
    # data = pd.read_csv('GFM_url_list.csv', names=colnames, header=None, sep='\t')
    #
    # list = {'https://www.gofundme.com/f/aeany-keep-city-lights-books-alive'}
    # # list.pop()
    # # for url in data['url']:
    # #     list.add(url)
    #
    # name = 'posts'
    # # start_urls={
    # #     'https://www.gofundme.com/f/meal-delivery-puget-sound-covid-19-hospital-staff'
    # # }
    # start_urls=list
    # print(start_urls)
    # def parse(self, response):
    #
    #     # for post in response.css('div.cell.grid-item.small-6.medium-4.js-fund-tile'):
    #     #     yield {
    #     #         'link':post.css('.react-campaign-tile a::attr(href)').get()
    #     #     }
    #
    #     # next_page = response.css('a.next-posts-link::attr(href)').get()
    #     # if next_page is not None:
    #     #     next_page=response.urljoin(next_page)
    #     #     yield scrapy.Request(next_page, callback=self.parse)
    #
    #     yield{
    #         'title':response.xpath('//*[@id="root"]/div/main/div/header/h1/text()').extract(),
    #         'current_amount':response.xpath('//*[@id="root"]/div/main/div/div[2]/aside/div[1]/div[1]/h2/text()').extract(),
    #         'goal_amount': response.xpath(
    #             '//*[@id="root"]/div/main/div/div[2]/aside/div[1]/div[1]/h2/span/text()').extract(),
    #         'create_time':response.xpath('//*[@id="root"]/div/main/div/div[3]/div/div[1]/ul/li[1]/span/text()').extract(),
    #         'categories': response.xpath('//*[@id="root"]/div/main/div/div[3]/div/div[1]/ul/li[2]/a/text()').extract(),
    #         'donations_link':response.xpath('//*[@id="root"]/div/main/div/div[2]/aside/div[2]/div[2]/a/@href').extract(),
    #         # 'organizer':response.xpath('//*[@id="campaign-members"]/div[2]/div[1]/div/div/div[1]/text()').extract(),
    #         'organizer':response.css('div.m-person-info-name::text').get(),
    #         'num_of_donors':response.xpath('//*[@id="root"]/div/main/div/div[4]/div[1]/div/ul/li[1]/button/span[1]/text()').extract(),
    #         'num_of_shares': response.xpath(
    #             '//*[@id="root"]/div/main/div/div[4]/div[1]/div/ul/li[2]/span/span[1]/text()').extract(),
    #         'num_of_donation': response.xpath('//*[@id="root"]/div/main/div/div[4]/div[3]/h2/button/text()').extract(),
    #         'num_of_followers': response.xpath(
    #             '//*[@id="root"]/div/main/div/div[4]/div[1]/div/ul/li[3]/button/span[1]/text()').extract(),
    #         'text': response.xpath('//*[@id="root"]/div/main/div/div[3]/div/div[2]/div/text()').extract(),
    #         'jpg':response.xpath('//*[@id="root"]/div/main/div/div[1]/ul/li/button/div').extract()
    #         # 'update':response.css('div.o-expansion-list-header').get()
    #     }


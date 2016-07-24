import scrapy
from lamchame.items import LamChaMeItem


class LCMSpider(scrapy.Spider):
    name = 'lamchame'
    allowed_domains = ['lamchame.com']

    # truong lop hoc hanh
    # root_url = 'https://www.lamchame.com/forum/forums/truong-lop-hoc-hanh.38/'

    # tieng anh cho con
    # root_url = 'https://www.lamchame.com/forum/forums/tieng-anh-cho-con.322/'

    # tai chinh gia dinh
    root_url = 'https://www.lamchame.com/forum/forums/tai-chinh-gia-dinh.125/'

    start_urls = []

    url = ''

    # truong lop hoc hanh
    # for i in range(0, 342):

    # tieng anh cho con
    for i in range(0, 179):
        url = root_url + 'page-' + str(i)
        start_urls.append(url)

    def parse(self, response):
        for href in response.xpath('//a[@class="PreviewTooltip"]/@href'):
            url = response.urljoin(href.extract())
            yield scrapy.Request(url, callback=self.parse_dir_contents)

        # file_name = response.url.split('/')[-2] + '.html'
        # with open(file_name, 'wb') as f:
        #     f.write(response.body)

    def parse_dir_contents(self, response):
        for sel in response.xpath('//div[@class="messageContent"]/article'):
            body = ''
            arr = map(unicode.strip, sel.xpath('blockquote[@class="messageText SelectQuoteContainer ugc baseHtml"]/text()').extract())

            for x in arr:
                if x != '' and x != ' ':
                    x = x.rstrip('\n')
                    body += x

            if len(body) >= 10:
                item = LamChaMeItem()
                item['post_body'] = body
                yield item
            else:
                continue

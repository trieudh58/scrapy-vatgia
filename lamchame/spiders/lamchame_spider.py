import scrapy
from lamchame.items import LamChaMeItem


class LCMSpider(scrapy.Spider):
    name = 'lamchame'
    allowed_domains = ['vatgia.com']

    # chototvn - vat nuoi thu cung
    # root_url = 'https://www.chotot.com/ha-noi/mua-ban-vat-nuoi-thu-cung'

    # san pham khac
    # root_url = 'https://www.chotot.com/ha-noi/mua-ban-cac-loai-khac'

    # du lich
    # root_url = 'https://www.chotot.com/toan-quoc/du-lich'

    # the thao
    # root_url = 'https://www.chotot.com/toan-quoc/mua-ban-do-the-thao-da-ngoai'

    # phu kien thoi tr
    # root_url = 'hatgiattps://www.chotot.com/toan-quoc/mua-ban-giay-dep-tui-xach-phu-kien'

    root_url = 'http://www.vatgia.com/raovat/type.php?iCat=3794'

    start_urls = []

    url = ''

    for i in range(2, 14):
        url = root_url + '&page=' + str(i)
        start_urls.append(url)

    def parse(self, response):
        for href in response.xpath('//h2/a[@class="raovat_name tooltip"]/@href'):
            url = response.urljoin(href.extract())
            yield scrapy.Request(url, callback=self.parse_dir_contents)

    def parse_dir_contents(self, response):
        # for sel in response.xpath('//span'):
        sel = response.xpath('//span')
        body = ''
        arr = map(unicode.strip, sel.xpath('span/text()').extract())
        # arr = sel.xpath('span/text()').extract()
        for x in arr:
            # x = map(unicode.strip, x)
            if '(8h - 21h' in x:
                arr.remove(x)
                continue
            if x != '' and x != ' ':
                x = x.replace('\n', ' ')
                x = x.replace('\t', '')
                body += x

        # print body

        if 10 < len(body) < 3000:
            item = LamChaMeItem()
            item['post_body'] = body
            yield item

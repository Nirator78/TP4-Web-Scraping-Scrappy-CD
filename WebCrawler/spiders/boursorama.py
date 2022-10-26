import scrapy
from scrapy import Request
from WebCrawler.items import ReviewsBoursoramaItem
import mysql.connector as mc
from datetime import datetime

class BoursoramaSpider(scrapy.Spider):
    name = 'boursorama'
    allowed_domains = ['www.boursorama.com']
    start_urls = ['https://www.boursorama.com/bourse/actions/palmares/france/']

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url=url, callback=self.parse)
    
    def parse(self, response):
        liste_indice = response.css('tbody.c-table__body').css('tr.c-table__row')
        
        # Boucle qui parcours l'ensemble des éléments de la liste des indices
        for indice in liste_indice:
            item = ReviewsBoursoramaItem()

            # Nom de l'indice
            try:
                item['name'] = indice.css('a.c-link::text').get()
            except:
                item['name'] = 'None'
            # Dernier prix
            try:
                item['last'] = indice.css('span.c-instrument::text').extract()[0]
            except:
                item['last'] = 'None'
            # Variation
            try:
                item['variation'] = indice.css('span.c-instrument::text').extract()[1]
            except:
                item['variation'] = 'None'
            # Open
            try:
                item['open'] = indice.css('span.c-instrument::text').extract()[2]
            except:
                item['open'] = 'None'
            # High
            try:
                item['high'] = indice.css('span.c-instrument::text').extract()[3]
            except:
                item['high'] = 'None'
            # Low
            try:
                item['low'] = indice.css('span.c-instrument::text').extract()[4]
            except:
                item['low'] = 'None'
            # Volume
            try:
                item['volume'] = indice.css('span.c-instrument::text').extract()[5]
            except:
                item['volume'] = 'None'

            # Date de la collecte
            try:
                item['time'] = datetime.now().strftime("%Y-%m-%d  %H:%M:%S")
            except:
                item['time'] = 'None'
                
            db = mc.connect(
                host="localhost",
                user="root",
                password="Azerty94",
                database="webscraping"
            )

            cursor = db.cursor()

            sql = "INSERT INTO `webscraping`.`boursorama` (`high`, `last`, `low`, `name`, `open`, `variation`, `volume`, `time`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
            val = (item['high'], item['last'], item['low'], item['name'], item['open'], item['variation'], item['volume'], item['time'])
            cursor.execute(sql, val)
            db.commit()

            yield item
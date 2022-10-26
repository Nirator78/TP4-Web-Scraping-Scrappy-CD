import scrapy
from scrapy import Request
from WebCrawler.items import ReviewsAllocineItem
# from save_in_database import save_in_database
import mysql.connector as mc

class AllocineSpider(scrapy.Spider):
    name = 'allocine'
    allowed_domains = ['www.allocine.fr']
    start_urls = [f'https://www.allocine.fr/film/meilleurs/?page={n}' for n in range(10)]

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url=url, callback=self.parse)
        

    def parse(self, response):
        liste_film = response.css('li.mdl')
        
        # Boucle qui parcours l'ensemble des éléments de la liste des films
        for film in liste_film:
            item = ReviewsAllocineItem()

            # Nom du film
            try:
                item['title'] = film.css('a.meta-title-link::text').extract()[0]
            except:
                item['title'] = 'None'
              
            # Lien de l'image du film
            try:
                item['img'] = film.css('img.thumbnail-img').attrib['src']
                # Si l'image est de la data en base 64 on récupère l'argument data-src
                if item['img'].startswith('data:image'):
                    item['img'] = film.css('img.thumbnail-img').attrib['data-src']
            except:
                item['img'] = 'None'

            # Auteur du film
            try:
                item['author'] = film.css('a.blue-link::text').extract()[0]
            except:
                item['author'] = 'None'
           
            # Durée du film
            try:
                item['time'] = film.css('div.meta-body-item::text').extract()[0].strip('\n')
            except:
                item['time'] = 'None'

            # Genre cinématographique
            try:
                item['genre'] = '-'.join(film.css('li.mdl div.meta-body-info')[0].css('span::text').extract()[1::])
            except:
                 item['genre'] = 'None'

            # Score du film
            try:
                item['score'] = film.css('span.stareval-note::text')[0].extract()[0]
            except:
                item['score'] = 'None'

            # Description du film
            try:
                item['desc'] = film.css('div.content-txt::text').extract()[0].strip('\n')
            except:
                item['desc'] = 'None'

            # Date de sortie
            try:
                item['release'] = film.css('span.date::text').extract()[0]
            except:
                item['release'] = 'None'
            db = mc.connect(
                host="localhost",
                user="root",
                password="Azerty94",
                database="webscraping"
            )

            cursor = db.cursor()

            def save_in_database(item):
                sql = "INSERT INTO `webscraping`.`allocine` (`title`, `img`, `author`, `time`, `genre`, `score`, `desc`, `release`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
                val = (item['title'], item['img'], item['author'], item['time'], item['genre'], item['score'], item['desc'], item['release'])
                cursor.execute(sql, val)
                db.commit()
            save_in_database(item)

            yield item
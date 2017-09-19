
from bs4 import BeautifulSoup
import csv
import html5lib
from urllib.request import urlopen
import requests
import lxml


class publicacionMoto:
    titulo = ''
    precio = ''
    año = ''
    km = ''
    link = ''
    def __str__(self):
        return ''.join([self.titulo ,'\n' ,self.precio ,'\n', self.año ,'\n', self.km,'\n', self.link  , '\n'])


listaPublicaciones = []


def scrapearPagina(theUrl):
    pageHTML = requests.get(theUrl).text
    soup = BeautifulSoup(pageHTML, 'html5lib')



    publicaciones = soup.find_all('li' , 'results-item article')

    for unaPublicacion in publicaciones:
        nuevaPublicacion = publicacionMoto()
        nuevaPublicacion.titulo =  unaPublicacion.find('a').get_text().replace(' ' , '')
        nuevaPublicacion.precio =  unaPublicacion.find('span', class_='ch-price').get_text().replace('$ ', '').replace('.', '')
        nuevaPublicacion.año = unaPublicacion.find('li', class_='destaque').find_all('strong')[0].get_text()
        nuevaPublicacion.km = unaPublicacion.find('li', class_='destaque').find_all('strong')[1].get_text()
        nuevaPublicacion.link = unaPublicacion.find('div', class_='images-viewer').get('item-url')
        # print(nuevaPublicacion)
        listaPublicaciones.append(nuevaPublicacion)




for i in range(58):
    theUrl = 'http://motos.tucarro.com.co/yamaha/_Desde_' +  str(i*48)
    scrapearPagina(theUrl)


with open('archivo.csv', 'w') as csvfile:
    fieldnames = ['titulo', 'precio', 'año' , 'km', 'link']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    for pub in listaPublicaciones:
        writer.writerow({'titulo':pub.titulo, 'precio':pub.precio, 'año':pub.año, 'km':pub.km, 'link':pub.link})

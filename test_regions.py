import json
import unittest
import urllib.parse
import urllib.error
from urllib import request

class TestRegions(unittest.TestCase):

#тест 1 - количество элементов на странице по умолчанию
    def test_page_size_count(self):
        try:
            res = request.urlopen('https://regions-test.2gis.com/1.0/regions?q')
        except urllib.error.HTTPError as e:
            print(e.getcode())

        # body = json.loads(res.read().decode('utf-8'))
        # if body['total'] >= 15:
        #     self.assertEqual(len(body['items']), 15)

#тест 2 - проверка,что страница по умолчанию - первая
    def test_page(self):
        res1 = request.urlopen('https://regions-test.2gis.com/1.0/regions')
        body1 = json.loads(res1.read().decode('utf-8'))

        res2 = request.urlopen('https://regions-test.2gis.com/1.0/regions?page=1')
        body2 = json.loads(res2.read().decode('utf-8'))

        self.assertEqual(body1, body2)

#тест 3 - проверка работы нечеткого поиска
    def test_fuzzy_search(self):
        #проверка, что регистр не имеет значения
        term = urllib.parse.quote("рск")
        res = request.urlopen('https://regions-test.2gis.com/1.0/regions?q=' + term)
        body = json.loads(res.read().decode('utf-8'))

        term1 = urllib.parse.quote("РсК")
        res1 = request.urlopen('https://regions-test.2gis.com/1.0/regions?q=' + term1)
        body1 = json.loads(res1.read().decode('utf-8'))

        if len(body['items']) != 0 and len(body1['items']) != 0:
            for region in body['items']:
                self.assertFalse(region['name'].find('рск') == -1)

            self.assertEqual(body, body1)

        #проверка, что нельзя написать меньше трех символов
        term2 = urllib.parse.quote("сК")
        res2 = request.urlopen('https://regions-test.2gis.com/1.0/regions?q=' + term2)
        body2 = json.loads(res2.read().decode('utf-8'))
        self.assertTrue(('error' in body2) == 1)

        #проверка, что если передан параметр q, то все остальные параметры - игнорируются
        res3 = request.urlopen('https://regions-test.2gis.com/1.0/regions?page=2&country_code=cz&page_size=15&q=' + term)
        body3 = json.loads(res3.read().decode('utf-8'))
        self.assertEqual(body, body3)

#тест 4 - проверка параметра country_code (аналогично для остальных регионов)
    def test_country_code(self):
        i = 1
        while True:
            res = request.urlopen('https://regions-test.2gis.com/1.0/regions?country_code=kg&page=' + str(i))
            body = json.loads(res.read().decode('utf-8'))

            for region in body['items']:
                self.assertTrue(region['country']['code'] == "kg")

            if len(body['items']) > 0:
                i += 1
            else:
                break

#тест 5 - проверка параметра country_code на допустимые значения
    def test_country_code_allowable_values(self):
        i = 1
        while True:
            res = request.urlopen('https://regions-test.2gis.com/1.0/regions?page=' + str(i))
            body = json.loads(res.read().decode('utf-8'))

            for region in body['items']:
                self.assertTrue(['ru', 'kz', 'kg', 'cz'].count(region['country']['code']) > 0)

            if len(body['items']) > 0:
                i += 1
            else:
                break

#тест 6 - проверка ответа сервера при некорректном вводе параметров
    def test_incorrect_parametr(self):
        res = request.urlopen('https://regions-test.2gis.com/1.0/regions?country_code=251')
        self.assertEqual(res.getcode(), 400)

        res1 = request.urlopen('https://regions-test.2gis.com/1.0/regions?page=2.5')
        self.assertEqual(res1.getcode(), 400)

        term = urllib.parse.quote("ск")
        res = request.urlopen('https://regions-test.2gis.com/1.0/regions?q=' + term)
        self.assertEqual(res.getcode(), 400)

        res = request.urlopen('https://regions-test.2gis.com/1.0/regions?page_size=4')
        self.assertEqual(res.getcode(), 400)

#тест 7 - проверка параметра q при пустом значении
    def test_empty_querry(self):
        try:
            res = request.urlopen('https://regions-test.2gis.com/1.0/regions?q=')
            self.assertEqual(res.getcode(), 400)
        except urllib.error.HTTPError as error:
            self.assertEqual(error.getcode(), 400)

#тест 8 - проверка параметра page при значении 0
    def test_page_zero(self):

        try:
            res = request.urlopen('https://regions-test.2gis.com/1.0/regions?page=0')
            self.assertEqual(res.getcode(), 400)
        except urllib.error.HTTPError as error:
            self.assertEqual(error.getcode(), 400)

#тест 9 - проверка, все ли города можно найти с помощью параметра q
    def test_all_cities_query(self):
        i = 1

        while True:
            res = request.urlopen('https://regions-test.2gis.com/1.0/regions?page=' + str(i))
            body = json.loads(res.read().decode('utf-8'))

            for region in body['items']:
                self.assertTrue(len(region['name']) >= 3)

            if len(body['items']) > 0:
                i += 1
            else:
                break




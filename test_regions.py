import json
import unittest
import urllib.parse
from urllib import request

class TestRegions(unittest.TestCase):

#тест 1 - количество элементов на странице по умолчанию
    def test_page_size_count(self):
        res = request.urlopen('https://regions-test.2gis.com/1.0/regions')
        body = json.loads(res.read().decode('utf-8'))
        if body['total'] >= 15:
            self.assertEqual(len(body['items']), 15)

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



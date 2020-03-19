# coding=utf-8
import unittest2
from datetime import datetime

import utils.helpers
import utils.http_requests
import utils.http_requests

def test_get_IATA_list():
    result = utils.helpers.get_json('http://api.travelpayouts.com/data/ru/cities.json')
    assert isinstance(result, (type([])))


_test_data_IATA_CITIES = [{
    'name': 'Тест',
    'time_zone': 'test',
    'code': 'test',
    'cases': {"vi": "", "tv": "", "ro": "", "pr": "", "da": ""},
    'coordinates': {"lon": "000", "lat": "000"},
    'country_code': 'test',
    'name_translations': {"en": "test"},
}]

_test_data_supported_directions = {

    "origin": {
        "iata": "LED",
        "name": "Санкт-Петербург",
        "country": "RU",
        "coordinates": [30.315785, 59.939039]
    },
    "directions":
        [
            {
            "direct": 'true',
            "iata": "AAQ",
            "name": "Анапа",
            "country": "RU",
            "coordinates": [37.316666, 44.9],
            "weight": 0,
            "weather":
                {
                    "weathertype": 'null',
                    "temp_min": 'null',
                    "temp_max": 'null',
                }
            }
        ]
}

test_best_prices_data = {
    "errors": {},
    "current_depart_date_prices": [],
    "best_prices":
        [
            {
                "value": '6787.0',
                "trip_class": '0',
                "show_to_affiliates": 'false',
                "return_date": 'null',
                "origin": "MOW",
                "number_of_changes": '0',
                "gate": "S7",
                "found_at": "2019-11-15T01:52:26",
                "distance": '1209',
                "destination": "AAQ",
                "depart_date": "2020-04-27",
                "actual": 'true'
            },
        ]
}


class TestIATABaseClass(unittest2.TestCase):

    def setUp(self):
        self._result = api_facade.data_cities.BaseCityClass(_test_data_IATA_CITIES).get_iata()[-1]

    def test_name(self):
        assert self._result.name == 'Тест'

    def test_tzone(self):
        assert self._result.tzone == 'test'

    def test_IATA(self):
        assert self._result.iata == 'test'

    def test_coordinates(self):
        assert self._result.coordinates == {"lon": "000", "lat": "000"}

    def test_cases(self):
        assert self._result.cases == {"vi": "", "tv": "", "ro": "", "pr": "", "da": ""}

    def test_name_translations(self):
        assert self._result.name_translations == {"en": "test"}

    def test_country_code(self):
        assert self._result.country_code == 'test'




class TestBestPrices(unittest2.TestCase):
    def setUp(self):
        self._result = api_facade.aviasales_min_prices.BaseCalendarPreload(test_best_prices_data)

    def test_best_prices_value(self):
        assert self._result.get_best_prices()[0].value == 6787.0

    def test_best_prices_trip_class(self):
        assert self._result.get_best_prices()[0].trip_class == 0

    def test_best_prices_return_date(self):
        assert self._result.get_best_prices()[0].return_date == datetime.now()

    def test_best_prices_origin(self):
        assert self._result.get_best_prices()[0].origin == 'MOW'

    def test_best_prices_destination(self):
        assert self._result.get_best_prices()[0].destination == 'AAQ'

    def test_best_prices_number_of_changes(self):
        assert self._result.get_best_prices()[0].number_of_changes == 0

    def test_best_prices_gate(self):
        assert self._result.get_best_prices()[0].gate == "S7"

    def test_best_prices_distance(self):
        assert self._result.get_best_prices()[0].distance == 1209

    def test_best_prices_depart_date_null(self):
        assert self._result.get_best_prices()[0]\
                   .depart_date == datetime.strptime('2020-04-27', "%Y-%m-%d")


# class TestGetJson(unittest.TestCase):
#     def setUp(self):
#         self._url = "http://min-prices.aviasales.ru/calendar_preload"
#
#     def test_get_json(self):
#         #origin=MOW&destination=AAQ&depart_date=2019-12-01&one_way=true
#         assert 'best_prices' in utils.http_requests.get_json_raw(self._url, {"origin": "MOW",
#                                                      "destination": "MOW",
#                                                      "depart_date": "2020-12-01",
#                                                      "one_way": "true"}).keys()


class TestErrorDecorator(unittest2.TestCase):
    def test_error_http(self):
        with self.assertRaises(Exception):
            utils.http_requests.get_json_raw('http://min-prices.aviasales.ru/calendar_preload',
                                                           {
                                                                "origin": "MOW",
                                                                "destination": "WWW",
                                                                "depart_date": "2019-12-01",
                                                                "one_way": "true"
                                                           })

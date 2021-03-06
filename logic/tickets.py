# -*- coding: utf-8 -*-
import copy
from mapping import mapweather, maptickets
import json
import credentials
from utils.helpers import Mdict, run_sql_file
from abc import ABC, abstractmethod
import config
from config import main_logger

class Builder(ABC):
    """
    Интерфейс Строителя объявляет создающие методы для различных частей объектов
    Продуктов.
    """

    @abstractmethod
    def product(self) -> None:
        pass

    @abstractmethod
    def produce_part_a(self) -> None:
        pass

    @abstractmethod
    def produce_part_b(self) -> None:
        pass

    @abstractmethod
    def produce_part_c(self) -> None:
        pass

    @abstractmethod
    def produce_part_d(self) -> None:
        pass


class ConcreteBuilder1(Builder):
    """
    Классы Конкретного Строителя следуют интерфейсу Строителя и предоставляют
    конкретные реализации шагов построения. Ваша программа может иметь несколько
    вариантов Строителей, реализованных по-разному.
    """

    def __init__(self) -> None:
        """
        Новый экземпляр строителя должен содержать пустой объект продукта,
        который используется в дальнейшей сборке.
        """
        self.reset()

    def reset(self) -> None:
        self._product = Product1()

    @property
    def product(self):
        """
        Конкретные Строители должны предоставить свои собственные методы
        получения результатов. Это связано с тем, что различные типы строителей
        могут создавать совершенно разные продукты с разными интерфейсами.
        Поэтому такие методы не могут быть объявлены в базовом интерфейсе
        Строителя (по крайней мере, в статически типизированном языке
        программирования).

        Как правило, после возвращения конечного результата клиенту, экземпляр
        строителя должен быть готов к началу производства следующего продукта.
        Поэтому обычной практикой является вызов метода сброса в конце тела
        метода getProduct. Однако такое поведение не является обязательным, вы
        можете заставить своих строителей ждать явного запроса на сброс из кода
        клиента, прежде чем избавиться от предыдущего результата.
        """
        product = self._product
        self.reset()
        return product

    def produce_part_a(self) -> None:
        self._product.form_db_list_with_routes()

    def produce_part_b(self) -> None:
        self._product.form_list_with_cheap_ticket_flights('MOW')

    def produce_part_c(self) -> None:
        self._product.form_list_with_weather_info()

    def produce_part_d(self) -> None:
        self._product.make_file(
            directory=config.UPLOAD_FILE, filename='MOW_weather_tickets.json')


class Product1:
    """
    В методах продукта содержатся все необходимые для получения готового результата методы. 1) Он делает запрос к базе
    данных 2) Запрашивает внешний api для поиска билетов 3)...
    """

    def __init__(self) -> None:
        self.routes = []
        self.flights = []
        self.weather = []

    def form_db_list_with_routes(self, filename=config.SQL_FILE,
                                 conn_sring='postgres://{user}:{password}@vacation-planner-library.ciodtn8hce9y.ap-south-1.rds.amazonaws.com:5432/postgres'
                                 .format(user=credentials.DB_LOGIN, password=credentials.DB_PASSWORD),
                                 tst_res=None) -> None:

        main_logger.info('CLASS: Product1, METHOD: form_db_list_with_routes')
        #todo: make a generator from populate data function

        def populate_data(sql_res):
            for row in sql_res:
                self.routes.append(row)

        if tst_res:
            populate_data(tst_res)

        else:
            rs = run_sql_file(filename, conn_sring)
            populate_data(rs)

        main_logger.debug(self.routes)


    def form_list_with_cheap_ticket_flights(self, origin: str) -> None:
        main_logger.info('CLASS: Product1, METHOD: form_list_with_cheap_ticket_flights ')

        def _chunk(route_data):
            return maptickets.get_info_from_api_with_mapping(route_data['arrival_iata']
                                                      , api='http://api.travelpayouts.com/v1/prices/cheap'
                                                      , mapping=maptickets.BasePricesCheap
                                                      , url_params={'currency': 'RUB',
                                                                    'origin': origin,
                                                                    'destination': route_data['arrival_iata'],
                                                                    'token': credentials.TRAVELPAYOUTS_TOKEN
                                                                    })

        if self.routes:
            for route in self.routes:
                for item in _chunk(route):
                    item.data.update(route)
                    self.flights.append(item.data)
        main_logger.debug(self.routes)


    def form_list_with_weather_info(self) -> None:
        main_logger.info('CLASS: Product1, METHOD: form_list_with_weather_info')
        for item in self.flights:
            weather_json = mapweather.weather_data(item['name']).form_json()
            aviasales_item = copy.deepcopy(item)
            self.weather.append(Mdict(weather_json) + Mdict(aviasales_item))
        main_logger.debug(self.weather)

    def make_file(self, directory: str, filename: str):
        main_logger.info('CLASS: Product1, METHOD: make_file')
        with open("{path}/{filename}".format(path=directory, filename=filename), "w+") as wf:
            json.dump(self.weather, wf)

class Director:
    """
    Директор отвечает только за выполнение шагов построения в определённой
    последовательности. Это полезно при производстве продуктов в определённом
    порядке или особой конфигурации. Строго говоря, класс Директор необязателен,
    так как клиент может напрямую управлять строителями.
    """

    def __init__(self) -> None:
        self._builder = None

    @property
    def builder(self) -> Builder:
        return self._builder

    @builder.setter
    def builder(self, builder: Builder) -> None:
        """
        Директор работает с любым экземпляром строителя, который передаётся ему
        клиентским кодом. Таким образом, клиентский код может изменить конечный
        тип вновь собираемого продукта.
        """
        self._builder = builder

    """
    Директор может строить несколько вариаций продукта, используя одинаковые
    шаги построения.
    """

    def build_file_to_upload(self) -> None:
        self.builder.produce_part_a()
        self.builder.produce_part_b()
        self.builder.produce_part_c()
        self.builder.produce_part_d()



if __name__ == "__main__":
    director = Director()
    builder = ConcreteBuilder1()
    director.builder = builder

    director.build_file_to_upload()


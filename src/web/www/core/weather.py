# coding:utf-8

import itertools
from web.www.helper import *
from web.db import get_new_db


class Weather(object):

    @staticmethod
    def factory():
        if hasattr(Weather, '_obj'):
            return Weather._obj

        obj = Weather()
        Weather._obj = obj

        return obj

    @staticmethod
    def get_group_weather_city():
        with get_new_db() as conn:
            rows = conn.execute('select * from weather_city order by city_url asc').fetchall()

            data = {}
            for row in rows:
                letter = row['city_url'][7].upper()
                print row['city_url'], letter

                if letter not in data:
                    data[letter] = []
                data[letter].append(row['city_name'])

            return sorted(data.items())

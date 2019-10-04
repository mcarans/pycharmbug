#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
"""
from os.path import join

import pytest
from hdx.data.vocabulary import Vocabulary
from hdx.hdx_configuration import Configuration
from hdx.hdx_locations import Locations
from hdx.location.country import Country
from hdx.utilities.path import temp_dir

from pycharmbug import generate_dataset_and_showcase


class TestWorldBank:
    gender = [{'id': 'SH.STA.MMRT', 'name': 'Maternal mortality ratio (modeled estimate, per 100, 000 live births)', 'unit': '', 'source': {'id': '2', 'value': 'World Development Indicators'}, 'sourceNote': 'Maternal mortality ratio is ...', 'sourceOrganization': 'WHO, UNICEF, UNFPA, World Bank Group, and the United Nations Population Division. Trends in Maternal Mortality:  2000 to 2017. Geneva, World Health Organization, 2019', 'topics': [{'id': '8', 'value': 'Health '}, {'id': '17', 'value': 'Gender'}, {'id': '2', 'value': 'Aid Effectiveness '}]},
              {'id': 'SG.LAW.CHMR', 'name': 'Law prohibits or invalidates child or early marriage (1=yes; 0=no)', 'unit': '', 'source': {'id': '2', 'value': 'World Development Indicators'}, 'sourceNote': 'Law prohibits or invalidates...', 'sourceOrganization': 'World Bank: Women, Business and the Law.', 'topics': [{'id': '13', 'value': 'Public Sector '}, {'id': '17', 'value': 'Gender'}]},
              {'id': 'SP.ADO.TFRT', 'name': 'Adolescent fertility rate (births per 1,000 women ages 15-19)', 'unit': '', 'source': {'id': '2', 'value': 'World Development Indicators'}, 'sourceNote': 'Adolescent fertility rate is...', 'sourceOrganization': 'United Nations Population Division,  World Population Prospects.', 'topics': [{'id': '8', 'value': 'Health '}, {'id': '17', 'value': 'Gender'}, {'id': '15', 'value': 'Social Development '}]},
              {'id': 'SH.MMR.RISK', 'name': 'Lifetime risk of maternal death (1 in: rate varies by country)', 'unit': '', 'source': {'id': '2', 'value': 'World Development Indicators'}, 'sourceNote': 'Life time risk of maternal death is...', 'sourceOrganization': 'WHO, UNICEF, UNFPA, World Bank Group, and the United Nations Population Division. Trends in Maternal Mortality:  2000 to 2017. Geneva, World Health Organization, 2019', 'topics': [{'id': '8', 'value': 'Health '}, {'id': '17', 'value': 'Gender'}]}]
    indicators1 = [{'page': 1, 'pages': 1, 'per_page': 10000, 'total': 236, 'sourceid': None, 'lastupdated': '2019-10-02'},
                   [{'indicator': {'id': 'SH.STA.MMRT', 'value': 'Maternal mortality ratio (modeled estimate, per 100,000 live births)'}, 'country': {'id': 'AF', 'value': 'Afghanistan'}, 'countryiso3code': 'AFG', 'date': '2016', 'value': 673, 'unit': '', 'obs_status': '', 'decimal': 0},
                    {'indicator': {'id': 'SG.LAW.CHMR', 'value': 'Law prohibits or invalidates child or early marriage (1=yes; 0=no)'}, 'country': {'id': 'AF', 'value': 'Afghanistan'}, 'countryiso3code': 'AFG', 'date': '2016', 'value': 1, 'unit': '', 'obs_status': '', 'decimal': 1}]]
    indicators2 = [{'page': 1, 'pages': 1, 'per_page': 10000, 'total': 236, 'sourceid': None, 'lastupdated': '2019-10-02'},
                   [{'indicator': {'id': 'SP.ADO.TFRT', 'value': 'Adolescent fertility rate (births per 1,000 women ages 15-19)'}, 'country': {'id': 'AF', 'value': 'Afghanistan'}, 'countryiso3code': 'AFG', 'date': '2016', 'value': 75.325, 'unit': '', 'obs_status': '', 'decimal': 0},
                    {'indicator': {'id': 'SH.MMR.RISK', 'value': 'Lifetime risk of maternal death (1 in:  rate varies by country)'}, 'country': {'id': 'AF', 'value': 'Afghanistan'}, 'countryiso3code': 'AFG', 'date': '2016', 'value': 30, 'unit': '', 'obs_status': '', 'decimal': 0}]]

    @pytest.fixture(scope='function')
    def configuration(self):
        Configuration._create(hdx_read_only=True, user_agent='test',
                              project_config_yaml=join('tests', 'config', 'project_configuration.yml'))
        Locations.set_validlocations([{'name': 'afg', 'title': 'Afghanistan'}])
        Country.countriesdata(False)
        Vocabulary._tags_dict = True
        Vocabulary._approved_vocabulary = {'tags': [{'name': 'hxl'}, {'name': 'gender'}, {'name': 'economics'}, {'name': 'indicators'}], 'id': '4e61d464-4943-4e97-973a-84673c1aaa87', 'name': 'approved'}

    @pytest.fixture(scope='function')
    def downloader(self):
        class Response:
            @staticmethod
            def json():
                pass

        class Download:
            @staticmethod
            def download(url):
                response = Response()
                if url == 'http://papa/v2/en/country/AFG/indicator/SH.STA.MMRT;SG.LAW.CHMR?source=2&format=json&per_page=10000':
                    def fn():
                        return TestWorldBank.indicators1
                    response.json = fn
                elif url == 'http://papa/v2/en/country/AFG/indicator/SP.ADO.TFRT;SH.MMR.RISK?source=2&format=json&per_page=10000':
                    def fn():
                        return TestWorldBank.indicators2
                    response.json = fn
                return response
        return Download()

    def test_generate_dataset_and_showcase(self, configuration, downloader):
        with temp_dir('worldbank') as folder:
            topic = {'id': '17', 'value': 'Gender & Science', 'sourceNote': 'Gender equality is a core development objective...',
                     'tags': ['gender', 'science'], 'sources': {'2': TestWorldBank.gender}}
            generate_dataset_and_showcase('http://papa/', downloader, 'AFG', 'Afghanistan', topic, 60, 25)

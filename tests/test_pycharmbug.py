# -*- coding: UTF-8 -*-
"""Dataset Title Helper Tests"""
from datetime import datetime

from hdx.data.dataset_title_helper import DatasetTitleHelper


class TestDatasetTitleHelper:
    def test_get_date_from_title(self):
        assert DatasetTitleHelper.get_dates_from_title('Myanmar Town 2019 July') == \
               ('Myanmar Town', [(datetime(2019, 7, 1, 0, 0), datetime(2019, 7, 31, 0, 0))])

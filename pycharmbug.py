#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
"""
import logging

from hdx.data.dataset import Dataset
logger = logging.getLogger(__name__)


def generate_dataset_and_showcase(base_url, downloader, countryiso, countryname, topic,
                                  indicator_limit, character_limit):
    topicname = topic['value'].replace('&', 'and')
    title = '%s - %s' % (countryname, topicname)

    dataset = Dataset({
        'name': 'wb',
        'title': title,
    })
    dataset.set_maintainer('196196be-6037-4488-8b71-d786adf4c081')
    dataset.set_organization('hdx')
    dataset.set_subnational(False)
    try:
        dataset.add_country_location(countryiso)
    except ValueError as e:
        logger.exception('%s has a problem! %s' % (countryname, e))
        return

    start_url = '%sv2/en/country/%s/indicator/' % (base_url, countryiso)
    for source_id in topic['sources']:
        indicator_list = topic['sources'][source_id]
        indicator_list_len = len(indicator_list)
        i = 0
        while i < indicator_list_len:
            ie = min(i + indicator_limit, indicator_list_len)
            indicators_string = ';'.join([x['id'] for x in indicator_list[i:ie]])
            if len(indicators_string) > character_limit:
                indicators_string = ';'.join([x['id'] for x in indicator_list[i:ie-2]])
                i -= 2
            url = '%s%s?source=%s&format=json&per_page=10000' % (start_url, indicators_string, source_id)
            response = downloader.download(url)
            json = response.json()
            if json[0]['total'] == 0:
                i += indicator_limit
                continue
            if json[0]['pages'] != 1:
                raise ValueError('Not expecting more than one page!')
            i += indicator_limit



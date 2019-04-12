# -*- coding: utf-8 -*-

# Copyright 2018 IBM.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# =============================================================================

from qiskit.aqua.drivers import BaseDriver, UnitsType
import importlib
from enum import Enum
import logging

logger = logging.getLogger(__name__)


class StockMarket(Enum):
    NASDAQ = 'NASDAQ'
    NYSE = 'NYSE'
    
class DataOnDemandDriver(BaseDriver):
    """Python implementation of an NASDAQ Data on Demand driver."""

    CONFIGURATION = {
        "name": "DOD",
        "description": "NASDAQ Data on Demand Driver",
        "input_schema": {
            "$schema": "http://json-schema.org/schema#",
            "id": "dod_schema",
            "type": "object",
            "properties": {
                STOCKMARKET: {
                    "type": "string",
                    "default": StockMarket.NASDAQ.value,
                    "oneOf": [
                         {"enum": [
                            StockMarket.NASDAQ.value,
                            StockMarket.NYSE.value,
                         ]}
                    ]
                },
                DATATYPE: {
                    "type": "string",
                    "default": DataType.DAILYADJUSTED.value,
                    "oneOf": [
                         {"enum": [
                            DataType.DAILYADJUSTED.value,
                            DataType.DAILY.value,
                            DataType.BID.value,
                            DataType.ASK.value,
                         ]}
                    ]
                },    
            },
        }
    }

    def __init__(self,
                 token,
                 tickers,
                 stockmarket = StockMarket.NASDAQ,
                 start = datetime.datetime(2016,1,1),
                 end = datetime.datetime(2016,1,30)):
        """
        Initializer
        Args:
            token (str): quandl access token
            tickers (str or list): tickers
            stockmarket (StockMarket): LONDON, EURONEXT, or SINGAPORE
        """
        if not isinstance(atoms, list) and not isinstance(atoms, str):
            raise QiskitFinanceError("Invalid atom input for DOD Driver '{}'".format(atoms))

        if isinstance(tickers, list):
            self._tickers = ';'.join(tickers)
        else:
            self._tickers = tickers.replace('\n', ';')
        self._n = len(self._tickers.split(";"))

        self.validate(locals())
        super().__init__()
        self._stockmarket = stockmarket # .value?
        self._token = token
        self._start = start
        self._end = end

    @staticmethod
    def check_driver_valid():
        err_msg = 'quandl is not installed.'
        try:
            spec = importlib.util.find_spec('quandl')
            if spec is not None:
                return
        except Exception as e:
            logger.debug('quandl check error {}'.format(str(e)))
            raise QiskitFinanceError(err_msg) from e

        raise QiskitFinanceError(err_msg)

    @classmethod
    def init_from_input(cls, section):
        """
        Initialize via section dictionary.

        Args:
            params (dict): section dictionary

        Returns:
            Driver: Driver object
        """
        if section is None or not isinstance(section, dict):
            raise QiskitFinanceError('Invalid or missing section {}'.format(section))

        params = section
        kwargs = {}
        #for k, v in params.items():
        #    if k == ExchangeDataDriver. ...: v = UnitsType(v)
        #    kwargs[k] = v
        logger.debug('init_from_input: {}'.format(kwargs))
        return cls(**kwargs)

    def run(self):
        import re
        import urllib
        import urllib2
        import json
        url = 'https://dataondemand.nasdaq.com/api/v1/quotes'
        self._data = []
        for ticker in self._tickers:
          values = {'_Token' : self._token,
          'symbols' : [ticker]
          'start' : start.strftime("%Y-%m-%d'T'%H:%M:%S.%f'Z'") , 
          'end' : end.strftime("%Y-%m-%d'T'%H:%M:%S.%f'Z'") , 
          'next_cursor': 0
          #'start' : start.strftime("%m/%d/%Y %H:%M:%S.%f") , 
          #'end' : end.strftime("%m/%d/%Y %H:%M:%S.%f") , 
          }
          request_parameters = urllib.urlencode(values)
          req = urllib2.Request(url, request_parameters)
          try: 
            response = urllib2.urlopen(req)
            quotes = json.loads(response)["quotes"]
            priceEvolution = []
            for q in quotes: priceEvolution.append(q["ask_price"])
            self._data.append(priceEvolution)
          except:
            raise QiskitFinanceError('Accessing Qiskit failed')

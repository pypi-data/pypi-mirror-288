""" 
Programa : Class Accounts for Canvas
Fecha Creacion : 05/08/2024
Fecha Update : None
Version : 1.0.0
Actualizacion : None
Author : Jaime Gomez
"""

import logging
from .base import BaseCanvas
import pandas as pd

# Create a logger for this module
logger = logging.getLogger(__name__)


class Accounts(BaseCanvas):

    def __init__(self, account_id, access_token):
        super().__init__(access_token)
        # 
        self.account_id = account_id
        # CONNECTOR
        self.url_accounts               = '<path>/accounts/<account_id>'
        self.url_accounts_terms         = '<path>/accounts/<account_id>/terms'
        self.url_accounts_item_term     = '<path>/accounts/<account_id>/terms/<term_id>'
        self.url_accounts_courses       = '<path>/accounts/<account_id>/courses'

    def get_details(self, params = None):
        url = self.url_accounts
        url = url.replace('<account_id>', self.account_id)
        logger.debug(url)
        return self.get(url,params)

    def get_courses(self, params = None):
        url = self.url_accounts_courses
        url = url.replace('<account_id>', self.account_id)
        logger.debug(url)
        return self.get(url,params)

    def get_all_courses(self):
        # Parameters to specify the number of results per page
        params = {
            'per_page': 100  # Maximum allowed per page
        }
        return self.get_courses(params)

    def get_all_courses_by_term_id(self, enrollment_term_id):

        courses = list()

        # Parameters to specify the number of results per page
        params = {
            'per_page': 100 , # Maximum allowed per page
            'enrollment_term_id' : int(enrollment_term_id)
        }

        for course in self.get_courses(params):
            courses.append( { "id" : course["id"] , "name" : course["name"]} )

        return courses


    def get_terms(self, params = None):
        url = self.url_accounts_terms
        url = url.replace('<account_id>', self.account_id)
        logger.info(url)
        return self.get(url,params)

    def get_term(self, term_id, params = None):
        url = self.url_accounts_item_term
        url = url.replace('<account_id>', self.account_id)
        url = url.replace('<term_id>', term_id)
        logger.info(url)
        return self.get(url,params)

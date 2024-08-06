""" 
Programa : Class user for Canvas
Fecha Creacion : 05/08/2024
Fecha Update : None
Version : 1.0.0
Actualizacion : None
Author : Jaime Gomez
"""

import logging
from .base import BaseCanvas

NAME =  'name'
EMAIL = 'email'
TEACHERS = 'teachers'

class Users(BaseCanvas):

    def __init__(self, course_id, access_token):
        super().__init__(access_token)
        # 
        self.course_id = course_id
        # CONNECTOR
        self.url_users       = '<path>/courses/<course_id>/users'

    def get_users(self, params = None):
        url = self.url_users
        url = url.replace('<course_id>', self.course_id)
        return self.get(url,params)

    def get_teachers(self):
        
        teachers = list()
        
        # Parameters to filter by enrollment type 'teacher'
        params = {
            'enrollment_type[]': 'teacher'
        }
        
        for teacher in self.get_users(params):
            teachers.append( { NAME: teacher[NAME], EMAIL : teacher[EMAIL] })

        return teachers

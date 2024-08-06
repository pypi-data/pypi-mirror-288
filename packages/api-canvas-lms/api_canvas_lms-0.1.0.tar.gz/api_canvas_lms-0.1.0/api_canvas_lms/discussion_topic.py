""" 
Programa : Class discussion topic for Canvas
Fecha : 14/04/2024
Version : 1.0.0
Author : Jaime Gomez
"""

from .base import BaseCanvas

class DiscussionTopic(BaseCanvas):
    
    def __init__(self, course_id, access_token):
        super().__init__(access_token)
        # 
        self.course_id = course_id
        # CONNECTOR
        self.url_discussion_topics        = '<path>/courses/<course_id>/discussion_topics'

    def post_item(self, data):
        url = self.url_discussion_topics
        url = url.replace('<course_id>', self.course_id)
        return  self.post(url, data)

    def create_discussion_topic(self, title, message):
        data = {'title'            : title ,
                'message'          : message,
                'discussion_type'  : "threaded",
                'published'        : 'false'}
        return self.post_item(data)

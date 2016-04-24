# -*- coding: utf-8 -*-
# As the article, tag, language_tag are all text based, we use json handlers as a simgle example
import webapp2
import json
import db

# the design priciples, you can see the README.md document in the package folder
class CreateArticleHandler(webapp2.RequestHandler):
    ''' a post handler, receives a json and create an article '''
    def post(self):
        title = self.request.get('title', 'Too lazy, No Title')
        author = self.request.get('author', '')
        article = self.request.get('article','')
        tags = self.request.
    	'tags':['work','travel',],
    	'language_tags':['english','chinese',],
        
class OperateArticleHandler(webapp2.RequestHandler):
    ''' GET, PUT, DELETE handler, modify the article '''
    def get(self, hash_id):
        ''' send back user a json-represented article '''
        pass
    
    def put(self, hash_id):
        ''' modify a field, or fields of an artile '''
        pass
    
    def delete(self, hash_id):
        ''' delete an article '''
        pass
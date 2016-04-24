# -*- coding: utf-8 -*-

from google.appengine.ext import ndb
import hashlib
import datetime
import random

class ArticleTag(ndb.Model):
    ''' A module that represent tags of articles, dont forget tags in your blogs! They are like keywords '''
    tag = ndb.StringProperty(default='') # tag name
    count = ndb.IntegerProperty(default=0) # how many times tag has been refered in article.
    add_date = ndb.DateTimeProperty(auto_now_add=True)
    
    @classmethod
    def query_whole(cls):
        return cls.query().order(-cls.add_date).fetch()


class LanguageTag(ndb.Model):
    ''' A module that represent tags of language '''
    tag = ndb.StringProperty(default='') # tag name
    add_date = ndb.DateTimeProperty(auto_now_add=True)
    
    @classmethod
    def query_whole(cls):
        return cls.query().order(-cls.add_date).fetch()


class Article(ndb.Model):
    ''' A module that represent an article, it shall have:
        title: that will appear on the title bar.
        author: who wrote it, name.
        article: the real article itself, html tags.
        tags: list of text, represents the tags.
        language: list of text, represents what is the language on this page
    '''
    title = ndb.StringProperty(default='') # title of article
    author = ndb.StringProperty(default='') # author of article
    article = ndb.TextProperty(default='') # actual text of article, this is the pure html part.
    tags = ndb.StringProperty(repeated=True) # tags, keywords of an article, a list
    language_tags = ndb.StringProperty(repeated=True) # languages of an article, a list.
    
    public_hash_id = ndb.StringProperty(default='') # a random job id, for marking purpose.
    last_touch_date_str = ndb.StringProperty()
    add_date = ndb.DateTimeProperty(auto_now_add=True)
    
    # Generate a public hash, we don't want to use the urlsafe hash from GAE
    def _pre_put_hook(self):
        m = hashlib.md5()
        factor_one = datetime.datetime.utcnow().strftime('%Y/%m/%d %H:%M:%S')
        factor_two = str(random.getrandbits(128))
        m.update(factor_one)
        m.update(factor_two)
        if not self.public_hash_id: # if the hash is not available
            self.public_hash_id = m.hexdigest()

        self.last_touch_date_str = factor_one
    
    @classmethod
    def query_whole(cls):
        return cls.query().order(-cls.add_date).fetch()
    
    
    @classmethod
    def query_by_page(cls, page_offset, each_page_amount, chrono=False):
        ''' if chronological, from far to near, query a results page by page''' 
        if chrono == True:
            return cls.query().order(cls.target_date).fetch(offset=page_offset,limit=each_page_amount)
            # return from offset, each page result limit.
        else:
            return cls.query().order(-cls.target_date).fetch(offset=page_offset,limit=each_page_amount)
    
    @classmethod
    def query_by_hash(cls, hash_value):
        return cls.query(cls.public_hash_id == hash_value).order(-cls.add_date).fetch()
    
    @classmethod
    def query_by_author(cls, author):
        return cls.query(cls.author == author).order(-cls.add_date).fetch()
    
    @classmethod
    def count_by_author(cls, author):
        return cls.query(cls.author == author).count()
    
    @classmethod
    def query_by_tag(cls, tag):
        return cls.query(cls.tags == tag).order(-cls.add_date).fetch()
    
    @classmethod
    def count_by_tag(cls, tag):
        return cls.query(cls.tags == tag).count()

    @classmethod
    def query_by_language(cls, language):
        return cls.query(cls.language_tags == language).order(-cls.add_date).fetch()
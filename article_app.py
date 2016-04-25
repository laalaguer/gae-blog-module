import webapp2
import os
import jinja2
import article.handlers

jinja_environment = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

# this config is shared accross all the application, so use wisely.
config = {}
config['jinja2_env'] = jinja_environment

app = webapp2.WSGIApplication(routes=[
    webapp2.Route('/article', handler=article.handlers.CreateArticleHandler),
    webapp2.Route('/article/<hash_id>', handler=article.handlers.OperateArticleHandler),
    webapp2.Route('/search_article', handler=article.handlers.SearchArticleByTagHandler),
    webapp2.Route('/tags', handler=article.handlers.ListTagsHandler),
    webapp2.Route('/language_tags', handler=article.handlers.ListLanguageTagsHandler),
], debug=True, config=config)
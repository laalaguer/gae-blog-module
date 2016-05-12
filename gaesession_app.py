import webapp2
import gaesession.handlers

# this config is shared accross all the application, so use wisely.
config = {}
config['webapp2_extras.sessions'] = {
    'secret_key': 'super_super_super_hard_key',
    'cookie_name':'name_i_never_use_cookie',  # this is the default session name/session id
    'cookie_args': {
        'max_age' : 604800 # in seconds, for a week
    }
}

app = webapp2.WSGIApplication(routes=[
    webapp2.Route('/gaesession/', handler=gaesession.handlers.MainHandler),
    webapp2.Route('/gaesessionwith/<photo_key>', handler=gaesession.handlers.MainHandlerWithArguments),
    webapp2.Route('/gaesession/upload', handler='gaesession.handlers.MyUploadHandler:my_post_dispatch'),
    webapp2.Route('/gaesession/download/<photo_key>', handler='gaesession.handlers.ServeBlobHandler:my_get_dispatch'),
], debug=True, config=config)
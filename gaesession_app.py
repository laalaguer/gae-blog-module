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
], debug=True, config=config)
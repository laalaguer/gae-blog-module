import webapp2
from webapp2_extras import sessions

class MainHandler(webapp2.RequestHandler):
    def get(self):
        # Session is stored on both client browser and our database
        session_1 = self.session_store.get_session(name='dbcookie',backend='datastore')
        previous_value_1 = session_1.get("my_attr_name")
        self.response.out.write('on db, ' + str(previous_value_1))
        session_1["my_attr_name"] = "Hi! " + (previous_value_1 if previous_value_1 else "")
        
        self.response.out.write('<br>')
        
        # Session is stored on client browser only
        session_2 = self.session_store.get_session(name='clientcookie')
        previous_value_2 = session_2.get('my_attr_name')
        self.response.out.write('on client browser, ' + str(previous_value_2))
        session_2['my_attr_name'] = "Hi! " + (previous_value_2 if previous_value_2 else "")
        
        self.response.out.write('<br>')
        
        # Session is stored on both client browser and our memcache for fast access
        session_3 = self.session_store.get_session(name='memcachecookie',backend="memcache")
        previous_value_3 = session_3.get('my_attr_name')
        self.response.out.write('on memcache, ' + str(previous_value_3))
        session_3['my_attr_name'] = "Hi! " + (previous_value_3 if previous_value_3 else "")

    # this is needed for webapp2 sessions to work
    def dispatch(self):
        # Get a session store for this request.
        self.session_store = sessions.get_store(request=self.request)
        try:
            webapp2.RequestHandler.dispatch(self)
        finally:
            # Save all sessions.
            self.session_store.save_sessions(self.response)
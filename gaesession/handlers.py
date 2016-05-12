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

class MainHandlerWithArguments(webapp2.RequestHandler):
    def get(self, photo_key): # even with arguments, we call with dispatch(self)
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
            

from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.ext import blobstore

class MyUploadHandler(blobstore_handlers.BlobstoreUploadHandler):
    def my_post_dispatch(self, *args, **kwargs):
        ''' A Fake dispatch method that you want to call inside your Route()
            Just an imitation of the webapp2 style dispatch() with limited functions
        '''
        self.session_store = sessions.get_store(request=self.request)
        try:
            if self.request.method == 'POST':
                self.post(*args, **kwargs) # since webapp doesn't have dispatch() method like webapp2, we do it manually
            else:
                self.error(405)
                self.response.out.write('Method not allowed')
        finally:
            # Save all sessions.
            self.session_store.save_sessions(self.response)
    
    def wrapper(func):
        def dest(self, *args, **kwargs):
            print 'before decorated' # for your future use. you can write wrapper like 'user_required'
            func(self,*args, **kwargs)
            print 'after decorated'
        return dest
    
    @wrapper
    def post(self):
        # Get all the uploaded file info
        myfiles = self.get_uploads('file') # this is a list of blob key info
        
        # You do some operations on the myfiles, maybe transform them
        # maybe associate them with other ndb entities in your database
        # ...
        # But we also want to manipulate with the session, RIGHT ???
        
        
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
        
        
        # Finally, I delete them,just in case you won't let it go.
        [blobstore.delete(each.key()) for each in self.get_uploads('file')]

class ServeBlobHandler(blobstore_handlers.BlobstoreDownloadHandler):
    ''' Serve the images to the public '''
    def my_get_dispatch(self, *args, **kwargs):
        ''' A Fake dispatch method that you want to call inside your Route()
            Just an imitation of the webapp2 style dispatch() with limited functions
        '''
        self.session_store = sessions.get_store(request=self.request)
        try:
            if self.request.method == 'GET':
                self.get(*args, **kwargs) # this is the real get method we want here
            else:
                self.error(405)
                self.response.out.write('Method not allowed')
        finally:
            # Save all sessions.
            self.session_store.save_sessions(self.response)
            
    def wrapper(func):
        def dest(self, *args, **kwargs):
            print 'before decorated' # for your future use. you can write wrapper like 'user_required'
            func(self,*args, **kwargs)
            print 'after decorated'
        return dest
            
    @wrapper
    def get(self, photo_key):
        if not blobstore.get(photo_key):
            self.error(404)
        else:
            self.send_blob(photo_key)
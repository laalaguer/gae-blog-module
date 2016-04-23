import webapp2
import os
import jinja2
import picture.handlers

jinja_environment = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

# this config is shared accross all the application, so use wisely.
config = {}
config['jinja2_env'] = jinja_environment
config['max_upload_size'] = 10
config['blob_process'] = '/pre_receive'
config['blob_serving_url'] = r'/view_photo/'
config['blob_store_final'] = '/blob_store_final'
config['refresh_url'] = '/refresh_url'
config['delete_image_collection'] = '/delete_by_hash/'

app = webapp2.WSGIApplication(routes=[
    webapp2.Route('/dropzone_upload_example', handler=picture.handlers.DropzoneExampleHandler),
    webapp2.Route('/refresh_url', handler=picture.handlers.RefreshUploadUrlHandler),
    webapp2.Route('/pre_receive', handler=picture.handlers.ImagePreProcessHandler),
    webapp2.Route('/blob_store_final', handler=picture.handlers.ImageStoreHandler),
    webapp2.Route('/view_photo/<photo_key>', handler=picture.handlers.ServeBlobHandler),
    webapp2.Route('/delete_by_hash/<public_hash_id>', handler=picture.handlers.DeleteProcessedImageCollectionHandler),
], debug=True, config=config)
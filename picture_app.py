import webapp2
import os
import jinja2
import picture.handlers

jinja_environment = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

# this config is shared accross all the application, so use wisely.
config = {}
config['jinja2_env'] = jinja_environment
config['max_upload_size'] = 10
config['blob_process'] = '/picture/pre_receive'
config['blob_serving_url'] = r'/picture/view_photo/'
config['blob_store_final'] = '/picture/blob_store_final'
config['refresh_url'] = '/picture/refresh_url'
config['delete_image_collection'] = '/picture/delete_by_hash/'

app = webapp2.WSGIApplication(routes=[
    webapp2.Route('/picture/dropzone_upload_example', handler=picture.handlers.DropzoneExampleHandler),
    webapp2.Route('/picture/refresh_url', handler=picture.handlers.RefreshUploadUrlHandler),
    webapp2.Route('/picture/pre_receive', handler=picture.handlers.ImagePreProcessHandler),
    webapp2.Route('/picture/blob_store_final', handler=picture.handlers.ImageStoreHandler),
    webapp2.Route('/picture/view_photo/<photo_key>', handler=picture.handlers.ServeBlobHandler),
    webapp2.Route('/picture/delete_by_hash/<public_hash_id>', handler=picture.handlers.DeleteProcessedImageCollectionHandler),
    webapp2.Route('/picture/update_description/<public_hash_id>', handler=picture.handlers.UpdateProcessedImageDescriptionHandler),
], debug=True, config=config)
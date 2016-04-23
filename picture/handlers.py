from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.ext import blobstore
from google.appengine.api import images
import webapp2
import json
from google.appengine.api import urlfetch
import db


class ServeBlobHandler(blobstore_handlers.BlobstoreDownloadHandler):
    ''' Get and serve the images'''
    def get(self, photo_key):
        if not blobstore.get(photo_key):
            self.error(404)
        else:
            self.send_blob(photo_key)

class RefreshUploadUrlHandler(webapp2.RequestHandler):
    ''' get a refresh uploading url where user can upload a picture
    You can use it inside a <form action="">, or , from a javascript applet
    Return: the uploading url
    '''
    def get(self):
        # Upload of an image url
        upload_url = blobstore.create_upload_url(self.app.config['blob_process'])
        self.response.out.write(upload_url)


class DropzoneExampleHandler(webapp2.RequestHandler):
    ''' Human user upload one image to datastore by drag and drop '''
    def get(self):
        d = {}
        upload_url = blobstore.create_upload_url(self.app.config['blob_process'])
        d['blob_process'] = upload_url
        d['refresh_url'] = self.app.config['refresh_url']
        d['blob_serving_url'] = self.app.config['blob_serving_url']
        d['max_upload_size'] = self.app.config['max_upload_size']
        d['delete_image_collection'] = self.app.config['delete_image_collection']

        # image processed, that already on the server
        d['already_on_server'] = []
        alreay_exist = db.ProcessedImages.query_whole() # a list returned
        for each in alreay_exist:
            d['already_on_server'].append(each.to_dict(exclude=['add_date']))
        
        jinja_environment = self.app.config['jinja2_env']
        template = jinja_environment.get_template('/html/dropzone-upload-example.html')
        self.response.out.write(template.render(d)) # render complete


class ImagePreProcessHandler(blobstore_handlers.BlobstoreUploadHandler):
    ''' gets an image and transform it into largest scale, then call another handler to handle it'''
    @classmethod
    def encode_multipart_formdata(cls, fields, files, mimetype='image/jpeg'):
        """
        Args:
          fields: A sequence of (name, value) elements for regular form fields.
          files: A sequence of (name, filename, value) elements for data to be
            uploaded as files.

        Returns:
          A sequence of (content_type, body) ready for urlfetch.
        """
        boundary = 'paLp12Buasdasd40tcxAp97curasdaSt40bqweastfarcUNIQUE_STRING'
        crlf = '\r\n'
        line = []
        for (key, value) in fields:
            line.append('--' + boundary)
            line.append('Content-Disposition: form-data; name="%s"' % key)
            line.append('')
            line.append(value)
        for (key, filename, value) in files:
            line.append('--' + boundary)
            line.append('Content-Disposition: form-data; name="%s"; filename="%s"' % (key, filename))
            line.append('Content-Type: %s' % mimetype)
            line.append('')
            line.append(value)
        line.append('--%s--' % boundary)
        line.append('')
        body = crlf.join(line)
        content_type = 'multipart/form-data; boundary=%s' % boundary
        return content_type, body

    def post(self):
        # get all the uploaded file info
        myfile = self.get_uploads('file')[0] 
        # 2. get the compressed files as different size
        compressed_file_url_list = [
            images.get_serving_url(myfile.key(), size=1600, crop=False),
            images.get_serving_url(myfile.key(), size=800, crop=False),
            images.get_serving_url(myfile.key(), size=512, crop=True),
            images.get_serving_url(myfile.key(), size=256, crop=True),
        ]

        format_size_list = ['1600','800','512','256']

        response_list = []
        for each_url in compressed_file_url_list:
            response = urlfetch.fetch(
                            url=each_url, # the url
                            method=urlfetch.GET,
                            deadline=30,
                            validate_certificate=False)
            response_list.append(response)

        content_type_str = response_list[0].headers['content-type'] # maybe image/jpeg
        #img_file = response.content # get the image, as a string (note: not a file yet)

        args_list = [ ('file', 'processed_file_'+ y, x.content) for x,y in zip(response_list, format_size_list)]
        # 3. write the picture to blob, again
        # Write new picture to blob
        content_type, body = ImagePreProcessHandler.encode_multipart_formdata(
          [], args_list, content_type_str) #[('file', 'processed_file', img_file)]
        # 4. upload to the image storage handler
        # when success, store a DB storage object that holds these images
        response2 = urlfetch.fetch(
          url=blobstore.create_upload_url(self.app.config['blob_store_final']),
          payload=body,
          method=urlfetch.POST,
          headers={'Content-Type': content_type},
          deadline=30
        )

        if response2.status_code == 200:
            response2_loaded_object = json.loads(response2.content,'utf-8')
            arg_list_db = {
                'blob_256' : None,
                'blob_512' : None,
                'blob_800' : None,
                'blob_1600' : None,
            }
            for each in response2_loaded_object['stored']:
                if '256' in each['filename']:
                    arg_list_db['blob_256'] = blobstore.BlobKey(each['blob_key'])
                if '512' in each['filename']:
                    arg_list_db['blob_512'] = blobstore.BlobKey(each['blob_key'])
                if '800' in each['filename']:
                    arg_list_db['blob_800'] = blobstore.BlobKey(each['blob_key'])
                if '1600' in each['filename']:
                    arg_list_db['blob_1600'] = blobstore.BlobKey(each['blob_key'])

            public_hash_id = db.add_processed_image(**arg_list_db)
            response2_loaded_object['public_hash_id'] = public_hash_id
            self.response.charset = 'utf-8'
            self.response.content_type = response2.headers['content-type']
            self.response.out.write(json.dumps(response2_loaded_object,ensure_ascii=False,indent=2, sort_keys=True).encode('utf-8'))
        

        for each in self.get_uploads('file'):
            blobstore.delete(each.key()) # delete the original file uploaded to blobstore,all of them


class ImageStoreHandler(blobstore_handlers.BlobstoreUploadHandler):
    '''  Store the blob one by one and return the blob key.
        Return: a json, structure like
        {
            'stored':[
                {'blob_key': xxxx, 'filename': xxx,},
                {'blob_key': xxxx, 'filename': xxx,},
                ...
            ]
        }
    '''
    def post(self):
        raw_list = self.get_uploads('file') # get all the files
        d = {}
        d['stored'] = []
        for each in raw_list:
            single_obj = {}
            single_obj['blob_key'] = str(each.key())
            single_obj['filename'] = str(each.filename)
            d['stored'].append(single_obj)

        self.response.charset = 'utf-8'
        self.response.content_type = 'application/json'
        self.response.out.write(json.dumps(d,ensure_ascii=False,indent=2, sort_keys=True).encode('utf-8'))

class DeleteProcessedImageCollectionHandler(webapp2.RequestHandler):
    def get(self, public_hash_id):
        counts = db.delete_processed_image(public_hash_id)
        self.response.out.write(counts)
from google.appengine.ext import ndb
import hashlib
import datetime
import random
from google.appengine.ext import blobstore

class ProcessedImages(ndb.Model):
    ''' A class to get hold of all the processed images that belongs to a single image '''
    public_hash_id = ndb.StringProperty(default='') # a random job id, for marking purpose.

    blob_256 = ndb.BlobKeyProperty()
    blob_512 = ndb.BlobKeyProperty()
    blob_800 = ndb.BlobKeyProperty()
    blob_1600 = ndb.BlobKeyProperty()
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
    def query_by_hash(cls, hash_value):
        return cls.query(cls.public_hash_id == hash_value).order(-cls.add_date).fetch()

    @classmethod
    def query_whole(cls):
        return cls.query().order(-cls.add_date).fetch()

def add_processed_image(blob_256,blob_512,blob_800,blob_1600):
    ''' public method for adding an processed image collection '''
    item = ProcessedImages(blob_256=blob_256,blob_512=blob_512,blob_800=blob_800,blob_1600=blob_1600)
    item_key = item.put()
    return item.public_hash_id # a string

def delete_processed_image(hash_id):
    ''' delete a processed image collection '''
    existing = ProcessedImages.query_by_hash(hash_id)
    length = len(existing)
    for each in existing:
        # delete the blob store key first
        blobstore.delete(each.blob_256)
        blobstore.delete(each.blob_512)
        blobstore.delete(each.blob_800)
        blobstore.delete(each.blob_1600)
        each.key.delete() # delete matching entries.

    return length # return the deleted entries numbers

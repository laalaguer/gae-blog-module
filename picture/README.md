### Folder structure
`db.py` the database, blobstore or NDB store

`handlers.py` the related web handlers to deal around database, CRUD operations via http

### A question about blobstore, blobkey and user behavior

You can notice that, without the blob key, you cannot fetch the blob from store.
So without the blob key, you are going to have no clue about where it is.
As nowadays user prefers to upload the pic, then input some dates and comments about it,

So we have two choices, one is upload the picture alongside the descriptions, this is 
what I called "one-time" uploading. You should think carefully about what info shall 
comes along with the picture(s) and the datastructure shall never change after that.
As the "descriptions+blobs" inside one structure, you have hold the path to the blobs.

As a result, the user shall provide the information all at once when uploading.
Pros: The client side html is simple, just a form.
Cons: The blobs are "private" to each item. You have no way to access it outside the item.

The second choice is uploading the picture(s) and actually return the blob keys via json.
Then the client side javascript application record those blobkeys.
When the user finishes the description(s) as key information of blob, we store the item back in database.
But this again create a risk that the picture maybe orphaned. How do we track it?
And the user input maybe malicious.
Maybe we shall check with the content-type when uploading?
User can provide nothing as the information when uploadin pictures.
The clientside js is a bit complicated.
Pros: The blob is "public" to inside the whole application.
Cons: But we may lose track to each and every blob that we have uploaded.
Solution: we may need to keep a record of "uploaded blobs" and, further more, split the record
into records so we have a improved performance.


### A blog site, a shopping site, not a Dropbox
So this question is easy to answer. The images user upload maybe 3.4Mb but we can only serve the readers
800 per picture for network performance. Either we do it on the clientside in javascript or server side via python.
But, we are not going to keep the original 3.4Mb file as user have uploaded, only the transformed light-weight picture.

However the `file` api of blobstore is deprecated, so it becomes a bit messy how to store your thumbnails back into datastore. I haven't think about a neat solution to it, yet.

Maybe: we upload a blob, then put it on a "pre-process" list. We get to a background jobs. We transform it into 2-3 types of thumbnails. Use a `urlfetch()` method to store thumbnails again into blob store. reuturn the thumbnail keys. Then we get back to cross off those blobs we have transferred and delete them all.


### Another question about thumbnails
The get `get_serving_url()` is not so useful as it can resize the image, but it is a waste of time
doing it over and over again on daily-use images. We have a headline pic and we dont want to transform it
over and over each time a use visits a page. Instead, we want to generate a thumbnail and store it once forall.
### Folder structure

`db.py` all database related about articles

`handlers.py` example web handlers about how to add/remove articles. 

### RESTful API design in http, of articles

The RESTful url match here shall look like: 
```
POST /article 				# create article by post a json, get back article id
GET  /article/<hash_id> 	# read article, get back a json-represented article.
PUT  /article/<hash_id> 	# update article parts, can update parts of article.
DELETE /article/<hash_id> 	# delete article, get back true or false.
```

Design in Details:
```
POST /article
request
{
	'article':{
		'title': 'My Awesome Title',
		'author': 'John Lenen',
		'article': '<html><p></p></html>',
		'tags':['work','travel',],
		'language_tags':['english','chinese',],
	}
	
}
response
{
	'success' : true/false,
	'public_hash_id': 'abc123',
}

```
GET  /article/<hash_id>
response
{
	'success' : true/false,
	'article':{
		'title': 'My Awesome Title',
		'author': 'John Lenen',
		'article': '<html><p></p></html>',
		'tags':['work','travel',],
		'language_tags':['english','chinese',],
		
		'last_touch_date_str': '1989/12/26',
	},
}
```

```
PUT  /article/<hash_id>
request: # these fields can be optional, but the other fileds will be omitted by server.
{
	'title': 'My Awesome Title',
	'author': 'John Lenen',
	'article': '<html><p></p></html>',
	'tags':['work','travel',],
	'language_tags':['english','chinese',],
}

response
{
	'success' : true/false,
	'public_hash_id': 'abc123',
}

```

```
DELETE /article/<hash_id>
response
{
	'success' : true/false,
}

```

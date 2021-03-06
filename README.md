## gae-blog-module
Blog related module on GAE (google app engine), including picture upload, client side javascript, server side, html editor, roles of visitor, admin, tag system, etc.

## modules and design principles

1. Seperation principle: every module shall function and have least relationship with other modules as possible.

2. I want some functionalities out of GAE so I can copy-paste these libraries and use it directly in different projects.

3. These functionalities are supposed to be related to 'blogs' and 'personal website' and 'shops', so I will gradually feed into this collection some functionalities.

## modules
### `picture` module
This module represents a keystone of blog system, pictures.

The module to let user upload pictures by drag and drop. All the pictures are uploaded and transformed into 1600px, 800px, 512px and 256px for web serving. Blog admin can easily refer to a single transformed image via a key. `picture` represents an image resource collection.

### `article` module
This module represents a keystrone of blog system, articles.
Also this module contains other fields like `tag` and `language_tag` data structures.

Unlike usual articles, web blogs are comprised of HTML tags. `article` mainly represents a kind of `text based` objects.
So the functionality will let user insert html articles, view the article on the fly while he/she is typing, and save the article into database

User shall be able to do CRUD(Create, Remove, Update and Delete) functionalities, see the `handlers.py` for more detailed operations.

### `user` module
This module is about the site user roles and their rights to the content. 
Four types:
1. user not logged in,
2. user logged in as common user.
3. user logged in as co-worker (co-author) 
4. user logged in as blog site owner.

They have different powers:

1. Not logged in user can only view public available content, but some actions and content is not visible.
2. Common user allowed to view private available content, but some actions will get 406 not allowed.
3. Co-worker can upload artciles, pictures and view private content.
4. Blog site owner can upload articles, pictures, and also add/remove co-worker in the website.

### `gaesession` module
This is the google app engine session managment module
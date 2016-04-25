# WEB API Restful for `picture` module
This is a after think about the difficulties in reality in Google app engine. But we still need to get out a design documentation for the standard, ideal blog `picture` module. Regardless of the platform or backend we are using.

### Work Flow
A User uploads a bunch of pictures. For each of the picture, we generate some thumbnails to store on the server. And this collection of thumbnails, belongs to a single object and has a description. 
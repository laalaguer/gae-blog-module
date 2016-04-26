# WEB API Restful for `picture` module
This is a after think about the difficulties in reality in Google app engine. But we still need to get out a design documentation for the standard, ideal blog `picture` module. Regardless of the platform or backend we are using.

### Work Flow
A User uploads a bunch of pictures. For each of the picture, we generate some thumbnails to store on the server. And this collection of thumbnails, belongs to a single object and has a description, a date and a privacy trigger called 'public' - if he/she wishes to let the public view it.

A User can upload a picture without description at first, and then update the privacy and description about it.

A User can delete the image on the server.
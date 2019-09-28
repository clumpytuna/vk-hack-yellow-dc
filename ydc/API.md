# Backend API description


### Create dialogue `/create`
#### Request
* POST

#### Response
* Content-type: `application/json`
* Content
    * `id`: Identifier of the created dialogue


### Add a question (request) with text `/request_text`
#### Request
* POST
* Content-type: `multipart/form-data`
    * `id`: Identifier of the dialogue
    * `request`: Request text

#### Response
* HTTP 200


### Add a question (request) with audio `/request_audio`
#### Request
* POST
* Content-type: `multipart/form-data`
    * `id`: Identifier of the dialogue
    * `speech`: Audio file, OGG Vorbis encoded

#### Response
* HTTP 200


### Get response in text format `/response_text`
#### Request
* POST
* Content-type: `multipart/form-data`
    * `id`: Identifier of the dialogue

#### Response
* Content-type: `text/plain`
* Content: Response, enclosed in double brackets (`"this is some response"`)


### Get response in audio format `/response_audio`
#### Request
* POST
* Content-type: `multipart/form-data`
    * `id`: Identifier of the dialogue

#### Response
* Content-type: `audio/ogg`
* Content: Audio file, OGG Vorbis encoded

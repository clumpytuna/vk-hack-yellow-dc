# Backend API description

### Process speech request `/process`
#### Request
* POST
* Content-type: `multipart/form-data`
* Parameters:
    * `speech`: [OGG Vorbis](https://xiph.org/vorbis/) speech record

#### Response
* Content-type: `audio/ogg`
* Binary data (response body): OGG audio file - generated answer

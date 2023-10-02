## Video Manager
This saves videos in the database and relays them

### Endpoints:
---
`/api/video-upload`
- consumes:
  - multipart/form-data
- produces:
  - application/json
- parameters:
  - name: uuid
    ```
      description: ID used to identify the video chunk
      required: true
      type: string
    ```
  - name: chunkindex
    ```
      description: Index signifying end of file (-1)
      required: true
      type: integer
    ```
  - name: video
    ```
      description: Video chunk less than 1MB
      requred: true
      type: file
    ```

- responses:
  - "201": Video complete and created
    ```
    {
      "message": "Video created succesfully",
      "video_id": <id>
    }
    ```
  - "200": Chunk uploaded succesfully
  - "400": Video parameter not found
  - "400": No video selected
  - "400": No UUID or Chunkindex
  - "500": Error writing to disk
    ```
    {
      "message": "Appropiate message"
    }
    ```
---
`/api/videos`
- response:
    - "200": All videos stored on the database
    ```
    {
        "videos": [
            {
                "id": "<id>",
                "uri": "/api/full-video/<id>",
                "transcript": "<transcript>"
            }, ...
        ]
    }
    ```

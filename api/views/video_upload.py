"""Video upload script"""
import os
from pathlib import Path
import shutil
from flask import request, jsonify, current_app, make_response
from werkzeug.utils import secure_filename
from api.views import api_views
from models.video import Video


@api_views.route("/")
def index():
    return """<!doctype html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <link rel="stylesheet"
     href="https://cdnjs.cloudflare.com/ajax/libs/dropzone/5.4.0/min/dropzone.min.css"/>
    <link rel="stylesheet"
     href="https://cdnjs.cloudflare.com/ajax/libs/dropzone/5.4.0/min/basic.min.css"/>
    <script type="application/javascript"
     src="https://cdnjs.cloudflare.com/ajax/libs/dropzone/5.4.0/min/dropzone.min.js">
    </script>
    <title>File Dropper</title>
</head>
<body>
<form method="POST" action='/upload' class="dropzone dz-clickable"
      id="dropper" enctype="multipart/form-data">
</form>

<script type="application/javascript">
    Dropzone.options.dropper = {
        paramName: 'video',
        chunking: true,
        forceChunking: true,
        url: '/video-upload',
        maxFilesize: 1025,
        chunkSize: 1000000
    }
</script>

</body>
</html>"""


@api_views.route("/video-upload", methods=["POST"])
def video_upload():
    """
    swagger_file: video_upload.yml
    """
    if "video" not in request.files:
        return jsonify({"message": "video parameter not found"}), 400
    video = request.files["video"]
    if video.filename == "":
        return jsonify({"message": "No video selected"}), 400
    file_extension = secure_filename(video.filename).split(".")[-1]

    uuid = request.form.get("uuid")
    chunk_idx = int(request.form.get("chunkindex"))
    if None in [uuid, chunk_idx]:
        return jsonify({"message": "No uuid or chunkindex"}), 400

    folder = Path(current_app.config["TEMPORARY_FOLDER"])
    if not os.path.exists(folder):
        os.mkdir(folder)
    filepath = os.path.join(folder, f"{uuid}.{file_extension}")

    try:
        with open(filepath, "ab") as file:
            file.write(video.stream.read())
    except OSError:
        return jsonify({"message": "Error writing file to disk"}), 500

    if chunk_idx == -1:
        perm_folder = Path(current_app.config["PERMANENT_FOLDER"])
        if not os.path.exists(perm_folder):
            os.mkdir(perm_folder)
        perm_filepath = os.path.join(perm_folder,
                                     f"{uuid}.{file_extension}")
        perm_filepath = shutil.copy(filepath, perm_folder)
        os.remove(filepath)
        vid_obj = Video(secure_filename(video.filename),
                        str(perm_filepath))
        vid_obj.save()
        # vid_obj.transcribe()
        return jsonify({"message": "Video created succesfully",
                        "video_id": vid_obj.id}), 201
        # Transciption begins
    return jsonify({"message": "Chunk uploaded"})

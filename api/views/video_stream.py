"""Stream the Video to client"""
import os
from flask import Response, make_response, request
from api.views import api_views
import models
from models.video import Video


def generate_frame(video):
    if not video.videofile:
        video.connect()
    can_display = True
    while can_display:
        frame = video.get_frame()
        if not frame:
            can_display = False
            continue
        yield (b"--frame\r\n"
               b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n")


@api_views.route("/video/<video_id>")
def stream_video(video_id):
    video = models.storage.get(Video, video_id)
    if video:
        return Response(generate_frame(video),
                        mimetype="multipart/x-mixed-replace; boundary=frame")
    return make_response(("Invalid Video ID", 404))


def get_chunk(filename, byte_start: int = None, byte_end: int = None):
    filesize = os.path.getsize(filename)
    yielded = 0
    yield_size = 1024 * 1024

    if byte_start:
        if not byte_end:
            byte_end = filesize
        yielded = byte_start
        filesize = byte_end

    with open(filename, "rb") as file:
        content = file.read()

    while True:
        remainder = filesize - yielded
        if remainder == 0:
            break
        elif remainder >= yield_size:
            yield content[yielded: yielded + yield_size]
            yielded += yield_size
        else:
            yield content[yielded: yielded + remainder]
            yielded += remainder


@api_views.route("/test-video/<video_id>")
def video(video_id):
    video = models.storage.get(Video, video_id)

    if video:
        range = request.headers.get("Range")
        byte_start = None
        byte_end = None
        if range:
            range = range.split("=")[-1]
            start, end = range.split("-")
            if start:
                byte_start = int(start)
            if end:
                byte_end = int(end)

        extension = video.filepath.split(".")[-1]
        response = Response(get_chunk(video.filepath, byte_start, byte_end),
                            mimetype=f"video/{extension}",
                            content_type=f"video/{extension}",
                            direct_passthrough=True)
        return response
    return make_response(("Invalid Video ID", 404))

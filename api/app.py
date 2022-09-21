import os

from flask import Flask, request, render_template, flash
from google.cloud import storage


app = Flask(__name__)
app.config["SECRET_KEY"] = os.urandom(24)

CLOUD_STORAGE_BUCKET = os.environ['CLOUD_STORAGE_BUCKET']


@app.route("/media-upload", methods=["GET", "POST"])
def media_upload():

    if request.method == "POST" and 'document' in request.files:

        uploaded_file = request.files.get('document')

        gcs = storage.Client()

        bucket = gcs.get_bucket(CLOUD_STORAGE_BUCKET)

        blob = bucket.blob(uploaded_file.filename)

        blob.upload_from_string(
            uploaded_file.read(),
            content_type=uploaded_file.content_type
        )

        flash("Document uploaded successfully.")
        return render_template('media-upload-success.html')
    return render_template('media-upload.html')

@app.route("/media-upload-view", methods=["GET"])
def media_upload_view():
    client = storage.Client()
    bucket = client.get_bucket(CLOUD_STORAGE_BUCKET)

    blobs = bucket.list_blobs()

    return render_template('media-view.html', docs=blobs)


if __name__ == "__main__":
    app.run()

import os

from flask import Flask, jsonify, request, render_template, flash
from flask_uploads import DOCUMENTS, UploadSet, configure_uploads
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

documents = UploadSet("documents", DOCUMENTS)
app.config["UPLOADED_DOCUMENTS_DEST"] = "static/documents"
app.config["SECRET_KEY"] = os.urandom(24)
app.config["ALLOWED_EXTENSIONS"] = ["docx", "doc", "pdf"]
app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024  # 10mb
configure_uploads(app, documents)


@app.route("/")
def main():
    return b'{"api-key-version": "0.0.1"}\n'

@app.route("/media-upload", methods=["GET", "POST"])
def media_upload():
    if request.method == "POST" and 'document' in request.files:
        documents.save(request.files['document'])
        flash("Document uploaded successfully.")
        return render_template('media-upload-success.html')
    return render_template('media-upload.html')


if __name__ == "__main__":
    app.run()

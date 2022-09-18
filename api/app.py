from crypt import methods
import os
import sqlite3

from flask import Flask, send_from_directory, request, render_template, flash
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

def get_db_connection():
    conn = sqlite3.connect('docs.db')
    conn.row_factory = sqlite3.Row
    return conn


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

@app.route("/media-upload-view", methods=["GET"])
def media_upload_view():
    conn = get_db_connection()
    docs = conn.execute('SELECT * FROM documents').fetchall()
    conn.close()
    return render_template('media-view.html', docs=docs)

@app.route("/media-upload-download/<file_name>")
def media_upload_download(file_name):
    working_dir = os.path.abspath(os.getcwd())
    file_path = working_dir + '/static/'
    return send_from_directory(file_path, file_name)

if __name__ == "__main__":
    app.run()

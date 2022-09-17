from flask import Flask, jsonify


app = Flask(__name__)


@app.route("/")
def main():
    return b'{"api-key-version": "0.0.1"}\n'


if __name__ == "__main__":
    app.run()

import datetime
from flask import Flask, request, jsonify
from firebase_admin import credentials, firestore, initialize_app, storage


# Initialize Flask App
app = Flask(__name__)


# Initialize Firebase
cred = credentials.Certificate('key.json')
initialize_app(cred, {'storageBucket': 'deltahacks-266217.appspot.com'})
db = firestore.client()
bucket = storage.bucket()


@app.route('/')
def hello():
    """Return a friendly HTTP greeting."""
    return 'Hello World!'


@app.route('/classify_image')
def classify_image():
    name = request.args.get('name')
    if name:
        blob = bucket.blob(name)
        return jsonify({'url': blob.generate_signed_url(datetime.timedelta(seconds=300), method='GET')})

    return jsonify({})


@app.route('/fish')
def fish():
    """Return a friendly HTTP greeting."""
    return get_image('fish.jpeg')


def get_image(name: str):
    blob = bucket.blob(name)
    return blob.generate_signed_url(datetime.timedelta(seconds=300), method='GET')


if __name__ == '__main__':
    # This is used when running locally. Gunicorn is used to run the
    # application on Google App Engine. See entrypoint in app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
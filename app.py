import datetime
from io import BytesIO
import requests
from flask import Flask, request, jsonify
from firebase_admin import credentials, firestore, initialize_app, storage

from fastai.vision import *


# Initialize Flask App
app = Flask(__name__)


# Initialize Firebase
cred = credentials.Certificate('key.json')
initialize_app(cred, {'storageBucket': 'vitae-266301.appspot.com'})
db = firestore.client()
bucket = storage.bucket()

# Initialize classification model
learn = load_learner('models')


@app.route('/')
def hello():
    """Return a friendly HTTP greeting."""
    return 'Hello World!'


@app.route('/classify_image')
def classify_image():
    fn = request.args.get('fn')
    if fn:
        image = get_image(fn)
        prediction = str(learn.predict(image)[0])
        return jsonify({'species': prediction})

    return jsonify({})


def get_image(name: str):
    blob = bucket.blob(name)
    url = blob.generate_signed_url(datetime.timedelta(seconds=300), method='GET')
    response = requests.get(url)
    return open_image(BytesIO(response.content))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)

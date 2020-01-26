import datetime
from io import BytesIO
import requests
from flask import Flask, request, jsonify
from firebase_admin import credentials, firestore, initialize_app, storage
import wikipedia
import fastai.vision as vision


# Initialize Flask App
app = Flask(__name__)


# Initialize Firebase
cred = credentials.Certificate('key.json')
initialize_app(cred, {'storageBucket': 'vitae-266301.appspot.com'})
db = firestore.client()
bucket = storage.bucket()

# Initialize classification model
learn = vision.load_learner('models')


@app.route('/')
def hello():
    """Return a friendly HTTP greeting."""
    return 'Hello World!'


@app.route('/classify_image', methods=["GET"])
def classify_image():
    fn = request.args.get('fn')
    if fn:
        image = get_image(fn)
        prediction = str(learn.predict(image)[0])
        summary = wikipedia.summary(prediction)
        images = wikipedia.page(prediction).images
        image = str(images[0]) if images else "https://www.freeiconspng.com/uploads/no-image-icon-12.jpg"
        return jsonify({'species': prediction, 'summary': summary, 'image': image})

    return jsonify({})


def get_image(name: str):
    blob = bucket.blob(name)
    url = blob.generate_signed_url(datetime.timedelta(seconds=300), method='GET')
    response = requests.get(url)
    return vision.open_image(BytesIO(response.content))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)

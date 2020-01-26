import json
import datetime
from io import BytesIO
import requests
from firebase_admin import credentials, firestore, initialize_app, storage
from google.cloud.firestore_v1 import Increment
import fastai.vision as vision
import wikipedia


# Initialize Firebase
cred = credentials.Certificate('key.json')
initialize_app(cred, {'storageBucket': 'vitae-266301.appspot.com'})
db = firestore.client()
bucket = storage.bucket()

# Initialize classification model
learn = vision.load_learner('models')


with open('models/invasive_species.json') as f:
    invasive_species = json.load(f)


def get_image(name: str):
    blob = bucket.blob(name)
    url = blob.generate_signed_url(datetime.timedelta(seconds=300), method='GET')
    response = requests.get(url)
    return vision.open_image(BytesIO(response.content))


def classify_image(fn, lat, lon, uid):
    image = get_image(fn)
    latin_name, index, tensor = learn.predict(image)
    if float(tensor[index]) >= 0.35:
        latin_name = str(learn.predict(image)[0])
        summary = wikipedia.summary(latin_name, sentences=2)
        wiki_images = wikipedia.page(latin_name).images
        wiki_image = str(wiki_images[0]) if wiki_images else "https://www.freeiconspng.com/uploads/no-image-icon-12.jpg"
        is_invasive = latin_name in invasive_species
        name = invasive_species[latin_name].title() if is_invasive else latin_name
        latin_name = latin_name.title() if is_invasive else ""
        data = {
            "name": name,
            "latin_name": latin_name,
            "bucket_fn": fn,
            "date": datetime.datetime.now(),
            "location": firestore.firestore.GeoPoint(lat, lon),
            "summary": summary,
            "wiki_image": wiki_image,
            "is_invasive": is_invasive
        }

        db.collection(f'users/{uid}/captures').add(data)
        points = 5 if is_invasive else 1
        db.document(f'users/{uid}').set({u'score': Increment(points)}, merge=True)

        return {"name": name, "latin_name": latin_name, "summary": summary,
                "wiki_image": wiki_image, "is_invasive": is_invasive}

    return {"error": "Whoops! We weren't able to classify that image. Please take another one, from a different angle."}


def get_captures(uid):
    docs = db.collection(f'users/{uid}/captures').stream()
    captures = []
    for doc in docs:
        data = doc.to_dict()
        data['location'] = [data['location'].latitude, data['location'].longitude]
        captures.append(data)
    return captures

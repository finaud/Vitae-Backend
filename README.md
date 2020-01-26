# Vitae Backend

## Inspiration
The cost of invasive species in Ontario annually is estimated to be $120 million,
and $30 billion in Canada; in the United States,  $120 billion. Globally, the estimated cost
is $1.4 trillion (roughly 5% of the global economy). Very few of us think about this on
a daily basis, but there are certain demographics that spend a great amount of time 
outside and discovering the world: the children! Why not have them have them collect
invasive species under the guise of a game?

## What It Does
The app provides a fun and interactive game intended to incentivize children to go outside
and explore the nature, all the while collecting data. It allows users to take a photo of 
a wide range of species (plants, animals, fish, etc.), then uses a custom model to classify 
it. The user then receives points for a successful classification (bonus points if the 
species is invasive) and is able to see all of their past "captures" on an interactive map.

## How We Built It
The front-end was developed in Swift, and communicates with the back-end via HTTP requests
and the Google Firebase SDK. The back-end is a Flask server that also contains a custom 
fastai model, trained on over 100 invasive species found in Ontario. All user data is stored
on Google Firebase.

## Challenges We Ran Into
We had many, many issues trying to get the Flask server running on other platforms. We originally
planned to have the back-end hosted on Google Cloud's App Engine; this worked fine until we tried
deploying the model (we tried different workarounds for 5 hours). We then tried DigitalOcean, but
multiple email addresses we used had their accounts automatically locked for some strange reason.
We finally were able to get a DigitalOcean droplet running, but once again were able to deploy 
everything but the model (we figured it was some problem with the fastai library). Next was Heroku;
setup went smoothly, but we were unable to deploy yet again. We finally settled on just running the 
back-end on locally on one of our computers since our time could be used more productively elsewhere.

## Accomplishments That We're Proud Of
We were really proud of our idea and working from scratch. Our classification model was trained
 from scratch, the front-end was done in Swift with few libraries and packages, and the back-end
 was developed with bare-bones Flask and Google Firebase imports. We were also proud of our app
 idea, and thought it could have a real-world impact on the environment and possibly even education 
 (provided we add more features to the app).

## What We learned
On the technical side, this was the first time our mobile developer had integrated a map or camera
functionality into an iOS app. This was also the first time for us to try to host something on 
Google App Engine or Digital Ocean; while it didn't work in the end, we learned a bit about each 
platform and Docker. We also learned about invasive species, and the power of teamwork!

## What's next for Vitae
Our first change would be to host it as a proper instance on a third-party platform so it could
actually be used; this would allow users to begin populating the database. Then end-goal is to have
enough geotagged data to provide research with enough information to get a general sense of where
invasive species are spreading to, and at what rate. We'd also like to train the model on even more
species/images. 
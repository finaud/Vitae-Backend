from flask import Flask, request, jsonify, render_template

import helpers

# Initialize Flask App
app = Flask(__name__)


@app.route('/')
def hello():
    """Return a friendly HTTP greeting."""
    return 'Hello World!'


@app.route('/classify', methods=["GET"])
def classify():
    """Classify an image, given its name in the Firestore bucket."""
    args = request.args
    fn, uid, lat, lon = args.get('fn'), args.get('uid'), float(args.get('lat')), float(args.get('lon'))
    if fn:
        return jsonify(helpers.classify_image(fn, lat, lon, uid))

    return jsonify({})


@app.route('/get_captures', methods=["GET"])
def get_captures():
    """Return a list of species captures a user has taken."""
    uid = request.args.get('uid')
    captures = helpers.get_captures(uid)

    return jsonify(captures)


@app.route('/invasive_map', methods=["GET"])
def invasive_map():
    """Plots all the captures of invasive species."""
    data = helpers.get_all_invasive_captures()
    return render_template('map.html', data=data)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)

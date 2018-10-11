import io
import flask
from PIL import Image
from flask import Flask, request, send_file
import transform_image


app = Flask(__name__)


filters = {
    "sepia": transform_image.sepia,
    "grayscale": transform_image.grayscale,
    "threshold": transform_image.threshold,
    "brightness": transform_image.brightness,
    "negative": transform_image.negative,
    "noises": transform_image.noises,
    "flip_vertical": transform_image.flip_vertical,
    "flip_horizontal": transform_image.flip_horizontal,
    "rotate": transform_image.rotate,
    "crop": transform_image.crop
}


@app.route("/", methods=["GET"])
def index():
    return "I'm alive!"


@app.route('/api', methods=["POST"])
def api():
    image = request.get_data()
    image_filter = request.args.get("filter")
    if image_filter in filters:
        bytes_image = filters[image_filter](image)
        image = Image.open(bytes_image)
        filename = '2.png'
        image.save(filename)
        return send_file(filename, mimetype='image/png')
    else:
        return "Error"


if __name__ == "__main__":
    app.run("localhost", 8000, debug=True)

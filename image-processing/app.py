from flask import Flask, request, send_file, jsonify
import io
from processor import resize_image, crop_image, rotate_image, grayscale_image, flip_image

app = Flask(__name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/process/resize', methods=['POST'])
def resize():
    if 'image' not in request.files:
        return jsonify({"error": "image file required"}), 400
    file = request.files['image']
    width = int(request.form.get('width', 800))
    height = int(request.form.get('height', 600))
    result = resize_image(file.read(), width, height)
    return send_file(io.BytesIO(result), mimetype='image/png')


@app.route('/process/crop', methods=['POST'])
def crop():
    if 'image' not in request.files:
        return jsonify({"error": "image file required"}), 400
    file = request.files['image']
    x = int(request.form.get('x', 0))
    y = int(request.form.get('y', 0))
    width = int(request.form.get('width', 100))
    height = int(request.form.get('height', 100))
    result = crop_image(file.read(), x, y, width, height)
    return send_file(io.BytesIO(result), mimetype='image/png')


@app.route('/process/rotate', methods=['POST'])
def rotate():
    if 'image' not in request.files:
        return jsonify({"error": "image file required"}), 400
    file = request.files['image']
    degrees = int(request.form.get('degrees', 90))
    result = rotate_image(file.read(), degrees)
    return send_file(io.BytesIO(result), mimetype='image/png')


@app.route('/process/grayscale', methods=['POST'])
def grayscale():
    if 'image' not in request.files:
        return jsonify({"error": "image file required"}), 400
    file = request.files['image']
    result = grayscale_image(file.read())
    return send_file(io.BytesIO(result), mimetype='image/png')


@app.route('/process/flip', methods=['POST'])
def flip():
    if 'image' not in request.files:
        return jsonify({"error": "image file required"}), 400
    file = request.files['image']
    direction = request.form.get('direction', 'horizontal')
    result = flip_image(file.read(), direction)
    return send_file(io.BytesIO(result), mimetype='image/png')


if __name__ == '__main__':
    app.run(debug=True, port=5008)

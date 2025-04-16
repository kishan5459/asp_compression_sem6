from flask import Flask, render_template, request, send_file, jsonify
import os
from werkzeug.utils import secure_filename
from utils import compress_image_dct, save_image
import uuid

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/compress', methods=['POST'])
def compress():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400
    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    filename = secure_filename(file.filename)
    input_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(input_path)

    original_size = os.path.getsize(input_path)

    compressed_image = compress_image_dct(input_path)
    output_filename = f'compressed_{uuid.uuid4().hex}.jpg'
    output_path = os.path.join(app.config['UPLOAD_FOLDER'], output_filename)
    save_image(compressed_image, output_path)

    compressed_size = os.path.getsize(output_path)
    compression_ratio = round((1 - compressed_size / original_size) * 100, 2)

    return jsonify({
        'output_file': output_filename,
        'compression_ratio': compression_ratio,
        'compressed_size_kb': round(compressed_size / 1024, 2),
        'original_size_kb': round(original_size / 1024, 2)
    })

@app.route('/download/<filename>')
def download(filename):
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if os.path.exists(filepath):
        response = send_file(filepath, as_attachment=True)
        return response
    return "File not found", 404

if __name__ == '__main__':
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    app.run(debug=True)
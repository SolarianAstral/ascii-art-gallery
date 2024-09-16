from flask import Flask, render_template, request, redirect, url_for, send_file
import os
from ascii_converter import image_to_ascii


# Allowed file extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp', 'bmp',}

app = Flask(__name__)

# Paths of the directories for uploading images and saving ASCII art
UPLOADS_FOLDER = 'static/uploads'
ASCII_ART_FOLDER = 'static/ascii_art'

# Check if both directories exist
os.makedirs(UPLOADS_FOLDER, exist_ok=True)
os.makedirs(ASCII_ART_FOLDER, exist_ok=True)

# Check the extension of the uploaded image


def file_extension_check(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/", methods=['GET', 'POST'])
def index_gallery():
    if request.method == 'POST':
        # Handle file upload
        file = request.files['file']
        if file and file_extension_check(file.filename):
            # Save the uploaded image
            filename = file.filename
            path_image = os.path.join(UPLOADS_FOLDER, filename)
            file.save(path_image)

            # Generate ASCII art and save it as a .jpg file
            path_ascii_image = os.path.join(
                ASCII_ART_FOLDER, f'{os.path.splitext(filename)[0]}.jpg')
            image_to_ascii(path_image, path_ascii_image)

            # Send ASCII art .jpg file to be downloaded
            return send_file(path_ascii_image, as_attachment=True)

    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)

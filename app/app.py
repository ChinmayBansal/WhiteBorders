from flask import Flask, request, flash, redirect, url_for, render_template, send_from_directory
from werkzeug.utils import secure_filename

from image_processing import add_white_borders_to_fit_4_5_aspect_ratio
from dotenv import load_dotenv

load_dotenv()
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['PROCESSED_FOLDER'] = 'processed/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app.secret_key = os.environ.get('SECRET_KEY')


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            # Process the image
            processed_filename = 'processed_' + filename
            processed_filepath = os.path.join(app.config['PROCESSED_FOLDER'], processed_filename)
            add_white_borders_to_fit_4_5_aspect_ratio(filepath, processed_filepath)

            return send_from_directory(app.config['PROCESSED_FOLDER'], processed_filename, as_attachment=True)
    return render_template('upload.html')


if __name__ == '__main__':
    app.run(debug=True)

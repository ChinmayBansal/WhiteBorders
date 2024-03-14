import os
from flask import Flask, request, flash, redirect, render_template, send_file
from werkzeug.utils import secure_filename
from io import BytesIO
from image_processing import add_white_borders_to_fit_4_5_aspect_ratio
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp'}
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
            processed_filename = 'processed_' + filename

            # Create an in-memory byte stream to hold the processed image
            byte_io = BytesIO()
            add_white_borders_to_fit_4_5_aspect_ratio(file, byte_io)
            byte_io.seek(0)

            flash('File has been processed and is ready to download.')
            return send_file(byte_io, as_attachment=True, download_name=processed_filename)

    return render_template('upload.html')

if __name__ == '__main__':
    app.run(debug=True)

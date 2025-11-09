import os
import io
import base64
from flask import Flask, render_template, request, redirect, url_for, flash, send_file
from PIL import Image
import pytesseract

# ======================================================================
# TESSERACT CONFIGURATION
# Update this path if Tesseract is installed elsewhere on your system.
# The path provided by the user is used below.
# ======================================================================
TESSERACT_PATH = r'C:\Users\myatphonesan\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'
try:
    pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH
except Exception:
    # We won't crash on import; the route will show an error if Tesseract is missing
    pass

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET', 'devsecret')


def run_ocr_from_bytes(file_bytes: bytes):
    """Run OCR on raw image bytes and return (text, error_message).

    Returns text (str) and error (None or str).
    """
    try:
        image = Image.open(io.BytesIO(file_bytes))
        # Default to English; change or make configurable if needed
        text = pytesseract.image_to_string(image, lang='eng')
        return text, None
    except pytesseract.TesseractNotFoundError:
        return None, "Tesseract executable not found. Please check the TESSERACT_PATH."
    except Exception as e:
        return None, f"Unexpected error during OCR: {e}"


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        uploaded = request.files.get('file')
        if not uploaded or uploaded.filename == '':
            flash('No file selected', 'warning')
            return redirect(url_for('index'))

        ext = uploaded.filename.rsplit('.', 1)[-1].lower()
        if ext not in ('png', 'jpg', 'jpeg'):
            flash('Unsupported file type. Please upload PNG/JPG/JPEG.', 'danger')
            return redirect(url_for('index'))

        # Read file bytes for both OCR and preview
        file_bytes = uploaded.read()
        extracted_text, error = run_ocr_from_bytes(file_bytes)
        if error:
            flash(error, 'danger')
            return render_template('index.html', tesseract_path=TESSERACT_PATH)

        # Build a data URI to preview the image in the browser
        image_b64 = base64.b64encode(file_bytes).decode('utf-8')
        data_uri = f"data:{uploaded.mimetype};base64,{image_b64}"

        return render_template(
            'index.html',
            extracted_text=extracted_text,
            filename=uploaded.filename,
            image_data=data_uri,
            tesseract_path=TESSERACT_PATH,
        )

    return render_template('index.html', tesseract_path=TESSERACT_PATH)


@app.route('/download', methods=['POST'])
def download():
    text = request.form.get('extracted_text', '')
    filename = request.form.get('filename', 'ocr_result.txt')
    if not text:
        flash('Nothing to download', 'warning')
        return redirect(url_for('index'))

    buf = io.BytesIO(text.encode('utf-8'))
    buf.seek(0)
    # Flask 2.0+ supports `download_name`
    return send_file(buf, as_attachment=True, download_name=filename, mimetype='text/plain')


if __name__ == '__main__':
    # Listening on 127.0.0.1:8501 to be similar to the Streamlit default port used earlier
    app.run(debug=True, host='127.0.0.1', port=8501)

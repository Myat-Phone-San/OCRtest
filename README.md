# Trade Document OCR Scanner (Flask)

This repository contains a small Flask web application that performs OCR on uploaded images using Tesseract via the `pytesseract` Python wrapper.

Files added
- `app.py` - Flask application (upload, OCR, preview, download)
- `templates/index.html` - HTML template for the app
- `requirements.txt` - Python dependencies

Requirements
- Python 3.8+
- Tesseract OCR installed on your machine. On Windows the default installer typically places the executable at:

```
C:\Program Files\Tesseract-OCR\tesseract.exe
```

This project uses the path configured in `app.py`:

```
C:\Users\myatphonesan\AppData\Local\Programs\Tesseract-OCR\tesseract.exe
```

If your Tesseract installation is in a different location, update the `TESSERACT_PATH` variable at the top of `app.py`.

Install dependencies (PowerShell)

```powershell
python -m pip install -r requirements.txt
```

Run the app

```powershell
# Run directly with Python
python .\app.py

# Open http://127.0.0.1:8501 in your browser
```

Notes
- The app accepts PNG/JPG/JPEG images and attempts OCR with the English language model (`lang='eng'`).
- If you get an error saying Tesseract is not found, double-check `TESSERACT_PATH` and ensure Tesseract is installed.
- For production use, don't use `debug=True` and consider running with a proper WSGI server.

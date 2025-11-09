import streamlit as st
from PIL import Image
import pytesseract
import io
import os

# ==============================================================================
# 1. TESSERACT CONFIGURATION (CRITICAL)
# ==============================================================================
# NOTE: This path MUST be updated if Tesseract is moved or installed elsewhere.
# The user provided path is: C:\Users\myatphonesan\AppData\Local\Programs\Tesseract-OCR
TESSERACT_PATH = r'C:\Users\myatphonesan\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'

try:
    # Set the tesseract command location for pytesseract to find the executable
    pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH
except Exception as e:
    st.error(f"Failed to configure Tesseract path: {e}")
    st.warning("Please verify the TESSERACT_PATH variable in the script is correct and Tesseract is installed.")
    st.stop()


# ==============================================================================
# 2. OCR FUNCTION
# ==============================================================================
@st.cache_data
def run_ocr_on_image(image_bytes):
    """
    Performs OCR on an image stream and returns the extracted text.
    """
    try:
        # Open the image from the uploaded bytes
        image = Image.open(io.BytesIO(image_bytes))

        # Use the 'eng' language and 'psm 6' (Assume a single uniform block of text)
        # For trade documents, you might want to try other Paging Segmentation Modes (PSM)
        # like 1, 4, or 3 depending on the layout. PSM 6 is a good default.
        text = pytesseract.image_to_string(image, lang='eng')
        return text, None
    except pytesseract.TesseractNotFoundError:
        return None, "Tesseract executable not found. Please check the path configuration."
    except Exception as e:
        return None, f"An unexpected error occurred during OCR: {e}"


# ==============================================================================
# 3. STREAMLIT APPLICATION
# ==============================================================================
def main():
    st.set_page_config(
        page_title="Trade Document OCR Scanner",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    st.title("📄 Trade Document OCR Scanner")
    st.subheader("Extract text from shipping manifests, invoices, or customs declarations.")

    st.sidebar.header("Configuration")
    st.sidebar.info(
        "Upload a document image (JPEG/PNG) to perform OCR and extract the text content."
    )
    st.sidebar.markdown(f"**Tesseract Path Set To:** \n`{TESSERACT_PATH}`")


    uploaded_file = st.file_uploader(
        "Choose an image file (e.g., Invoice, Bill of Lading)",
        type=['png', 'jpg', 'jpeg']
    )

    if uploaded_file is not None:
        # Display the uploaded image
        col1, col2 = st.columns([1, 1])

        with col1:
            st.markdown("### Uploaded Document Preview")
            # Create a bytes-like object to read the file data
            image_bytes = uploaded_file.read()
            st.image(image_bytes, caption=uploaded_file.name, use_column_width=True)

        with col2:
            st.markdown("### Extracted Text")
            # Run OCR with a loading spinner
            with st.spinner('Processing document and running OCR...'):
                extracted_text, error = run_ocr_on_image(image_bytes)

            if error:
                st.error(error)
            elif extracted_text:
                st.text_area(
                    "OCR Result",
                    extracted_text,
                    height=400,
                    help="This is the raw text extracted by Tesseract OCR. You can copy it for further processing."
                )

                st.download_button(
                    label="Download Extracted Text",
                    data=extracted_text,
                    file_name=f"{os.path.splitext(uploaded_file.name)[0]}_ocr_result.txt",
                    mime="text/plain"
                )
            else:
                st.warning("OCR returned no text. The image might be too blurry or the content is not clear.")

    else:
        st.info("Please upload an image file to begin the OCR process.")


if __name__ == '__main__':
    main()
st.run()
import os
import logging
from io import BytesIO
from fastapi import FastAPI, UploadFile, HTTPException, status
from modal import App, asgi_app, Image, gpu
from pydantic import BaseModel

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define the base image with necessary dependencies and pre-download the YOLOX model
image = (
    Image.debian_slim(python_version="3.11")
    .apt_install(["poppler-utils", "tesseract-ocr", "libgl1-mesa-glx", "libglib2.0-0"])
    .pip_install("unstructured", "unstructured[pdf,local-inference]")
    .run_commands("python -c \"from unstructured_inference.models.base import get_model; get_model('yolox')\"")
)

# Initialize FastAPI and Modal apps
web_app = FastAPI()
app = App('ModalPDFProcessor')

# Pydantic model for response validation
class PDFElement(BaseModel):
    type: str
    text: str = None
    metadata: dict = None
    element_id: str = None

@app.function(image=image, gpu='any', timeout=900)
@web_app.post("/process-pdf/", response_model=list[PDFElement])
async def process_pdf(file: UploadFile):
    try:
        from unstructured.partition.pdf import partition_pdf

        # Read the uploaded file into memory
        pdf_content = await file.read()
        pdf_file = BytesIO(pdf_content)

        # Process the PDF
        elements = partition_pdf(
            file=pdf_file,
            strategy="hi_res",
            infer_table_structure=True,
            extract_images_in_pdf=True,
            hi_res_model_name='yolox',
            max_partition=None
        )

        # Convert elements to dict
        elements_dict = [el.to_dict() for el in elements]

        return elements_dict

    except Exception as e:
        logger.error(f"Error processing PDF: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to process PDF: {str(e)}")

@app.function(image=image, gpu='any', timeout=900)
@asgi_app()
def fastapi_app():
    return web_app

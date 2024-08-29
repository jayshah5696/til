from fastapi import FastAPI, UploadFile, HTTPException
from modal import App, asgi_app, Image, gpu

image = (
    Image.debian_slim(python_version="3.11")
    .apt_install(["poppler-utils", "tesseract-ocr", "libgl1-mesa-glx", "libglib2.0-0"])  # Install required libraries
    .pip_install("unstructured", "unstructured[pdf,local-inference]")
)
# Initialize FastAPI app

web_app = FastAPI()
app = App('Modalapp')

# Set a timeout of 15 minutes (900 seconds) for the FastAPI endpoint
@app.function(image=image, gpu='any', timeout=900)
@web_app.post("/partition-pdf/")
async def partition_pdf_endpoint(file: UploadFile):
    try:
        from unstructured.partition.pdf import partition_pdf
        from io import BytesIO

        # Read the uploaded file into memory
        pdf_content = await file.read()
        pdf_file = BytesIO(pdf_content)

        # Partition the PDF
        elements = partition_pdf(
            file=pdf_file,  # Use 'file' instead of 'pdf_path'
            strategy="hi_res",
            infer_table_structure=True,
            extract_images_in_pdf=True,
            max_partition=None
        )

        # Return the partitioned elements as JSON
        return {"elements": [element.to_dict() for element in elements]}

    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))

# Set a timeout of 15 minutes (900 seconds) for the Modal app function
@app.function(image=image, gpu='any', timeout=900)
@asgi_app()
def my_function():
    return web_app
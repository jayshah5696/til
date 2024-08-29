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



# @app.function(image=Image.from_registry("downloads.unstructured.io/unstructured-io/unstructured:latest"), gpu=gpu.A100())
@app.function(image=image, gpu='any')
@web_app.post("/partition-pdf/")
async def partition_pdf_endpoint(file: UploadFile):
    try:
        from unstructured.partition.pdf import partition_pdf
        from io import BytesIO

        # Read the uploaded file into memory
        pdf_content = await file.read()
        pdf_file = BytesIO(pdf_content)
        # file_location = f"/tmp/{file.filename}"
        # print(file_location)
        # with open(file_location, "wb") as f:
        #     f.write(await file.read())

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

@app.function(image=image,gpu='any')
@asgi_app()
def my_function():
    return web_app
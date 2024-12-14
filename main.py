import os
import uuid
from fastapi import FastAPI, File, UploadFile,  HTTPException
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.post("/upload")
def upload(file: UploadFile = File(...)):
    try:
        extension = file.filename.rsplit(".", 1)[-1]
        filename = f"{uuid.uuid4()}.{extension}"
        with open(os.path.join("static", filename), "wb") as f:
            contents = file.file.read()
            f.write(contents)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="There was a problem")
    finally:
        file.file.close()

    return {"message" : f"Successfully uploaded {file.filename}", "url" : f"/static/{filename}"}
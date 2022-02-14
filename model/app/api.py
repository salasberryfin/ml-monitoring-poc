from fastapi import FastAPI, Response

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "ML Monitoring test model"}


# @app.post("/predict")
# def predict(response: Response, sample):
#     return ""


@app.get("/healthcheck")
async def healthcheck():
    return {"status": "ok"}

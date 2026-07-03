from fastapi import FastAPI

app = FastAPI(title="Smart Task & Analytics API")


@app.get("/")
def root():
    return {"message": "Smart Task & Analytics API is running"}
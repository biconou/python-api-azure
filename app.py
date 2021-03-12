import logging

from fastapi import FastAPI
import uvicorn

app = FastAPI()
logger = logging.getLogger()


@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to this fantastic app!"}
    

@app.get("/customer/{customer_id}")
async def get_customer(customer_id):
    return {"CustomerID": customer_id}


@app.post("/customer/{customer_id}")
async def post_customer(customer_id):
    logger.info("Adding a customer")
    return {"CustomerID": customer_id}

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)

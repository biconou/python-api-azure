from fastapi import FastAPI

app = FastAPI()


@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to this fantastic app!"}

@app.get("/customer/{customer_id}")
async def get_customer(customer_id):
    return {"CustomerID": customer_id}


@app.post("/customer/{customer_id}")
async def post_customer(customer_id):
    return {"CustomerID": customer_id}

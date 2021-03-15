from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder

from app.server.database import (
    add_pschit,
    delete_pschit,
    retrieve_pschit,
    retrieve_pschits,
    update_pschit,
)
from app.server.models.pschit import (
    ErrorResponseModel,
    ResponseModel,
    PschitSchema,
    UpdatePschitModel,
)

router = APIRouter()


@router.post("/", response_description="Pschit data added into the database")
async def add_pschit_data(pschit: PschitSchema = Body(...)):
    pschit = jsonable_encoder(pschit)
    new_pschit = await add_pschit(pschit)
    return ResponseModel(new_pschit, "Pschit added successfully.")


@router.get("/", response_description="Pschits retrieved")
async def get_pschits():
    pschits = await retrieve_pschits()
    if pschits:
        return ResponseModel(pschits, "Pschits data retrieved successfully")
    return ResponseModel(pschits, "Empty list returned")


@router.get("/{id}", response_description="Pschit data retrieved")
async def get_pschit_data(id):
    pschit = await retrieve_pschit(id)
    if pschit:
        return ResponseModel(pschit, "Pschit data retrieved successfully")
    return ErrorResponseModel("An error occurred.", 404, "Pschit doesn't exist.")


@router.put("/{id}")
async def update_pschit_data(id: str, req: UpdatePschitModel = Body(...)):
    req = {k: v for k, v in req.dict().items() if v is not None}
    updated_pschit = await update_pschit(id, req)
    if updated_pschit:
        return ResponseModel(
            "Pschit with ID: {} name update is successful".format(id),
            "Pschit name updated successfully",
        )
    return ErrorResponseModel(
        "An error occurred", 404, "There was an error updating the pschit data."
    )


@router.delete("/{id}", response_description="Pschit data deleted from the database")
async def delete_pschit_data(id: str):
    deleted_pschit = await delete_pschit(id)
    if deleted_pschit:
        return ResponseModel(
            "Pschit with ID: {} removed".format(id), "Pschit deleted successfully"
        )
    return ErrorResponseModel(
        "An error occurred", 404, "Pschit with id {0} doesn't exist".format(id)
    )

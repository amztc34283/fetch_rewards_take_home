from fastapi import FastAPI, HTTPException, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError, ValidationException
from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend
from fastapi_cache.decorator import cache
from fastapi.openapi.docs import get_swagger_ui_html
from contextlib import asynccontextmanager
from uuid import uuid4
from .model import ProcessReceiptResponse, Receipt, GetPointsResponse
from .datastore import DatastoreService
from .processor import calculate_points

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize the cache
    FastAPICache.init(InMemoryBackend())
    # Initialize the datastore
    DatastoreService.get_instance()
    yield
    # Clean up the cache
    FastAPICache.clear()

app = FastAPI(lifespan=lifespan)

@app.get("/receipts/{id}/points", response_model=GetPointsResponse,
        responses={404: {"content": {"application/json": {"example": {"detail": "No receipt found for that id"}}}},
                   422: {"content": {"application/json": {"example": {"detail": [{"loc": ["string", 0], "msg": "string", "type": "string"}]}}}}})
@cache(namespace="receipt", expire=3600)
async def get_points(id: str):
    datastore_service = DatastoreService.get_instance()
    receipt = await datastore_service.get(id)
    if receipt is None:
        raise HTTPException(status_code=404, detail="No receipt found for that id")
    points = await calculate_points(receipt)
    return GetPointsResponse(points=points)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: ValidationException):
    path = request.scope['root_path'] + request.scope['route'].path
    if path == '/receipts/process':
        raise HTTPException(status_code=400, detail='The receipt is invalid')
    else:
        raise HTTPException(status_code=422, detail=exc)

@app.post("/receipts/process", response_model=ProcessReceiptResponse,
        responses={400: {"content": {"application/json": {"example": {"detail": "The receipt is invalid"}}}},
                   422: {"content": {"application/json": {"example": {"detail": [{"loc": ["string", 0], "msg": "string", "type": "string"}]}}}}})
async def process_receipt(receipt: Receipt):
    datastore_service = DatastoreService.get_instance()
    id=str(uuid4())
    while await datastore_service.get(id) is not None: # regenerate id until it doesn't exist
        id=str(uuid4())
    await datastore_service.set(id, jsonable_encoder(receipt))
    return ProcessReceiptResponse(id=id)

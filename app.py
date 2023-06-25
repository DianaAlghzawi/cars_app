from fastapi import FastAPI, Request, status
from cars.controllors.owners_controller import owner_router
from cars.controllors.cars_cotroller import cars_router
from cars.exception import ModelFoundException, ValidatorException, ModelNotFoundException
from fastapi.responses import JSONResponse

app = FastAPI()

app.include_router(owner_router)
app.include_router(cars_router)


@app.exception_handler(ModelNotFoundException)
async def unicorn_not_found_exception_handler(request: Request, exc: ModelNotFoundException):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"error": exc.content},
    )


@app.exception_handler(ModelFoundException)
async def unicorn_found_exception_handler(request: Request, exc: ModelFoundException) -> JSONResponse:
    return JSONResponse(content={"error": exc.message}, status_code=status.HTTP_409_CONFLICT)


@app.exception_handler(ValidatorException)
async def unicorn_invalid_validator(request: Request, exc: ValidatorException) -> JSONResponse:
    return JSONResponse(content={"error": exc.message}, status_code=status.HTTP_400_BAD_REQUEST)

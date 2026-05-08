from fastapi import FastAPI, Request
from database.database import Base, engine
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from routes import users, tasks

# Create all database tables automatically
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Task Management API",
    description="A simple Task Management REST API with JWT Authentication",
    version="1.0.0"
)

# Connect all routes
app.include_router(users.router)
app.include_router(tasks.router)


# Clean validation error messages
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = exc.errors()
    first_error = errors[0]
    message = first_error["msg"].replace("Value error, ", "")
    return JSONResponse(
        status_code=422,
        content={"detail": message}
    )

@app.get("/")
def root():
    return {"message": "Task Management API is running!"}

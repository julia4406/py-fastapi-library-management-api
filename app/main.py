from fastapi import FastAPI

app = FastAPI(
    title="Library management"
)

app.include_router(...)

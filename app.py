from fastapi import FastAPI, HTTPException
from starlette.staticfiles import StaticFiles

from api import api_router
from templates import templates_router, templates

app = FastAPI()
app.mount('/assets', app=StaticFiles(directory='assets'), name='assets')
app.include_router(api_router)
app.include_router(templates_router)


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    if exc.status_code == 404:
        return templates.TemplateResponse("404.html", {"request": request})

import secure
import uvicorn
import crud
import rest_api
from contextlib import asynccontextmanager
from config import settings
from db import create_tables
from dependencies import get_engine
from fastapi import Depends, FastAPI, Request, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.exceptions import HTTPException as StarletteHTTPException
from sqlmodel import create_engine, Session
from sqlalchemy.engine.base import Engine
from typing import Annotated

@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup behavior: this code runs when app is created
    # create database engine singleton
    engine = create_engine(settings.database_url, echo=True)
    app.state.engine = engine
    create_tables(engine)
    yield
    # shutdown behavior: this code runs when app is deleted
    # do not need to close the engine connection


app = FastAPI(openapi_url=None, lifespan=lifespan)
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

csp = secure.ContentSecurityPolicy().default_src("'self'").frame_ancestors("'none'")
hsts = secure.StrictTransportSecurity().max_age(31536000).include_subdomains()
referrer = secure.ReferrerPolicy().no_referrer()
cache_value = secure.CacheControl().no_cache().no_store().max_age(0).must_revalidate()
x_frame_options = secure.XFrameOptions().deny()

secure_headers = secure.Secure(
    csp=csp,
    hsts=hsts,
    referrer=referrer,
    cache=cache_value,
    xfo=x_frame_options,
)


@app.middleware("http")
async def set_secure_headers(request, call_next):
    response = await call_next(request)
    secure_headers.framework.fastapi(response)
    return response


app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.client_origin_url],
    allow_methods=["GET"],
    allow_headers=["Authorization", "Content-Type"],
    max_age=86400,
)


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    message = str(exc.detail)

    return JSONResponse({"message": message}, status_code=exc.status_code)


# Include /api routes
app.include_router(rest_api.router, prefix="/api")


@app.get("/", response_class=HTMLResponse)
def homepage(request: Request, engine: Engine = Depends(get_engine)):
    with Session(engine) as session:
        ski_passes = crud.read_all_ski_passes(session)
    return templates.TemplateResponse(
        name="index.html", context={"request": request, "message": "Ski Club Manager", "ski_passes": ski_passes}
    )


@app.get("/reservation", response_class=HTMLResponse)
def reservation_page(request: Request):
    return templates.TemplateResponse(
        name="reservation.html", context={"request": request}
    )


@app.get("/manage", response_class=HTMLResponse)
def manage_page(request: Request, engine: Engine = Depends(get_engine)):
    with Session(engine) as session:
        ski_passes = crud.read_all_ski_passes(session)
    return templates.TemplateResponse(
        name="manage.html", context={"request": request, "ski_passes": ski_passes}
    )


@app.post("/manage/add", response_class=HTMLResponse)
def manage_page_add(serial_number: Annotated[str, Form()], request: Request, engine: Engine = Depends(get_engine)):
    with Session(engine) as session:
        crud.create_ski_pass(session, serial_number)
        session.commit()
        ski_passes = crud.read_all_ski_passes(session)
    return templates.TemplateResponse(
        name="manage.html", context={"request": request, "ski_passes": ski_passes}
    )


@app.post("/manage/invalidate/{serial_number}", response_class=HTMLResponse)
def manage_page_invalidate(serial_number: str, request: Request, engine: Engine = Depends(get_engine)):
    with Session(engine) as session:
        crud.invalidate_ski_pass(session, serial_number)
        session.commit()
        ski_passes = crud.read_all_ski_passes(session)
    return templates.TemplateResponse(
        name="manage.html", context={"request": request, "ski_passes": ski_passes}
    )


@app.post("/manage/delete/{serial_number}", response_class=HTMLResponse)
def manage_page_delete(serial_number: str, request: Request, engine: Engine = Depends(get_engine)):
    with Session(engine) as session:
        crud.delete_ski_pass(session, serial_number)
        session.commit()
        ski_passes = crud.read_all_ski_passes(session)
    return templates.TemplateResponse(
        name="manage.html", context={"request": request, "ski_passes": ski_passes}
    )


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=settings.port,
        reload=settings.reload,
        server_header=False,
    )

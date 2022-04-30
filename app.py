from datetime import datetime, timedelta
import typing as t

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from piccolo_admin.endpoints import create_admin
from piccolo_api.crud.serializers import create_pydantic_model
from piccolo.engine import engine_finder
from starlette.routing import Route, Mount
from starlette.staticfiles import StaticFiles

from dhrift.endpoints import HomeEndpoint
from dhrift.piccolo_app import APP_CONFIG
from dhrift.tables import DrifttUser, Site, Resource
from dhrift.tables import ResourceType

from metadata import title, description, tags
from security import (
    hash,
    Token,
    authenticate_user,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    AuthCredentials,
    create_access_token,
)


app = FastAPI(
    title=title,
    description=description,
    openapi_tags=tags,
    routes=[
        Route("/", HomeEndpoint),
        Mount(
            "/admin/",
            create_admin(
                tables=APP_CONFIG.table_classes,
                # Required when running under HTTPS:
                # allowed_hosts=['my_site.com']
            ),
        ),
        Mount("/static/", StaticFiles(directory="static")),
    ],
)


@app.post("/token", response_model=Token, tags=["users"])
async def login_for_access_token(form_data: AuthCredentials = Depends()):

    user = await authenticate_user(
        form_data.username, form_data.password.get_secret_value()
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["username"]}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


DrifttUserIn: t.Any = create_pydantic_model(
    table=DrifttUser,
    model_name="DrifttUserIn",
    exclude_columns=(DrifttUser.last_modified,),
)
DrifttUserOut: t.Any = create_pydantic_model(
    table=DrifttUser, include_default_columns=True, model_name="DrifttUserOut"
)

SiteIn: t.Any = create_pydantic_model(
    table=Site,
    model_name="SiteIn",
    exclude_columns=(
        Site.created,
        Site.last_modified,
    ),
)
SiteOut: t.Any = create_pydantic_model(
    table=Site, include_default_columns=True, model_name="SiteOut"
)


ResourceIn: t.Any = create_pydantic_model(
    table=Resource,
    model_name="ResourceIn",
    exclude_columns=(
        Resource.created,
        Resource.last_modified,
    ),
)

ResourceOut: t.Any = create_pydantic_model(
    table=Resource, include_default_columns=True, model_name="ResourceOut"
)


# The create_pydantic_model function messes up some of the schemas
# Seehttps://github.com/piccolo-orm/piccolo/issues/467
class ResourceInExtended(ResourceIn):
    type: ResourceType


@app.get("/users/", response_model=t.List[DrifttUserOut], tags=["users"])
async def users():
    return await DrifttUser.select().order_by(DrifttUser.id)


@app.post("/users/", response_model=DrifttUserOut, tags=["users"])
async def create_user(user_model: DrifttUserIn):

    user_model.password = hash(user_model.password)

    user = DrifttUser(**user_model.dict())

    await user.save()
    return user.to_dict()


@app.put("/users/{user_id}/", response_model=DrifttUserOut, tags=["users"])
async def update_user(user_id: int, user_model: DrifttUserIn):
    user = await DrifttUser.objects().get(DrifttUser.id == user_id)
    if not user:
        return JSONResponse({}, status_code=404)

    for key, value in user_model.dict().items():
        setattr(user, key, value)

    await user.save()

    return user.to_dict()


@app.delete("/users/{user_id}/", tags=["users"])
async def delete_user(user_id: int):
    user = await DrifttUser.objects().get(DrifttUser.id == user_id)
    if not user:
        return JSONResponse({}, status_code=404)

    await user.remove()

    return JSONResponse({})


## Site schema


@app.get("/sites/", response_model=t.List[SiteOut], tags=["sites"])
async def sites():
    return await Site.select().order_by(Site.id)


@app.post("/sites/", response_model=SiteOut, tags=["sites"])
async def create_site(site_model: SiteIn):

    site = Site(**site_model.dict())
    await site.save()
    return site.to_dict()


@app.put("/sites/{site_id}/", response_model=SiteOut, tags=["sites"])
async def update_site(site_id: int, site_model: SiteIn):
    site = await Site.objects().get(Site.id == site_id)
    if not site:
        return JSONResponse({}, status_code=404)

    for key, value in site_model.dict().items():
        setattr(site, key, value)

    await site.save()

    return site.to_dict()


@app.delete("/sites/{site_id}/", tags=["sites"])
async def delete_site(site_id: int):
    site = await Site.objects().get(Site.id == site_id)
    if not site:
        return JSONResponse({}, status_code=404)

    await site.remove()

    return JSONResponse({})


# Resource schema


@app.get("/resources/", response_model=t.List[ResourceOut], tags=["resources"])
async def resources():
    return await Resource.select().order_by(Resource.id)


@app.post("/resources/", response_model=ResourceOut, tags=["resources"])
async def create_resource(resource_model: ResourceInExtended):

    resource = Resource(**resource_model.dict())
    await resource.save()
    return resource.to_dict()


@app.put("/resources/{resource_id}/", response_model=ResourceOut, tags=["resources"])
async def update_resource(resource_id: int, resource_model: ResourceInExtended):
    resource = await Resource.objects().get(Resource.id == resource_id)
    if not resource:
        return JSONResponse({}, status_code=404)

    for key, value in resource_model.dict().items():
        setattr(resource, key, value)

    await resource.save()

    return resource.to_dict()


@app.delete("/resources/{resource_id}/", tags=["resources"])
async def delete_resource(resource_id: int):
    resource = await Resource.objects().get(Resource.id == resource_id)
    if not resource:
        return JSONResponse({}, status_code=404)

    await resource.remove()

    return JSONResponse({})


@app.on_event("startup")
async def open_database_connection_pool():
    try:
        engine = engine_finder()
        await engine.start_connection_pool()
    except Exception:
        print("Unable to connect to the database")


@app.on_event("shutdown")
async def close_database_connection_pool():
    try:
        engine = engine_finder()
        await engine.close_connection_pool()
    except Exception:
        print("Unable to connect to the database")

# project/app/main.py


from enum import IntEnum
from fastapi import FastAPI, Depends
import os
from tortoise.contrib.fastapi import register_tortoise
import pathlib
from app.config import get_settings, Settings


app = FastAPI()

register_tortoise(
    app,
    db_url=os.environ.get("DATABASE_URL"),
    modules={"models": ["app.models.tortoise"]},
    generate_schemas=False,  # updated
    add_exception_handlers=True,
)


def funcion_tree(path, file, tree, complete_path):
    if file != '': path = os.path.join(path, file)
    if os.path.isdir(path):
        mapa = {}
        if (complete_path): tree[str(path)] = mapa
        else: tree[os.path.basename(path)] = mapa
        for value in os.listdir(path): funcion_tree(path, value, mapa, complete_path)    
    else:
        if (complete_path): tree[str(path)] = None
        else: tree[os.path.basename(path)] = None


@app.get("/ping")
async def pong(settings: Settings = Depends(get_settings)):
    dir_app = pathlib.Path(__file__).parent.parent.absolute()
    mapa = {}
    funcion_tree(dir_app, '', mapa, False)

    return {
        "ping": "pong!",
        "environment": settings.environment,
        "testing": settings.testing,
        # "path_app": dir_app,
        # 'mapa': mapa,
        # "DATABASE_URL": os.environ.get("DATABASE_URL")
    }

    


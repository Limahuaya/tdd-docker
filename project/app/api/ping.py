#project/app/api/ping.py
 
import os
from fastapi import APIRouter, Depends
 
from app.config import get_settings, Settings
import pathlib
 
router = APIRouter()
 
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


 
@router.get("/ping")
async def pong(settings: Settings = Depends(get_settings)):
    dir_app = pathlib.Path(__file__).parent.parent.parent.absolute()
    mapa = {}
    funcion_tree(dir_app, '', mapa, False)

    return {
        "ping": "pong!",
        "environment": settings.environment,
        "testing": settings.testing,
        # "path_app": dir_app,
        'estructural del proyecto': mapa,
        # "DATABASE_URL": os.environ.get("DATABASE_URL")
    }
    
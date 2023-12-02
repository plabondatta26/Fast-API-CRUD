from fastapi import FastAPI
from core.database import engine
import os
from importlib import import_module


class Routes:
    app = FastAPI()

    # register controller dynamically
    controller_files = os.listdir('controller')
    controller_files = [file for file in controller_files if file not in ['__init__.py', '__pycache__']]
    for controller_file in controller_files:
        controller_module = import_module(f"controller.{controller_file.split('.')[0]}")
        app.include_router(controller_module.router)

    # register model dynamically
    model_files = os.listdir('models')
    model_files = [file for file in model_files if file not in ['__init__.py', '__pycache__']]
    for model_file in model_files:
        model = import_module(f"models.{model_file.split('.')[0]}")
        model.Base.metadata.create_all(bind=engine)

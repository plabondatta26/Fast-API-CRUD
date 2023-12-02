from fastapi import FastAPI
from config.router import Routes

import uvicorn

if __name__ == '__main__':
    uvicorn.run(Routes.app, host="127.0.0.1", port=8000)

import uvicorn

from config.utils import HOST, PORT, RELOAD, WORKERS

if __name__ == "__main__":
    uvicorn.run("main_router:app", host=HOST, port=int(PORT),
                reload=RELOAD, workers=int(WORKERS))
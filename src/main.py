from fastapi import FastAPI

import uvicorn

from api import main_router


app = FastAPI()



        
app.include_router(main_router)


def main():
    uvicorn.run("main:app", reload=True)


if __name__ == "__main__":
    main()

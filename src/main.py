import sys

from fastapi import FastAPI
import uvicorn
from pathlib import Path

from api import main_router



sys.path.append(str(Path(__file__).parent))

app = FastAPI()

        
app.include_router(main_router)


def main():
    uvicorn.run("main:app", reload=True)


if __name__ == "__main__":
    main()

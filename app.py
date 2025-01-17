import os
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
import uvicorn
from database.connection import init_db
from routes import public
from routes import secure

load_dotenv()

app = FastAPI()


@app.on_event("startup")
async def startup_event():
    print("Project Startup", flush=True)
    await init_db()


app.include_router(public.router)
app.include_router(secure.router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("SERVER_PORT", 8000)))

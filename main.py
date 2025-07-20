import os
import uvicorn
from fastapi import FastAPI
from src.controllers import userTypeController, userController

app = FastAPI(debug=True)

app.include_router(userTypeController.router)
app.include_router(userController.router)

if __name__ == "__main__":
    uvicorn.run(
        "main:app", host="0.0.0.0", port=int(os.getenv("PORT", 8000)), reload=True
    )

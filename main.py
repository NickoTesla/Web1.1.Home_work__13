from fastapi import FastAPI, Depends, HTTPException, BackgroundTasks
from sqlalchemy import text
from sqlalchemy.orm import Session
import uvicorn
from src.database.db import get_db
from src.routes import contacts, auth
from pathlib import Path
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from pydantic import EmailStr, BaseModel
from typing import List
import redis.asyncio as redis
from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter
from src.conf.config import settings


app = FastAPI()


@app.get("/api/healthchecker")
def healthchecker(db: Session = Depends(get_db)):
    try:
        # Make request
        result = db.execute(text("SELECT 1")).fetchone()
        if result is None:
            raise HTTPException(status_code=500, detail="Database is not configured correctly")
        return {"message": "Welcome to FastAPI!"}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Error connecting to the database")

# below newly pasted

# @app.post("/send-email")
# async def send_in_background(background_tasks: BackgroundTasks, body: EmailSchema):
#     message = MessageSchema(
#         subject="Fastapi mail module",
#         recipients=[body.email],
#         template_body={"fullname": "Billy Jones"},
#         subtype=MessageType.html
#     )

#     fm = FastMail(conf)

#     background_tasks.add_task(fm.send_message, message, template_name="example_email.html")

#     return {"message": "email has been sent"}


@app.on_event("startup")
async def startup():
    r = await redis.Redis(host=settings.redis_host, port=settings.redis_port, db=0, encoding="utf-8",
                          decode_responses=True)
    await FastAPILimiter.init(r)

@app.get("/", dependencies=[Depends(RateLimiter(times=2, seconds=5))])
def read_root():
    return {"message": "Hello World"}




app.include_router(auth.router, prefix='/api')
app.include_router(contacts.router, prefix='/api')
# app.include_router(users.router, prefix='/api')

if __name__ == '__main__':
    uvicorn.run('main:app', port=8000, reload=True)

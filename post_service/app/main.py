from fastapi import FastAPI, HTTPException, Depends, Header
from sqlalchemy.orm import Session
from . import models, schemas, database
from jose import JWTError, jwt
import os

app = FastAPI()

database.Base.metadata.create_all(bind=database.engine)

SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey")
ALGORITHM = "HS256"


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")
        if user_id is None:
            raise JWTError
        return user_id
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except JWTError:
        raise HTTPException(status_code=400, detail="Invalid token")


@app.post("/message", status_code=201)
def create_message(
        message_data: schemas.MessageCreate,
        authorization: str = Header(...),
        db: Session = Depends(get_db)
):
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=400, detail="Invalid authorization header")

    token = authorization.split(" ")[1]

    user_id = verify_token(token)

    new_message = models.Message(user_id=user_id, message=message_data.message)
    db.add(new_message)
    db.commit()
    return {}
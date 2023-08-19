import redis
import json
import uvicorn
import pickle

from fastapi import FastAPI

app = FastAPI()
# Connecting to Redis
r = redis.Redis(host='localhost', port=6379, db=0)

database = {
    "10": 10,
    "11": 11,
    "12": 12
}


@app.get("/product/{product_id}")
def read_product(product_id: int):
    product = r.get(str(product_id))
    if product is None:
        product = fetch_product_from_db(product_id)
        r.set(str(product_id), json.dumps(product))
        r.expire(str(product_id), 3600)
        return product
    return json.loads(product)


def fetch_product_from_db(product_id: int):
    data = database.get(str(product_id), None)
    print(data)
    return data

class Auth:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    SECRET_KEY = "secret_key"
    ALGORITHM = "HS256"
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")
    r = redis.Redis(host='localhost', port=6379, db=0)

async def get_current_user(self, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

        try:
            # Decode JWT
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
            if payload['scope'] == 'access_token':
                email = payload["sub"]
                if email is None:
                    raise credentials_exception
            else:
                raise credentials_exception
        except JWTError as e:
            raise credentials_exception
        user = self.r.get(f"user:{email}")
        if user is None:
            user = await repository_users.get_user_by_email(email, db)
            if user is None:
                raise credentials_exception
            self.r.set(f"user:{email}", pickle.dumps(user))
            self.r.expire(f"user:{email}", 900)
        else:
            user = pickle.loads(user)
        return user
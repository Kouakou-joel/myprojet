from fastapi import FastAPI, Depends
from database import engine
from models import Base
from crud import auth, taches, user
from middleware import LoggingMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm


app = FastAPI()

app.add_middleware(LoggingMiddleware)

# Ajout de la sécurité
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    return {"access_token": form_data.username, "token_type": "Basic"}

# # Création des tables au démarrage
# @app.on_event("startup")
# async def startup():
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)

@app.get("/")
def read_home():
    return {"message": "Bienvenue sur votre TODO app ! "}


# Inclusion des routes
app.include_router(auth.router, prefix="/auth", tags=["Authentification"])
app.include_router(taches.router, prefix="/api", tags=["Tâches"])
app.include_router(user.router, prefix="/api", tags=["Users"])




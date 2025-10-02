# Ensure runtime patches are applied before importing FastAPI and its
# dependencies. This prevents issues with Python 3.13 and older Pydantic
# releases that FastAPI still depends on.
from . import pycompat  # noqa: F401

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .ollama import router as ollama_router
from .auth import authenticate_user, create_access_token, get_current_active_user
from .database import Base, engine, get_db

VERSION = "1.0.2"

print(f"VERSION = {VERSION}")

_ = models  # ensure models are imported for metadata creation

Base.metadata.create_all(bind=engine)

app = FastAPI(title="FastAPI + Svelte Tutorial")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(ollama_router)


@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI + Svelte tutorial API"}


@app.post("/auth/register", response_model=schemas.UserRead, status_code=status.HTTP_201_CREATED)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    existing = crud.get_user_by_email(db, email=user.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    return crud.create_user(db, user)


@app.post("/auth/token", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.email})
    return schemas.Token(access_token=access_token)


@app.get("/users/me", response_model=schemas.UserRead)
async def read_users_me(current_user=Depends(get_current_active_user)):
    return current_user


@app.get("/items", response_model=schemas.PaginatedItems)
async def read_items(
    skip: int = 0,
    limit: int = 20,
    current_user=Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    items, total = crud.list_items(db, owner_id=current_user.id, skip=skip, limit=limit)
    return {"items": items, "total": total}


@app.post("/items", response_model=schemas.ItemRead, status_code=status.HTTP_201_CREATED)
async def create_item(
    item: schemas.ItemCreate,
    current_user=Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    return crud.create_item(db, item=item, owner_id=current_user.id)


@app.put("/items/{item_id}", response_model=schemas.ItemRead)
async def update_item(
    item_id: int,
    item: schemas.ItemUpdate,
    current_user=Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    db_item = crud.update_item(db, item_id=item_id, item=item, owner_id=current_user.id)
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item


@app.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(
    item_id: int,
    current_user=Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    deleted = crud.delete_item(db, item_id=item_id, owner_id=current_user.id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Item not found")
    return None

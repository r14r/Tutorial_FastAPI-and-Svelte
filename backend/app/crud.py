from typing import List, Optional, Tuple

from sqlalchemy.orm import Session

from . import models, schemas
from .auth import get_password_hash


def get_user(db: Session, user_id: int) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.email == email).first()


def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    print(__file__, "password=", user.password)
    
    hashed_password = get_password_hash(user.password)
    db_user = models.User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def list_items(db: Session, owner_id: int, skip: int = 0, limit: int = 20) -> Tuple[List[models.Item], int]:
    query = db.query(models.Item).filter(models.Item.owner_id == owner_id)
    total = query.count()
    items = query.offset(skip).limit(limit).all()
    return items, total


def create_item(db: Session, item: schemas.ItemCreate, owner_id: int) -> models.Item:
    db_item = models.Item(**item.model_dump(), owner_id=owner_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def update_item(db: Session, item_id: int, item: schemas.ItemUpdate, owner_id: int) -> Optional[models.Item]:
    db_item = (
        db.query(models.Item)
        .filter(models.Item.id == item_id, models.Item.owner_id == owner_id)
        .first()
    )
    if not db_item:
        return None
    for key, value in item.model_dump(exclude_unset=True).items():
        setattr(db_item, key, value)
    db.commit()
    db.refresh(db_item)
    return db_item


def delete_item(db: Session, item_id: int, owner_id: int) -> bool:
    deleted = (
        db.query(models.Item)
        .filter(models.Item.id == item_id, models.Item.owner_id == owner_id)
        .delete()
    )
    db.commit()
    return bool(deleted)

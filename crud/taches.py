from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models import Tache, User
from schemas.tache import TacheCreate, TacheResponse
from database import get_db
from crud.auth import get_current_active_user
from typing import List

router = APIRouter()

# Créer une tâche
@router.post("/taches/", response_model=TacheResponse, status_code=status.HTTP_201_CREATED)
async def create_tache(
    tache: TacheCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    new_tache = Tache(title=tache.title, description=tache.description, owner_id=current_user.id)
    db.add(new_tache)
    await db.commit()
    await db.refresh(new_tache)
    return new_tache

# Récupérer toutes les tâches de l'utilisateur connecté
@router.get("/taches/", response_model=List[TacheResponse])
async def get_my_taches(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    result = await db.execute(select(Tache).filter(Tache.owner_id == current_user.id))
    return result.scalars().all()

# Mettre à jour une tâche
@router.put("/taches/{tache_id}", response_model=TacheResponse, status_code=status.HTTP_200_OK)
async def update_tache(
    tache_id: int,
    tache: TacheCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    result = await db.execute(select(Tache).filter(Tache.id == tache_id, Tache.owner_id == current_user.id))
    db_tache = result.scalars().first()

    if not db_tache:
        raise HTTPException(status_code=404, detail="Tâche non trouvée ou non autorisée")

    db_tache.title = tache.title
    db_tache.description = tache.description
    await db.commit()
    await db.refresh(db_tache)

    return db_tache

# Supprimer une tâche
@router.delete("/taches/{tache_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_tache(
    tache_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    result = await db.execute(select(Tache).filter(Tache.id == tache_id, Tache.owner_id == current_user.id))
    db_tache = result.scalars().first()

    if not db_tache:
        raise HTTPException(status_code=404, detail="Tâche non trouvée ou non autorisée")

    await db.delete(db_tache)
    await db.commit()

import json

from fastapi import APIRouter, Depends, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import RoleChecker, get_current_user
from app.core.database import get_db
from app.core.redis import redis_client
from app.models.project import Project
from app.models.user import User, UserRole
from app.schemas.project import ProjectCreate, ProjectOut

router = APIRouter(prefix="/projects", tags=["Projects"])

@router.post("/", response_model=ProjectOut, status_code=status.HTTP_201_CREATED)
async def create_project(
    project_in: ProjectCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(RoleChecker([UserRole.MANAGER, UserRole.ADMIN]))
):
    """Создать новый проект (Доступно: Manager, Admin)."""
    new_project = Project(
        title=project_in.title,
        description=project_in.description,
        creator_id=current_user.id
    )
    db.add(new_project)
    await db.commit()
    await db.refresh(new_project)

    await redis_client.delete("projects_list")
    return new_project

@router.get("/", response_model=list[ProjectOut])
async def list_projects(
    skip: int = 0,
    limit: int = 10,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Получить список проектов (с кэшированием в Redis)."""
    cache_key = "projects_list"

    cached_projects = await redis_client.get(cache_key)
    if cached_projects:
        return json.loads(cached_projects)

    result = await db.execute(select(Project).offset(skip).limit(limit))
    projects = result.scalars().all()

    projects_json = [
        {
            "id": p.id, "title": p.title, "description": p.description,
            "creator_id": p.creator_id, "created_at": p.created_at.isoformat()
        } for p in projects
    ]

    await redis_client.set(cache_key, json.dumps(projects_json), ex=60)

    return projects
from typing import Optional
from fastapi import APIRouter, HTTPException, Depends
from app.schemas import ProjectCreate, ProjectOut, ProjectUpdate
import app.models
from app.dependencies import get_current_user, get_pagination
from sqlalchemy.orm import Session
from app.database import get_db

router = APIRouter(prefix="/projects", tags=["projects"], dependencies=[Depends(get_current_user)])

@router.post("", response_model=ProjectOut, status_code=201)
def post_projects(project: ProjectCreate, 
                  db: Session = Depends(get_db), 
                  user: app.models.User = Depends(get_current_user)):   
    new_project = app.models.Project(
        name = project.name,
        description = project.description,
        owner_id = user.id
    )
    db.add(new_project)
    db.commit()
    db.refresh(new_project)
    return new_project

@router.get("", response_model=list[ProjectOut])
def get_projects(search: Optional[str] = None, 
                 db: Session = Depends(get_db), 
                 pagination: dict = Depends(get_pagination)):
    query = db.query(app.models.Project)
    if search:
        query = query.filter(app.models.Project.name.ilike(f"%{search}%"))
    projects = query.offset(pagination["skip"]).limit(pagination["limit"]).all()
    if not projects:
        return []
    return projects

@router.get("/{project_id}", response_model=ProjectOut)
def get_project_by_id(project_id: int,
                      db: Session = Depends(get_db)):
    project = db.query(app.models.Project).filter(app.models.Project.id == project_id).first()
    if project is None:
        raise HTTPException(status_code=404, detail=f"There is no project with ID {project_id}.")
    return project

@router.patch("/{project_id}", response_model=ProjectOut)
def patch_project(project_id: int,
                  project_upts: ProjectUpdate,
                  db: Session = Depends(get_db),
                  current_user: app.models.User = Depends(get_current_user)):
    project = db.query(app.models.Project).filter(app.models.Project.id == project_id).first()
    if project is None:
         raise HTTPException(status_code=404, detail=f"There is no project with ID {project_id}.")
    if project.owner_id != current_user.id and current_user.role != app.models.UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Not authorized to modify this project.")
    for field, value in project_upts.model_dump(exclude_unset=True).items():
        setattr(project, field, value)
    db.commit()
    db.refresh(project)
    return project
    
@router.delete("/{project_id}",status_code=204)
def delete_project(project_id: int,
                   db: Session = Depends(get_db),
                   current_user: app.models.User = Depends(get_current_user)):
    project = db.query(app.models.Project).filter(app.models.Project.id == project_id).first()
    if project is None:
         raise HTTPException(status_code=404, detail=f"There is no project with ID {project_id}.")
    if project.owner_id != current_user.id and current_user.role != app.models.UserRole.ADMIN:
         raise HTTPException(status_code=403, detail="Not authorized to modify this project.")
    db.delete(project)
    db.commit()

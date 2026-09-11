from fastapi import APIRouter, HTTPException, Depends
from app.schemas import IssueCreate, IssueOut, IssueUpdate, IssuePriority, IssueStatus
import app.models
from app.dependencies import get_current_user, get_pagination
from sqlalchemy.orm import Session
from app.database import get_db
from typing import Optional

router = APIRouter(tags=["issues"], dependencies=[Depends(get_current_user)])

@router.post("/projects/{project_id}/issues", response_model=IssueOut, status_code=201)
def post_issue(project_id: int,
               issue: IssueCreate,
               db: Session = Depends(get_db),
               user: app.models.User = Depends(get_current_user)):
    project = db.query(app.models.Project).filter(app.models.Project.id == project_id).first()
    if project is None:
        raise HTTPException(status_code = 404, detail = "Project not found.")
    new_issue = app.models.Issue(
        title = issue.title,
        description = issue.description,
        status = issue.status or IssueStatus.OPEN,
        priority = issue.priority or IssuePriority.MEDIUM,
        project_id = project.id,
        reporter_id = user.id
    )
    db.add(new_issue)
    db.commit()
    db.refresh(new_issue)
    return new_issue

@router.get("/projects/{project_id}/issues", response_model=list[IssueOut])
def get_issues(project_id: int,
               status: Optional[IssueStatus] = None,
               priority: Optional[IssuePriority] = None,
               db: Session = Depends(get_db),
               pagination: dict = Depends(get_pagination)):
    project = db.query(app.models.Project).filter(app.models.Project.id == project_id).first()
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found.")
    query = db.query(app.models.Issue).filter(app.models.Issue.project_id == project_id)
    if status:
        query = query.filter(app.models.Issue.status == status)
    if priority:
        query = query.filter(app.models.Issue.priority == priority)
    issues = query.offset(pagination["skip"]).limit(pagination["limit"]).all()
    return issues

@router.get("/issues/{issue_id}", response_model=IssueOut)
def get_issue_by_id(issue_id: int,
                    db: Session = Depends(get_db)):
    issue = db.query(app.models.Issue).filter(app.models.Issue.id == issue_id).first()
    if not issue:
        raise HTTPException(status_code=404, detail="Issue not found.")
    return issue

@router.patch("/issues/{issue_id}", response_model=IssueOut)
def update_issue(issue_id: int,
                 uptdate: IssueUpdate,
                 db: Session = Depends(get_db),
                 user: app.models.User = Depends(get_current_user)):
    issue = db.query(app.models.Issue).filter(app.models.Issue.id == issue_id).first()
    if not issue:
        raise HTTPException(status_code=404, detail="Issue not found.")
    if user.id != issue.reporter_id and user.id != issue.project.owner_id and user.role != app.models.UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Not authorized to modify this issue.")
    for field, value in uptdate.model_dump(exclude_unset=True).items():
            setattr(issue, field, value)
    db.commit()
    db.refresh(issue)
    return issue

@router.delete("/issues/{issue_id}", status_code=204)
def delete_issue(issue_id: int,
                 db: Session = Depends(get_db),
                 user: app.models.User = Depends(get_current_user)):
    issue = db.query(app.models.Issue).filter(app.models.Issue.id == issue_id).first()
    if not issue:
        raise HTTPException(status_code=404, detail="Issue not found.")
    if user.id != issue.reporter_id and user.id != issue.project.owner_id and user.role != app.models.UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Not authorized to delete this issue.")
    db.delete(issue)
    db.commit()

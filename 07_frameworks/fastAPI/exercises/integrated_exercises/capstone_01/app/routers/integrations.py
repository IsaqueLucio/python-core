from fastapi import APIRouter, HTTPException, Depends
from app.dependencies import get_current_user
from app.schemas import GitHubProfileOut
import httpx

router = APIRouter(prefix="/integrations", tags=["integrations"], dependencies=[Depends(get_current_user)])

@router.get("/github/{username}", response_model=GitHubProfileOut)
async def get_github_profile(username: str):
    url = f"https://api.github.com/users/{username}"
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, timeout=30)
            if response.status_code == 404:
                raise HTTPException(status_code=404, detail="User not found.")
            response.raise_for_status()
            data = response.json()
            github_profile = GitHubProfileOut(
                login=data["login"],
                name=data["name"],
                public_repos=data["public_repos"],
                html_url=data["html_url"]
            )
            return github_profile
    except HTTPException:
        raise
    except (httpx.TimeoutException, httpx.NetworkError, httpx.HTTPError):
        raise HTTPException(status_code=502, detail="Bad Gateway")
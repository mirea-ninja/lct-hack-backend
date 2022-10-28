from fastapi import APIRouter, Depends

router = APIRouter()


@router.post("/signin")
async def signin():
    pass


@router.post("/signup")
async def signup():
    pass

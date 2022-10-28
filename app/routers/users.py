from fastapi import APIRouter, Depends

router = APIRouter()


@router.post('/user')
async def create():
    pass

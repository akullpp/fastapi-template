from fastapi import APIRouter, Depends

from app.security import authorization

router = APIRouter(
    prefix="/health",
    dependencies=[Depends(authorization)],
    tags=["Health"],
)


@router.get("")
def get_health():
    pass

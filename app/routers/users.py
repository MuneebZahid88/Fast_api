from ..models import models
from ..schemas.schemas import UserCreate,UserResponse
from ..utils.utils import hash_password
from fastapi import Body, FastAPI, responses, status, HTTPException, Depends,APIRouter
from ..database.database import engine, get_db
from sqlalchemy.orm import Session


router = APIRouter(prefix="/users",tags={'Users'})

@router.post("/", status_code=status.HTTP_201_CREATED,response_model=UserResponse)
async def create_user(user:UserCreate,db: Session = Depends(get_db)):
    

    user.password = hash_password(user.password)
     

    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user



@router.get("/{id}",response_model=UserResponse)
async def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {id} does not exist"
        )

    return user


@router.get("/",response_model=list[UserResponse])
async def get_user(db: Session = Depends(get_db)):
    user = db.query(models.User).all()

    return user

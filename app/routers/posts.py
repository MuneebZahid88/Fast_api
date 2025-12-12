from ..models import models
from ..schemas.schemas import PostCreate,PostResponse
from fastapi import Body, FastAPI, responses, status, HTTPException, Depends,APIRouter
from ..database.database import engine, get_db
from sqlalchemy.orm import Session
from ..oauth2 import get_current_user


router = APIRouter(prefix="/posts",tags={'Posts'})



# SQLAlchemy test route
@router.get("/",response_model=list[PostResponse])
async def read_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts


# # GET ALL POSTS (raw SQL)
# @app.get("/posts")
# async def read_posts():
#     cursor.execute("SELECT * FROM posts")
#     posts = cursor.fetchall()
#     return {"posts": posts}


# CREATE POST
@router.post("/", status_code=status.HTTP_201_CREATED,response_model=PostResponse)
async def create_post(post: PostCreate = Body(...),db: Session = Depends(get_db),current_user:int = Depends(get_current_user)):
    
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


# # CREATE POST
# @app.post("/posts", status_code=status.HTTP_201_CREATED)
# async def create_post(post: PostSchema = Body(...)):
#     cursor.execute(
#         "INSERT INTO posts(title, content, published) VALUES (%s, %s, %s) RETURNING *",
#         (post.title, post.content, post.published)
#     )
#     new_post = cursor.fetchone()
#     conn.commit()
#     return {"post_created": new_post}


# GET SINGLE POST
@router.get("/{id}",response_model=PostResponse)
async def get_post(id: int,db: Session = Depends(get_db)):
    posts = db.query(models.Post).filter(models.Post.id == id).first()
    
    if posts:
        return posts

    raise HTTPException(status_code=404, detail=f"Post with id {id} not found")




# # GET SINGLE POST
# @app.get("/posts/{id}")
# async def get_post(id: int):
#     cursor.execute("SELECT * FROM posts WHERE id = %s", (str(id),))
#     post_record = cursor.fetchone()

#     if post_record:
#         return {"post": post_record}

#     raise HTTPException(status_code=404, detail=f"Post with id {id} not found")




# DELETE POST
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int,db: Session = Depends(get_db),current_user:int = Depends(get_current_user)):
    

    posts = db.query(models.Post).filter( models.Post.id == id)

    if posts.first() == None:

        raise HTTPException(status_code=404, detail="Post not found")
    
    posts.delete(synchronize_session = False)
    db.commit()

    return responses.Response(status_code=204)


# # DELETE POST
# @app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
# async def delete_post(id: int):
#     cursor.execute("DELETE FROM posts WHERE id = %s RETURNING *", (str(id),))
#     deleted_post = cursor.fetchone()
#     conn.commit()

#     if deleted_post:
#         return responses.Response(status_code=204)

#     raise HTTPException(status_code=404, detail="Post not found")




# UPDATE POST
@router.put("/{id}",response_model=PostResponse)
async def update_post(id: int,post: PostCreate = Body(...),db: Session = Depends(get_db),current_user:int = Depends(get_current_user)):
    
    
    post_querry = db.query(models.Post).filter( models.Post.id == id)
    posts = post_querry.first()

    if posts is None:
        raise HTTPException(status_code=404, detail="Post not found")

    post_querry.update(post.dict(),synchronize_session = False)
    db.commit()
    return post_querry.first()



# # UPDATE POST
# @app.put("/posts/{id}")
# async def update_post(id: int, updated_post: PostSchema = Body(...)):
#     cursor.execute(
#         """
#         UPDATE posts
#         SET title = %s, content = %s, published = %s
#         WHERE id = %s
#         RETURNING *
#         """,
#         (updated_post.title, updated_post.content, updated_post.published, id)
#     )

#     updated_row = cursor.fetchone()
#     conn.commit()

#     if updated_row is None:
#         raise HTTPException(status_code=404, detail="Post not found")

#     return {"message": "Post updated", "post": updated_row}



from fastapi import FastAPI, Depends, HTTPException, status, Response 
import models
import schemas
from typing import Optional
from database import engine, SessionLocal
from sqlalchemy.orm import Session


app = FastAPI()


models.Base.metadata.create_all(engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/blog", status_code=status.HTTP_201_CREATED)
def create(request:schemas.Blog, db: Session = Depends( get_db)):
    new_blog = models.Blog(title= request.title, body = request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return  new_blog

 
@app.get("/blogs")
def get_all_blogs(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs 


@app.get("/blog/{id}", response_model=schemas.Blog,status_code=status.HTTP_200_OK)
def read_blog(id: int, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    db.commit()
    if not blog : 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with the id {id}  not found ")
    return blog
 
@app.put("/blog/{id}")
def update(id:int, request:schemas.Blog, db:Session = Depends(get_db)):
     blog = db.query(models.Blog).filter(models.Blog.id == id).first()
     if not blog:
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "Blog not found")
     blog.title = request.title
     blog.body = request.body
     db.commit()
     return {"Message":"Updated successfully"}

 
@app.delete("/blog/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_blog(id, db:Session = Depends(get_db)):
   
      
      db.query(models.Blog).filter(models.Blog.id == id).delete(synchronize_session=False)
      db.commit()
      raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail=f"Blog with the id {id} was deleted successfully")
    #if blog is not found raise http 404 error
#raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

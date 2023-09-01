from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String

app = FastAPI()

#SQLALCHEMY_DATABASE_URL = "postgresql://myuser:password@localhost/fastapi_database"
#SQLALCHEMY_DATABASE_URL = "postgresql://myuser:password@localhost/fastapi_database"
SQLALCHEMY_DATABASE_URL = "sqlite:///urls.db"
#
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Veritabanı modeli
class URL(Base):
    __tablename__ = "urls"
    id = Column(Integer, primary_key=True)
    url = Column(String)
    url_id = Column(Integer)
    url_author = Column(String)
    source = Column(String)

Base.metadata.create_all(bind=engine)

# Veritabanı oturumu oluşturma
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
@app.post("/urls")
def create_url(url: str, url_id: int, url_author: str, source: str, db: Session = Depends(get_db)):
    new_url = URL(url=url, url_id=url_id, url_author=url_author, source=source)
    db.add(new_url)
    db.commit()
    db.refresh(new_url)
    return new_url

@app.get("/urls")
def get_all_urls(db: Session = Depends(get_db)):
    urls = db.query(URL).all()
    return urls


@app.get("/urls/{url_id}")
def get_url_by_id(url_id: int, db: Session = Depends(get_db)):
    url = db.query(URL).filter(URL.id == url_id).first()
    if not url:
        raise HTTPException(status_code=404, detail="URL not found")
    return url

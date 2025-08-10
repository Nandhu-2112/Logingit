from fastapi import FastAPI
from pydantic import BaseModel
import mysql.connector
from starlette.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "nandhu",
    "port": 3309
}

class RegisterItem(BaseModel):
    name: str
    phno: str
    email: str
    password: str

@app.post("/register")
def register(i: RegisterItem):
    mydb = mysql.connector.connect(**DB_CONFIG)
    mypost = mydb.cursor()
    query = f"INSERT INTO usersdb (name, phno, email, password) VALUES ('{i.name}', '{i.phno}', '{i.email}', '{i.password}')"
    mypost.execute(query)
    mydb.commit()
    mydb.close()
    return {"message": "Registered successfully"}

class LoginItem(BaseModel):
    email: str
    password: str

@app.post("/login")
def login(i: LoginItem):
    mydb = mysql.connector.connect(**DB_CONFIG)
    mypost = mydb.cursor()
    query = f"SELECT * FROM usersdb WHERE email='{i.email}' AND password='{i.password}'"
    mypost.execute(query)
    result = mypost.fetchone()
    mydb.close()
    if result:
        return {"message": "Login successful"}
    else:
        return {"message": "Invalid credentials"}

@app.get("/table")
def view():
    mydb = mysql.connector.connect(**DB_CONFIG)
    mypost = mydb.cursor(dictionary=True)
    mypost.execute("SELECT * FROM usersdb")
    result = mypost.fetchall()
    mydb.close()
    return result

class UpdateItem(BaseModel):
    name: str

@app.put("/update/{user_id}")
def update(i: UpdateItem, user_id: int):
    mydb = mysql.connector.connect(**DB_CONFIG)
    mypost = mydb.cursor()
    query = f"UPDATE usersdb SET name='{i.name}' WHERE id={user_id}"
    mypost.execute(query)
    mydb.commit()
    mydb.close()
    return {"message": "Successfully updated"}

@app.delete("/del/{user_id}")
def delete(user_id: int):
    remote_db = mysql.connector.connect(
        host="ut3742.h.filess.io",
        user="logindb_childtube",
        password="165f0c3c342e32651e89590a2c42b374e2856d10",
        database="logindb_childtube",
        port=3307
    )
    mypost = remote_db.cursor()
    query = f"DELETE FROM usersdb WHERE id={user_id}"
    mypost.execute(query)
    remote_db.commit()
    remote_db.close()
    return {"message": "Deleted successfully"}

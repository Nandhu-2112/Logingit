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

class RegisterItem(BaseModel):
    name: str
    phno: str
    email: str
    password: str
@app.post("/register")
def register(i: RegisterItem):
    mydb = mysql.connector.connect(
        host="ut3742.h.filess.io",
        user="logindb_childtube",
        password="165f0c3c342e32651e89590a2c42b374e2856d10",
        database="logindb_childtube",
        port=3307
    )
    mypost = mydb.cursor()
    mypost.execute("insert into  usersdb (name, phno, email, password) values ('"
        + i.name + "', '" + i.phno + "', '" + i.email + "', '" + i.password + "')"
    )
    mydb.commit()
    mydb.close()
    return {"message": "registered successfull"}


class LoginItem(BaseModel):
    email: str
    password: str

@app.post("/login")
def login(i: LoginItem):
    mydb = mysql.connector.connect(
        host="ut3742.h.filess.io",
        user="logindb_childtube",
        password="165f0c3c342e32651e89590a2c42b374e2856d10",
        database="logindb_childtube",
        port=3307
    )
    mypost = mydb.cursor()
    mypost.execute(
        "select * from usersdb where email='" + i.email + "' AND password='" + i.password + "'"
    )
    result = mypost.fetchone()
    mydb.close()
    if result:
        return {"message": "Success"}
    else:
        return {"message": "Invalid"}


@app.get("/table")
def view():
    mydb = mysql.connector.connect(
        host="ut3742.h.filess.io",
        user="logindb_childtube",
        password="165f0c3c342e32651e89590a2c42b374e2856d10",
        database="logindb_childtube",
        port=3307
    )
    mypost= mydb.cursor(dictionary=True)
    mypost.execute("SELECT * FROM usersdb")
    result =  mypost.fetchall()
    mydb.close()
    return result

class UpdateItem(BaseModel):
    name: str

@app.put("/update/{user_id}")
def update(i: UpdateItem, user_id: int):
    mydb = mysql.connector.connect(
        host="ut3742.h.filess.io",
        user="logindb_childtube",
        password="165f0c3c342e32651e89590a2c42b374e2856d10",
        database="logindb_childtube",
        port=3307
    )
    mypost = mydb.cursor()
    mypost.execute("update usersdb set name='" + i.name + "' where id=" + str(user_id))
    mydb.commit()
    mydb.close()
    return {"message": "Updated"}
#
@app.delete("/del/{user_id}")
def delete(user_id: int):
    mydb = mysql.connector.connect(
        host="ut3742.h.filess.io",
        user="logindb_childtube",
        password="165f0c3c342e32651e89590a2c42b374e2856d10",
        database="logindb_childtube",
        port=3307
    )
    mypost = mydb.cursor()
    mypost.execute("delete from usersdb where id=" + str(user_id))
    mydb.commit()
    mydb.close()
    return {"message": "Deleted"}






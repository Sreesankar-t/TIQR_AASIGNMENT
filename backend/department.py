from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.middleware.cors import CORSMiddleware
import psycopg2
import json
from pydantic import BaseModel

app =FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DB_CONFIG = {
        'dbname':"department",
        'user':"postgres",
        'password':"Sree@123",
        'host':"localhost",
        'port':"5432"
}

class Department(BaseModel):
    name: str
    number_of_employee: int

class Employee(BaseModel):
    name: str
    department: str
    age: int   

class UpdateDepartmentModel(BaseModel):
    name: str     


def dbConnection():
    conn = psycopg2.connect(**DB_CONFIG)
    return conn

# DEPAERMENT
# Read department
@app.get("/read-department")
async def read_department():
        conn =dbConnection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM department")
        rows = cur.fetchall()
        cur.close()
        conn.close()    
        department = [{"id": row[0], "name": row[1], "number_of_employee": row[2]} for row in rows]
        return department

# Add department
@app.post("/add-department")
async def add_department(department:Department):
        conn = dbConnection()
        cur = conn.cursor()
        cur.execute("INSERT INTO department (name, number_of_employee) VALUES (%s, %s)",
                    (department.name,department.number_of_employee))

        conn.commit()
        cur.close()
        conn.close() 
        return {"status": "department added"}

# Update department   
@app.put("/update-department/{department_id}")

async def update_department(department_id :int,department:UpdateDepartmentModel):
        print(department_id)
        conn =dbConnection()
        cur =conn.cursor()
        cur.execute("UPDATE department SET name = %s WHERE id = %s",(department.name,department_id))
        conn.commit()
        cur.close()
        conn.close()
        return{"status" : "department updated"}

# Delete department
@app.delete("/delete-department/{department_id}")
async def delete_department(department_id: int):
    conn =dbConnection()
    cur = conn.cursor()
    cur.execute("DELETE FROM department WHERE id = %s", (department_id,))
    conn.commit()
    cur.close()
    conn.close()
    return {"status": "department deleted"}    


# EMPLOYEE
# read employee
@app.get("/read-user")
async def read_user():
    conn =dbConnection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM employee")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    users = [{"id": row[0], "name": row[1], "department": row[2], "age": row[3]} for row in rows]
    return users

# Add user
@app.post("/add-user")
async def add_user(employee: Employee):
    conn =dbConnection()
    cur = conn.cursor()
    cur.execute("SELECT id, number_of_employee FROM department WHERE name = %s", (employee.department,))
    department = cur.fetchone()
    
    if department:
        department_id, number_of_employee = department
        cur.execute("UPDATE department SET number_of_employee = %s WHERE id = %s",
                    (number_of_employee + 1, department_id))
    else:
        cur.execute("INSERT INTO department (name, number_of_employee) VALUES (%s, %s) RETURNING id",
                    (employee.department, 1))
        department_id = cur.fetchone()[0]
    
    cur.execute("INSERT INTO employee (name, department, age) VALUES (%s, %s, %s)",
                (employee.name, employee.department, employee.age))
    conn.commit()
    cur.close()
    conn.close()
    return {"status": "employee added"}

# Update user
@app.put("/update-employee/{user_id}")
async def update_employee(user_id: int, employee: Employee):
    conn =dbConnection()
    cur = conn.cursor()
    cur.execute("UPDATE employee SET name = %s, department = %s, age = %s WHERE id = %s",
                (employee.name, employee.department, employee.age, user_id))
    conn.commit()
    cur.close()
    conn.close()
    return {"status": "employee updated"}

# Delete user
@app.delete("/delete-user/{user_id}")
async def delete_user(user_id: int):
    conn =dbConnection()
    cur = conn.cursor()
    cur.execute("SELECT department FROM employee WHERE id = %s", (user_id,))
    result = cur.fetchone()
    
    if result:
        department_name = result[0]
        cur.execute("DELETE FROM employee WHERE id = %s", (user_id,))
        conn.commit()
        cur.execute("UPDATE department SET number_of_employee = number_of_employee - 1 WHERE name = %s",
                    (department_name,))
        conn.commit()
        cur.close()
        conn.close()
        return {"status": "user deleted"}
    else:
        cur.close()
        conn.close()
        raise HTTPException(status_code=404, detail="User not found")
                          
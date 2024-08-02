from http.server import BaseHTTPRequestHandler, HTTPServer
import psycopg2
import json

class RequestHandler(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Content-Type', 'application/json')

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS, DELETE')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()


    def do_GET(self):
        if self.path == "/read-department":
            print("---READ DEPARTMENT---")
            self.get_department()     

        elif self.path == '/read-user':
            print("---READ USER---")
            self.get_users()

        else:
            self.send_response(404)
            self.end_headers()   

    
    def do_POST(self):
        if self.path == '/add-department':
            print('---ADD DEPARTMENT---')
            self.add_department()

        elif self.path == "/add-user":
            print("---ADD USER---")
            self.add_user()

        else:
            self.send_response(404)
            self.end_headers()


    def do_PUT(self):
        
        if self.path.startswith("/update-department"):    
            print("---UPDATE DEPAERMENT---")
            self.update_department()

        elif self.path.startswith("/update-employee"):
            self.update_employee()

        else:
            self.send_response(404)
            self.end_headers()


    def do_DELETE(self):
        if self.path.startswith("/delete-department/"):
            print("---DELETE DEPAERMENT ---")
            self.delete_department()

        elif self.path.startswith("/delete-user/"):
             print("---DELETE USER ---")
             self.delete_user()

        else:
            self.send_response(404)
            self.end_headers()       

# DEPAERMENT
    def get_department(self):
        conn = psycopg2.connect(
            dbname="department",
            user="postgres",
            password="Sree@123",
            host="localhost",
            port="5432"
        )
        cur = conn.cursor()
        cur.execute("SELECT * FROM department")
        rows = cur.fetchall()

        department = [{"id": row[0], "name": row[1], "number_of_employee": row[2]} for row in rows]
        data = json.dumps(department)
        self.send_response(200)
        self._set_headers()
        self.end_headers()
        self.wfile.write(data.encode('utf-8'))

        cur.close()
        conn.close()

            

    def add_department(self):
        content_length = int(self.headers['Content-Length']) 
        post_data = self.rfile.read(content_length)
        request_json = json.loads(post_data)
        conn = psycopg2.connect(
            dbname="department",
            user="postgres",
            password="Sree@123",
            host="localhost",
            port="5432"
        )
        cur = conn.cursor()
        cur.execute("INSERT INTO department (name, number_of_employee) VALUES (%s, %s)",
                    (request_json['name'], request_json['number_of_employee']))

        conn.commit()

        self.send_response(201)
        self._set_headers()
        self.end_headers()
        self.wfile.write(json.dumps({'status': 'department added'}).encode('utf-8'))

        cur.close()
        conn.close()    

  
    def update_department(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        request_json = json.loads(post_data)
        department_id = self.path.split("/")[-1]

        conn = psycopg2.connect(
            dbname="department",
            user="postgres",
            password="Sree@123",
            host="localhost",
            port="5432"
        )
        cur = conn.cursor()
        cur.execute("UPDATE department SET name = %s  WHERE id = %s",
                    (request_json['name'] ,department_id))
        conn.commit()

        self.send_response(200)
        self._set_headers()
        self.end_headers()
        self.wfile.write(json.dumps({'status': 'department updated'}).encode('utf-8'))

        cur.close()
        conn.close()



    def delete_department(self):
        id = self.path.split("/")[-1]
        conn = psycopg2.connect(
            dbname="department",
            user="postgres",
            password="Sree@123",
            host="localhost",
            port="5432"
        )
        cur = conn.cursor()
        cur.execute("DELETE FROM department WHERE id = %s", (id,))
        conn.commit()

        self.send_response(200)
        self._set_headers()
        self.end_headers()
        self.wfile.write(json.dumps({'status': 'department deleted','code':200}).encode('utf-8'))

        cur.close()
        conn.close()        
            

# EMPLOYEE    
    def get_users(self):
        conn = psycopg2.connect(
            dbname="department",
            user="postgres",
            password="Sree@123",
            host="localhost",
            port="5432"
        )
        cur = conn.cursor()
        cur.execute("SELECT * FROM employee")
        rows = cur.fetchall()

        users = [{"id": row[0], "name": row[1], "department": row[2], "age": row[3]} for row in rows]
        data = json.dumps(users)
        self.send_response(200)
        self._set_headers()
        self.end_headers()
        self.wfile.write(data.encode('utf-8'))

        cur.close()
        conn.close()


    def add_user(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        request_json = json.loads(post_data)
        department_name = request_json['department']

        conn = psycopg2.connect(
        dbname="department",
        user="postgres",
        password="Sree@123",
        host="localhost",
        port="5432"
        )
        cur = conn.cursor()

        
        cur.execute("SELECT id, number_of_employee FROM department WHERE name = %s", (department_name,))
        department = cur.fetchone()

        if department:
           
            department_id, number_of_employee = department
            cur.execute("UPDATE department SET number_of_employee = %s WHERE id = %s",
                    (number_of_employee + 1, department_id))
        else:
            
            cur.execute("INSERT INTO department (name, number_of_employee) VALUES (%s, %s) RETURNING id",
                    (department_name, 1))
            department_id = cur.fetchone()[0]

        
        cur.execute("INSERT INTO employee (name, department, age) VALUES (%s, %s, %s)",
                (request_json['name'], department_name, request_json['age']))
        conn.commit()

        self.send_response(201)
        self._set_headers()
        self.end_headers()
        self.wfile.write(json.dumps({'status': 'employee added'}).encode('utf-8'))

        cur.close()
        conn.close()

        

    def update_employee(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        request_json = json.loads(post_data)
        user_id = self.path.split("/")[-1]

        conn = psycopg2.connect(
            dbname="department",
            user="postgres",
            password="Sree@123",
            host="localhost",
            port="5432"
        )
        cur = conn.cursor()
        cur.execute("UPDATE employee SET name = %s , department = %s , age = %s  WHERE id = %s",
                    (request_json['name'] ,request_json['department'] ,request_json['age'], user_id))
        conn.commit()

        self.send_response(200)
        self._set_headers()
        self.end_headers()
        self.wfile.write(json.dumps({'status': 'employee updated'}).encode('utf-8'))

        cur.close()
        conn.close()

    
    def delete_user(self):
        user_id = self.path.split("/")[-1]

        conn = psycopg2.connect(
        dbname="department",
        user="postgres",
        password="Sree@123",
        host="localhost",
        port="5432"
        )
        cur = conn.cursor()

        # Get the department of the user before deletion
        cur.execute("SELECT department FROM employee WHERE id = %s", (user_id,))
        result = cur.fetchone()

        if result:
            department_name = result[0]

            
            cur.execute("DELETE FROM employee WHERE id = %s", (user_id,))
            conn.commit()

            
            cur.execute("UPDATE department SET number_of_employee = number_of_employee - 1 WHERE name = %s",
                    (department_name,))
            conn.commit()

            self.send_response(200)
            self._set_headers()
            self.end_headers()
            self.wfile.write(json.dumps({'status': 'user deleted', 'code': 200}).encode('utf-8'))
        else:
            self.send_response(404)
            self._set_headers()
            self.end_headers()
            self.wfile.write(json.dumps({'status': 'user not found', 'code': 404}).encode('utf-8'))

        cur.close()
        conn.close()
        

# SERVER CONFIGURATION
def run(server_class=HTTPServer, handler_class=RequestHandler, port=8080):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting httpd server on port {port}...')
    httpd.serve_forever()


if __name__ == "__main__":
    run()
                          
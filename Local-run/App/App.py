import os
from flask import Flask, render_template,request,session,url_for,redirect
from sqlalchemy import (Column, Integer, MetaData, String, Table,
                        create_engine, inspect)
from sqlalchemy.exc import SQLAlchemyError

app = Flask(__name__,template_folder='../templates',static_folder='../static')
# Change this to your secret key (can be anything, it's for extra protection)
app.secret_key = 's_ecre_t'
# parent directory
parent_dir = os.path.dirname(os.path.dirname(__file__))
#Populate AWS DB End Point from rds_endpoint.txt file
#db_endpoint_file = open("/home/ec2-user/rds_endpoint.txt", "r")
db_endpoint_file = open(parent_dir+"/rds_endpoint.txt", "r") #<--Uncomment to run locally and update the file path

db_parms_file = parent_dir+"/sqldbparms.txt" #<--Uncomment to run locally and update the file path

#read sql parms from file
with open(db_parms_file,"r") as f:
    rows = ( line.split('=') for line in f)
    dict = { row[0]:row[1] for row in rows }

for item in dict:
    if str(item) == "sqlid":
        var_sqlid = dict[item].rstrip('\n')
    if str(item) == "sqlpass":
        var_sqlpass = dict[item].rstrip('\n')
    if str(item) == "sqldb":
        var_sqldb = dict[item].rstrip('\n')


#read whole file to a string
db_endpoint_file_text = db_endpoint_file.read().rstrip('\n')

## Manipulate and concate string
db_endpoint_prefix = "mysql+pymysql://"+var_sqlid+":"+var_sqlpass
#db_endpoint_prefix = "mysql+pymysql://admin:Japassword-1@"
#db_uri = db_endpoint_prefix + db_endpoint_file_text.replace(":3306","/f1dbse")
db_uri = db_endpoint_prefix +"@"+ db_endpoint_file_text+"/"+var_sqldb

#close file
db_endpoint_file.close()

print(db_uri)

engine = ''

# Create a metadata instance/object
metadata = MetaData()  # Create the Metadata Object

# f1_driver_tbl Preparing SQL query to INSERT a record into the database.
f1_driver_insert_stmt = ("INSERT INTO f1driver_tbl (f1drivername, f1wins, status) VALUES (%s, %s, %s)")
f1_driver_insert_data1 = ('Lewis Hamilton','103','Active')
f1_driver_insert_data2 = ('Michael Schumacher','91','Retired')
#COUNT Query
f1_driver_count_qry='SELECT COUNT(f1wins) FROM f1driver_tbl'

# f1_accnt_tbl Preparing SQL query to INSERT a record into the database.
f1_accnt_insert_stmt = ("INSERT INTO f1_accnt_tbl (id,username,password,email) VALUES (%s, %s, %s, %s)")
f1_accnt_insert_data1 = ('1','f1admin','f1-admin-pass','f1-admin@f1admin.com')
#COUNT Query
f1_accnt_count_qry='SELECT COUNT(username) FROM f1_accnt_tbl'

inspector = ''
conn=''

try:
    create_engine(db_uri).connect()
    engine = create_engine(db_uri)
    metadata.reflect(bind=engine)
    inspector = inspect(engine)
    conn = engine.connect()
    print(" DB Connected--> success")
    ukdb_flag = True
except SQLAlchemyError as err:
    print ("DB Not Connected. Check DB End point in rds_endpoint.txt file",
            err.__cause__)  # this will give what kind of error


def create_table(var_tableName, metadata):  # Function creates table if it doesn't exist
    tables = metadata.tables.keys()
    #Creating a cursor object using the cursor() method
    #cursor = conn.cursor()
    if var_tableName not in tables:
      if var_tableName == "f1driver_tbl":
        t1 = Table(var_tableName, metadata,  # Create a table with the appropriate Columns
                   Column('id', Integer, primary_key=True, nullable=False, autoincrement=True),
                   Column('f1drivername', String(30), nullable=False),
                   Column('f1wins', Integer),
                   Column('status', String(15)))# check if table exits

        t1.create(engine)

        table_list = inspector.get_table_names()
        print("New Table Created  => ",table_list[0])
        conn.execute(f1_driver_insert_stmt, f1_driver_insert_data1)
        conn.execute(f1_driver_insert_stmt, f1_driver_insert_data2)
        # conn.execute(t1.insert(),[
        #     {'f1drivername':'Lewis Hamilton','f1wins':'103','status':'Active'},
        #     {'f1drivername':'Michael Schumacher','f1wins':'91','status':'Retired'}])
      elif var_tableName == "f1_accnt_tbl":
            t2 = Table(var_tableName, metadata,  # Create a table with the appropriate Columns
                    Column('id', Integer, primary_key=True, nullable=False, autoincrement=True),
                    Column('username', String(50),nullable=False,),
                    Column('password', String(50),nullable=False,),
                    Column('email', String(100),nullable=False,))# check if table exits

            t2.create(engine)

            table_list = inspector.get_table_names()
            print("New Table Created  => ",table_list[0])
            conn.execute(f1_driver_insert_stmt, f1_driver_insert_data1)
            conn.execute(f1_driver_insert_stmt, f1_driver_insert_data2)
            # conn.execute(t2.insert(),[
            #     {'id':'1','username':'f1admin','password':'f1-admin','email':'f1-admin@f1admin.com'}])
        
    else:
            table_list = inspector.get_table_names()
            print("Table already exists  => ",table_list[0])
            f1_row_count = conn.execute(f1_driver_count_qry).fetchall()
            for rc in f1_row_count:
                if rc[0] == 0:
                   conn.execute(f1_driver_insert_stmt, f1_driver_insert_data1)
                   conn.execute(f1_driver_insert_stmt, f1_driver_insert_data2)
                   print("Table Empty. 2 new rows inserted")
                   break
            print("Table already exists  => ",table_list[1])
            acc_row_count = conn.execute(f1_accnt_count_qry).fetchall()
            for acc_rc in acc_row_count:
                if acc_rc[0] == 0:
                   conn.execute(f1_accnt_insert_stmt, f1_accnt_insert_data1)
                   print("Account Table Empty. 1 new row inserted")
                   break

tbls = ['f1driver_tbl','f1_accnt_tbl']  # Provides table /tables to be created
for _t in tbls: create_table(_t, metadata)

query_result = engine.execute('SELECT * FROM f1driver_tbl')

print("Id", "\t", "Driver Name ", "\t", "F1 Wins", "\t", " Status")
for _row in query_result:
    print(_row[0], "\t", _row[1], "\t", _row[2], "\t", _row[3])

with open(parent_dir+"/ipaddress.txt", "r+") as ipaddress_file:
    ip_address = ipaddress_file.read()     # Reading form a file

@app.route("/")
def homepage():
    """View function for Home Page."""
    select_result = conn.execute('SELECT * FROM f1driver_tbl')
    return render_template("home.html", result=select_result, ip=ip_address)

@app.route('/form')
def form():
    return render_template('form.html')

@app.route('/login', methods=['POST','GET'])
def login():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        # Check if account exists using MySQL
        ##cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        ##cursor.execute('SELECT * FROM accounts WHERE username = %s AND password = %s', (username, password,))
        # Fetch one record and return result
        account = conn.execute('SELECT * FROM f1_accnt_tbl WHERE username = %s AND password = %s', (username, password,)).fetchone()
        # If account exists in accounts table in out database
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            # Redirect to home page
            #return 'Logged in successfully!'
            return redirect(url_for('homepage'))
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'
        # Show the login form with message (if any)
        return render_template('login.html', msg=msg)
    return render_template('login.html', msg=msg)

@app.route('/data/', methods = ['POST', 'GET'])
def data():
    if request.method == 'GET':
        return f"The URL /data is accessed directly. Try going to '/form' to submit form"
    if request.method == 'POST':
        form_data = request.form
        sql = "INSERT INTO f1driver_tbl (f1drivername, f1wins, status) VALUES (%s, %s, %s)"
        sql_val=(request.form['F1driver_name'],request.form['F1_wins'],request.form['F1_status'])
        query_result = conn.execute(sql,sql_val)
        print("New Row Inserted")
        return render_template('data.html',form_data = form_data)

@app.route('/logout')
def logout():
    # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   # Redirect to login page
   return redirect(url_for('login'))
if __name__ == "__main__":
   # app.run(debug=False, host="0.0.0.0", port=3000)
     app.run(debug=False, host='0.0.0.0')

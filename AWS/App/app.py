from flask import Flask, render_template,request
from sqlalchemy import (Column, Integer, MetaData, String, Table,
                        create_engine, inspect)
from sqlalchemy.exc import SQLAlchemyError
app = Flask(__name__,template_folder='../templates')

#Populate AWS DB End Point from rds_endpoint.txt file
#db_endpoint_file = open("/home/ec2-user/rds_endpoint.txt", "r")
db_endpoint_file = open("./rds_endpoint.txt", "r") #<--Uncomment to run locally and update the file path
db_parms_file = "./sqldbparms.txt" #<--Uncomment to run locally and update the file path

#read sql parms from file
with open(db_parms_file,"r") as f:
    rows = ( line.split('=') for line in f)
    dict = { row[0]:row[1] for row in rows }

for item in dict:
    print (item, dict[item])
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

# Preparing SQL query to INSERT a record into the database.
insert_stmt = ("INSERT INTO f1driver_tbl (f1drivername, f1wins, status) VALUES (%s, %s, %s)")
insert_data1 = ('Lewis Hamilton','103','Active')
insert_data2 = ('Michael Schumacher','91','Retired')
#COUNT Query
count_qry='SELECT COUNT(*) FROM f1driver_tbl'

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
        t1 = Table(var_tableName, metadata,  # Create a table with the appropriate Columns
                   Column('id', Integer, primary_key=True, nullable=False, autoincrement=True),
                   Column('f1drivername', String(30), nullable=False),
                   Column('f1wins', Integer),
                   Column('status', String(15)))# check if table exits
                
        t1.create(engine)    

        table_list = inspector.get_table_names()
        print("New Table Created  => ",table_list[0])
        conn.execute(t1.insert(),[
            {'f1drivername':'Lewis Hamilton','f1wins':'103','status':'Active'},
            {'f1drivername':'Michael Schumacher','f1wins':'91','status':'Retired'}])
    else:
        table_list = inspector.get_table_names()
        print("Table already exists  => ",table_list[0])
        row_count = conn.execute(count_qry).fetchall()
        if row_count[0] == 0:
                conn.execute(insert_stmt, insert_data1)
                conn.execute(insert_stmt, insert_data2)

tbls = ['f1driver_tbl']  # Provides table /tables to be created
for _t in tbls: create_table(_t, metadata)
  
query_result = engine.execute('SELECT * FROM f1driver_tbl') 

print("Id", "\t", "Driver Name ", "\t", "F1 Wins", "\t", " Status")
for _row in query_result:
    print(_row[0], "\t", _row[1], "\t", _row[2], "\t", _row[3])   

with open("./ipaddress.txt", "r+") as ipaddress_file:
    ip_address = ipaddress_file.read()     # Reading form a file

@app.route("/")
def homepage():
    """View function for Home Page."""
    select_result = conn.execute('SELECT * FROM f1driver_tbl')
    return render_template("home.html", result=select_result, ip=ip_address)

@app.route('/form')
def form():
    return render_template('form.html')
 
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

if __name__ == "__main__":
   # app.run(debug=False, host="0.0.0.0", port=3000)
     app.run(debug=False, host='0.0.0.0', port=5000)

from flask import Flask, render_template,request
from sqlalchemy import (Column, Integer, MetaData, String, Table,
                        create_engine, inspect)
from sqlalchemy.exc import SQLAlchemyError
app = Flask(__name__,template_folder='../templates')

#Populate AWS DB End Point from rds_endpoint.txt file
#db_endpoint_file = open("/home/ec2-user/rds_endpoint.txt", "r")
db_endpoint_file = open("./rds_endpoint.txt", "r") #<--Uncomment to run locally and update the file path

#read whole file to a string
db_endpoint_file_text = db_endpoint_file.read().rstrip('\n')

## Manipulate and concate string
db_endpoint_prefix = "mysql+pymysql://admin:Japassword-1@"
db_uri = db_endpoint_prefix + db_endpoint_file_text.replace(":3306","/f1dbse")

#close file
db_endpoint_file.close()

print(db_uri)

engine = ''

# Create a metadata instance/object
metadata = MetaData()  # Create the Metadata Object

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
        qry='SELECT COUNT(*) FROM '+table_list[0]
        row_count = conn.execute(qry)
        if int(row_count) == 0:
            conn.execute(table_list[0].insert(),[
            {'f1drivername':'Lewis Hamilton','f1wins':'103','status':'Active'},
            {'f1drivername':'Michael Schumacher','f1wins':'91','status':'Retired'}])

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
        # for key, value in form_data.items():
        #     print(f'{key}: {value}')
        sql = "INSERT INTO f1driver_tbl (f1drivername, f1wins, status) VALUES (%s, %s, %s)"
        sql_val=(request.form['F1driver_name'],request.form['F1_wins'],request.form['F1_status'])
        query_result = conn.execute(sql,sql_val)
        print("New Row Inserted")
        return render_template('data.html',form_data = form_data)


    # <p>F1 Driver Name <input type = "text" name = "F1driver_name" /></p>
    # <p>F1 wins <input type = "text" name = "F1_wins" /></p>
    # <p>Status <input type = "text" name = "F1_Status" /></p>
    # <p><input type = "submit" value = "Submit" /></p>
if __name__ == "__main__":
   # app.run(debug=False, host="0.0.0.0", port=3000)
     app.run(debug=False, host='0.0.0.0', port=5000)

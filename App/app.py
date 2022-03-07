
from flask import Flask, render_template
from sqlalchemy import (Column, Integer, MetaData, String, Table,
                        create_engine, inspect)
from sqlalchemy.exc import SQLAlchemyError
app = Flask(__name__,template_folder='../templates')

#Populate AWS DB End Point from rds_endpoint.txt file
db_endpoint_file = open("/home/ec2-user/rds_endpoint.txt", "r")
#db_endpoint_file = open("../rds_endpoint.txt", "r") #<--Uncomment to run locally and update the file path

#read whole file to a string
db_endpoint_file_text = db_endpoint_file.read()

## Manipulate and concate string
db_endpoint_prefix = "mysql+pymysql://admin:Japassword1@"
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
    # engine = create_engine(us_db_uri)
    # metadata.reflect(bind=engine)
    # inspector = inspect(engine)
    # conn = engine.connect()
    # print("US DB Connected--> success")
    # ukdb_flag = False
    

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
            {'f1drivername':'Lewis Hamilton','f1wins':'103','status':'Unknown'},
            {'f1drivername':'Michael Schumacher','f1wins':'91','status':'Retired'}])
    else:
        table_list = inspector.get_table_names()
        print("Table already exists  => ",table_list[0])

tbls = ['f1driver_tbl']  # Provides table /tables to be created
for _t in tbls: create_table(_t, metadata)

# table = metadata.tables['f1driver_tbl']
# select_st = select([table])

# result = conn.execute(select_st)
# print ("rresult",result)
# for _row in result:
#     print("select=>",_row[1])
  
result = engine.execute('SELECT * FROM f1driver_tbl') 

print("Id", "\t", "Driver Name ", "\t", "F1 Wins", "\t", " Status")
for _row in result:
    print(_row[0], "\t", _row[1], "\t", _row[2], "\t", _row[3])   

@app.route("/")
def homepage():
    """View function for Home Page."""
    query_result = engine.execute('SELECT * FROM f1driver_tbl')
    return render_template("home.html", result=query_result)

if __name__ == "__main__":
   # app.run(debug=False, host="0.0.0.0", port=3000)
     app.run(debug=False, host='0.0.0.0', port=5000)

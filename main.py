import mysql.connector
from flask import Flask, render_template, request, redirect, session, url_for
import re
import os 
import logging
import json
import traceback

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'd3d44d57d0125f119f14f7633652d5d0')



import time
from functools import wraps

# from kafka import KafkaProducer
# from confluent_kafka.admin import AdminClient, NewTopic

#  # Kafka producer setup
# producer = KafkaProducer(bootstrap_servers=['localhost:9092'],
#                         value_serializer=lambda v: json.dumps(v).encode('utf-8'))

# def invocation(func):
#     @wraps(func)
#     def wrapper(*args, **kwargs):

#         print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
#         print("Sensor Microagent Launched!")
#         print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")

#         # Retrieve system properties (environment variables)
#         swid = os.getenv("swid", 1)
#         cxid = os.getenv("cxid", 1)

#         # Construct the Kafka topic
#         BASE_TOPIC = "INV"  # Set your base topic here
#         appTopic = f"{BASE_TOPIC}/{swid}_{cxid}"

#         data = {
#             "swid": swid,
#             "cxid": cxid,
#             "callStackId": None,  # Set this if you have a call stack identifier
#             "fullyQualifiedMethodName": f"{func.__module__}.{func.__qualname__}",
#             "params": args,
#             "result": None,
#             "_returns": False,
#             "_returnsString": False,
#             "_returnsNumber": False,
#             "exception": False,
#             "startTime": None,
#             "endTime": None,
#             "executionTime": None,
#             "tag": None,  # Set this if you have a tag
#             "label": None  # Set this if you have a label
#         }

#         start_time = int(time.time() * 1000)
#         data["startTime"] = start_time
        
#         try:
#             result = func(*args, **kwargs)
#             data["result"] = result
#             data["_returns"] = result is not None
#             data["_returnsString"] = isinstance(result, str)
#             data["_returnsNumber"] = isinstance(result, (int, float))
#         except Exception as e:
#             data["exception"] = True
#             data["result"] = str(e)
#             print(f"An exception occurred in {func.__name__}: {e}")
#         finally:
#             end_time = int(time.time() * 1000)
#             data["endTime"] = end_time
#             data["executionTime"] = end_time - start_time
            

#             # Step 3: Define the new topic
#             topic_list = [NewTopic(appTopic, num_partitions=3, replication_factor=1)]
#             # Adjust "my_new_topic", num_partitions, and replication_factor as needed

#             # Send the data to the constructed Kafka topic
#             print(f"Sending data to Kafka topic: {appTopic}")
#             producer.send(appTopic, value=data)
#             producer.flush()
#             print("Data sent successfully!")
            
#             if data["exception"]:
#                 raise
        
#         return result
#     return wrapper

# Don't forget to properly handle Kafka cleanup after usage, e.g.:
# producer.close(timeout=60)



# class JsonFormatter(logging.Formatter):
#     def format(self, record):
#         log_record = {

#             "callStackId": None,  # Set this if you have a call stack identifier
#             "fullyQualifiedMethodName": None,
#             "params": None,
#             "result": None,
#             "_returns": False,
#             "_returnsString": False,
#             "_returnsNumber": False,
#             "exception": False,
#             "startTime": None,
#             "endTime": None,
#             "executionTime": None,
#             "tag": None,  # Set this if you have a tag
#             "label": None  # Set this if you have a label
#         }
#         if record.exc_info:
#             log_record['exception'] = self.formatException(record.exc_info)
#         return json.dumps(log_record)
    
# logging.basicConfig(
#     level=logging.INFO,
#     format='%(swid)s - %(cxid)s - %(callStackId)s - %(fullyQualifiedMethodName)s - %(params)s - %(result)s - %(_returns)s - %(_returnsString)s - %(_returnsNumber)s - %(exception)s - %(startTime)s - %(endTime)s - %(executionTime)s - %(tag)s - %(label)s',
#     handlers=[
#         logging.FileHandler("django_app_json.log"),
#         logging.StreamHandler()
#     ]
# )

# # Get the logger and set the formatter to the JSON formatter for the file handler
# logger = logging.getLogger()
# file_handler = logger.handlers[0]  # Assuming the first handler is the FileHandler
# file_handler.setFormatter(JsonFormatter())

# Function to capture and log request details
@app.before_request
def log_request_info():
    try:
        # Capturing the call stack
        call_stack = traceback.format_stack()

        # Simplifying the call stack for readability
        # You might want to customize this part based on your needs
        simplified_stack = [line.strip() for line in call_stack]

        # Capturing request method and content
        request_info = {
            "call_stack": simplified_stack,
            "method": request.method,
            "data": request.get_data(as_text=True)  # or request.json if expecting JSON
        }

        # Write information to a JSON file
        with open("request_logs.json", "a") as file:
            json.dump(request_info, file)
            file.write("\n")  # Newline for separating entries

    except Exception as e:
        print(f"Error logging request info: {e}")



if __name__ == "__main__":
    app.run(debug=True)


@app.route("/")
def jeniya():
    return render_template("index.html")


@app.route("/home")
def home():
    return render_template('home.html')


@app.route("/aboutus")
def aboutus():
    return render_template('aboutus.html')


@app.route("/order")
def order():
    return render_template('order.html')


@app.route("/profile")
def pf():
    return render_template('profile.html')


@app.route("/adminlogin")
def al():
    return render_template("adminlogin.html")


@app.route("/alogin", methods=["GET", "POST"])
#@invocation
def alogin():
    con = mysql.connector.connect(
        host='localhost',
        user='root',  # Replace 'root' with the appropriate username
        password='Conamieas44',  
        database='jeniyadb'
    )
    cursor = con.cursor()
    msg = ''
    if request.method == 'POST':
        adminname = request.form['adminname']
        password = request.form['password']
        cursor.execute("SELECT * FROM admin WHERE adminname='"+adminname+"' AND password='"+password+"'")
        record = cursor.fetchone()
        if record:
            session['loggedin'] = True
            session['id'] = record[1]
            msg = 'Logged in successfully !'
            return render_template('admin.html', msg=msg)
        else:
            msg = 'Incorrect User/Password, Try again!!'
            return render_template('adminlogin.html', msg=msg)


@app.route("/admin")
#@invocation
def admin():
    con = mysql.connector.connect(
        host='localhost',
        user='root',  # Replace 'root' with the appropriate username
        password='Conamieas44',  # Replace 'your_password' with the correct password
        database='jeniyadb'
    )
    cur = con.cursor()
    sql = "select * from fruit"
    cur.execute(sql)
    result = cur.fetchall()
    return render_template('admin.html')


@app.route("/ManageSellers")

def ms():
    con = mysql.connector.connect(
        host='localhost',
        user='root',  # Replace 'root' with the appropriate username
        password='Conamieas44',  # Replace 'your_password' with the correct password
        database='jeniyadb'
    )
    cur = con.cursor()
    sql = "select * from seller"
    cur.execute(sql)
    result = cur.fetchall()
    return render_template('ManageSellers.html', data=result)


@app.route("/ManageProducts")

def mp():
    return render_template('ManageProducts.html')


@app.route("/afruits")
def afruits():
    con = mysql.connector.connect(
        host='localhost',
        user='root',  # Replace 'root' with the appropriate username
        password='Conamieas44',  # Replace 'your_password' with the correct password
        database='jeniyadb'
    )
    cur = con.cursor()
    sql = "select * from fruit"
    cur.execute(sql)
    result = cur.fetchall()
    return render_template('afruits.html', data=result)


@app.route("/avegetables")
#@invocation
def avegetables():
    con = mysql.connector.connect(
        host='localhost',
        user='root',  # Replace 'root' with the appropriate username
        password='Conamieas44',  # Replace 'your_password' with the correct password
        database='jeniyadb'
    )
    cur = con.cursor()
    sql = "select * from vegetables"
    cur.execute(sql)
    result = cur.fetchall()
    return render_template('avegetables.html', data=result)


@app.route("/ahomemade")
def ahomemade():
    con = mysql.connector.connect(
        host='localhost',
        user='root',  # Replace 'root' with the appropriate username
        password='Conamieas44',  # Replace 'your_password' with the correct password
        database='jeniyadb'
    )
    cur = con.cursor()
    sql = "select * from handmade"
    cur.execute(sql)
    result = cur.fetchall()
    return render_template('ahomemade.html', data=result)


@app.route("/ahandcraft")
def ahandcraft():
    con = mysql.connector.connect(
        host='localhost',
        user='root',  # Replace 'root' with the appropriate username
        password='Conamieas44',  # Replace 'your_password' with the correct password
        database='jeniyadb'
    )
    cur = con.cursor()
    sql = "select * from handcraft"
    cur.execute(sql)
    result = cur.fetchall()
    return render_template('ahandcraft.html', data=result)


@app.route('/fruitsdelete', methods=["POST", "GET"])
#@invocation
def fruitsdelete():
    id=request.args.get("id")
    con = mysql.connector.connect(
        host='localhost',
        user='root',  # Replace 'root' with the appropriate username
        password='Conamieas44',  # Replace 'your_password' with the correct password
        database='jeniyadb'
    )
    cursor = con.cursor()
    cursor.execute("delete FROM fruit WHERE fruit_id='"+id+"'")
    con.commit()
    con.close()
    return redirect(url_for('afruits'))


@app.route('/vegetablesdelete', methods=["POST", "GET"])
#@invocation
def vegetablesdelete():
    id=request.args.get("id")
    con = mysql.connector.connect(
        host='localhost',
        user='root',  # Replace 'root' with the appropriate username
        password='Conamieas44',  # Replace 'your_password' with the correct password
        database='jeniyadb'
    )
    cursor = con.cursor()
    cursor.execute("delete FROM vegetables WHERE vegetable_id='"+id+"'")
    con.commit()
    con.close()
    return redirect(url_for('avegetables'))


@app.route('/homemadedelete', methods=["POST", "GET"])
#@invocation
def homemadedelete():
    id=request.args.get("id")
    con = mysql.connector.connect(
        host='localhost',
        user='root',  # Replace 'root' with the appropriate username
        password='Conamieas44',  # Replace 'your_password' with the correct password
        database='jeniyadb'
    )
    cursor = con.cursor()
    cursor.execute("delete FROM handmade WHERE handmade_id='"+id+"'")
    con.commit()
    con.close()
    return redirect(url_for('ahandmade'))


@app.route('/handcraftdelete', methods=["POST", "GET"])
#@invocation
def handcraftdelete():
    id=request.args.get("id")
    con = mysql.connector.connect(
        host='localhost',
        user='root',  # Replace 'root' with the appropriate username
        password='Conamieas44',  # Replace 'your_password' with the correct password
        database='jeniyadb'
    )
    cursor = con.cursor()
    cursor.execute("delete FROM handcraft WHERE handcraft_id='"+id+"'")
    con.commit()
    con.close()
    return redirect(url_for('ahandcraft'))


@app.route('/sellerdelete', methods=["POST", "GET"])
#@invocation
def sellerdelete():
    id=request.args.get("id")
    con = mysql.connector.connect(
        host='localhost',
        user='root',  # Replace 'root' with the appropriate username
        password='Conamieas44',  # Replace 'your_password' with the correct password
        database='jeniyadb'
    )
    cursor = con.cursor()
    cursor.execute("delete FROM seller WHERE seller_id='"+id+"'")
    con.commit()
    con.close()
    return redirect(url_for('ManageSellers'))


@app.route("/sellerlogin")
def sl():
    return render_template("sellerlogin.html")


@app.route("/Productdetails")
def pd():
    con = mysql.connector.connect(
        host='localhost',
        user='root',  # Replace 'root' with the appropriate username
        password='Conamieas44',  # Replace 'your_password' with the correct password
        database='jeniyadb'
    )
    cur = con.cursor()
    sql = "select * from fruit"
    cur.execute(sql)
    result = cur.fetchall()
    return render_template("Productdetails.html", data=result)


@app.route("/addproducts", methods=['GET', 'POST'])
#@invocation
def addproducts():
    con = mysql.connector.connect(
        host='localhost',
        user='root',  # Replace 'root' with the appropriate username
        password='Conamieas44',  # Replace 'your_password' with the correct password
        database='jeniyadb'
    )
    cursor = con.cursor()
    if request.method == 'POST':
        fruit_name = request.form['fruit_name']
        fruit_weight = request.form['fruit_weight']
        fruit_rate = request.form['fruit_rate']
        fruit_desc = request.form['fruit_desc']
        fruit_image = request.form['fruit_image']
        cursor.execute("INSERT INTO fruit (fruit_name, fruit_weight, fruit_rate, fruit_desc, fruit_image) VALUES ('" + fruit_name + "','" + fruit_weight + "','" + fruit_rate + "','" + fruit_desc + "', '" + fruit_image + "')")
        con.commit()
        return render_template('Productdetails.html')
    else:
        return render_template("addproducts.html")

#@invocation
@app.route("/SellerAccInfo", methods=["POST", "GET"])
def sellerinfo():
    con = mysql.connector.connect(
        host='localhost',
        user='root',  # Replace 'root' with the appropriate username
        password='Conamieas44',  # Replace 'your_password' with the correct password
        database='jeniyadb'
    )
    cur = con.cursor()
    sellername = request.form['sellername']
    password = request.form['password']
    email=request.form['email']
    address=request.form['address']
    delivery=request.form['delivery']
    sql = ("UPDATE seller (sellername, password, email, firstname, lastname) SET ('" + sellername + "', '" + password + "','" + email + "','" + address + "','"+delivery+"')")
    cur.execute(sql)
    result = cur.fetchall()
    return render_template("SellerAccInfo.html", data=result)


@app.route("/sorder")
def sorder():
    con = mysql.connector.connect(
        host='localhost',
        user='root',  # Replace 'root' with the appropriate username
        password='Conamieas44',  # Replace 'your_password' with the correct password
        database='jeniyadb'
    )
    cur = con.cursor()
    sql = "select * from order"
    cur.execute(sql)
    result = cur.fetchall()
    return render_template("sorder.html", data=result)



@app.route("/contactus")
def contactus():
    return render_template("contactus.html")


@app.route("/slogin", methods=["GET", "POST"])
#@invocation
def slogin():
    con = mysql.connector.connect(
        host='localhost',
        user='root',  # Replace 'root' with the appropriate username
        password='Conamieas44',  # Replace 'your_password' with the correct password
        database='jeniyadb'
    )
    cursor = con.cursor()
    msg = ''
    if request.method == 'POST':
        sellername = request.form['sellername']
        password = request.form['password']
        cursor.execute("SELECT * FROM seller WHERE sellername='"+sellername+"' AND password='"+password+"'")
        record = cursor.fetchone()
        if record:
            session['loggedin'] = True
            session['id'] = record[1]
            msg = 'Logged in successfully !'
            return render_template('seller.html', msg=msg)
        else:
            msg = 'Incorrect User/Password, Try again!!'
            return render_template('sellerlogin.html', msg=msg)


@app.route("/seller")
def seller():
    return render_template('seller.html')


@app.route('/productsdelete', methods=["POST", "GET"])
#@invocation
def productsdelete():
    id = request.args.get("id")
    con = mysql.connector.connect(
        host='localhost',
        user='root',  # Replace 'root' with the appropriate username
        password='Conamieas44',  # Replace 'your_password' with the correct password
        database='jeniyadb'
    )
    cursor = con.cursor()
    cursor.execute("delete FROM fruit WHERE fruit_id='"+id+"'")
    con.commit()
    con.close()
    return redirect(url_for('pd'))


@app.route("/login", methods=["GET", "POST"])
#@invocation
def login():
    con = mysql.connector.connect(
        host='localhost',
        user='root',  # Replace 'root' with the appropriate username
        password='Conamieas44',  # Replace 'your_password' with the correct password
        database='jeniyadb'
    )
    cursor = con.cursor()
    msg = ''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cursor.execute("SELECT * FROM user WHERE username='"+username+"' AND password='"+password+"'")
        record = cursor.fetchone()
        if record:
            session['loggedin'] = True
            session['id'] = record[1]
            msg = 'Logged in successfully !'
            return render_template('home.html', msg=msg)
        else:
            msg = 'Incorrect User/Password, Try again!!'
            return render_template('index.html', msg=msg)


@app.route('/registration', methods=['GET', 'POST'])
#@invocation
def registration():
    con = mysql.connector.connect(
        host='localhost',
        user='root',  # Replace 'root' with the appropriate username
        password='Conamieas44',  
        database='jeniyadb'
    )
    cursor = con.cursor()
    msg = ''
    
    # Log the request method
    logging.info(f"Request method: {request.method}")
    
    if request.method == 'POST':
        # Extract form data
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        
        # Log extracted form data
        #logging.info(f"Form data - Username: {username}, Password: {password}, Email: {email}, Firstname: {firstname}, Lastname: {lastname}")
        params = {
            "username": username,
            "password": password,
            "email": email,
            "firstname": firstname,
            "lastname": lastname
        }
        #logger.info(registration.__func__.__name__  ,extra={'params':params})
        # Execute parameterized query to prevent SQL injection
        query = "INSERT INTO user (username, password, email, firstname, lastname) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(query, (username, password, email, firstname, lastname))
        
        con.commit()
        
        msg = 'You have successfully registered !'
        
        # Log successful registration
        # logging.info(msg)
        
        return render_template('index.html', msg=msg)
    else:
        msg = 'Please fill out the form !'
        
        # Log form not filled
        # logging.info(msg)
    
    return render_template('registration.html', msg=msg)

@app.route("/fruits")
def jeniya2():
    con = mysql.connector.connect(
        host='localhost',
        user='root',  # Replace 'root' with the appropriate username
        password='Conamieas44',  
        database='jeniyadb'
    )
    cur = con.cursor()
    sql = "select * from fruit"
    cur.execute(sql)
    result = cur.fetchall()
    return render_template("fruits.html", data=result)


@app.route("/vegetables")
def jeniya3():
    con = mysql.connector.connect(
        host='localhost',
        user='root',  # Replace 'root' with the appropriate username
        password='Conamieas44',  # Replace 'your_password' with the correct password
        database='jeniyadb'
    )
    cur = con.cursor()
    sql = "select * from vegetables"
    cur.execute(sql)
    result = cur.fetchall()
    return render_template("vegetables.html", data=result)


@app.route("/homemade")
def jeniya4():
    con = mysql.connector.connect(
        host='localhost',
        user='root',  # Replace 'root' with the appropriate username
        password='Conamieas44',  # Replace 'your_password' with the correct password
        database='jeniyadb'
    )
    cur = con.cursor()
    sql = "select * from handmade"
    cur.execute(sql)
    result = cur.fetchall()
    return render_template("homemade.html", data=result)


@app.route("/handcraft")
def jeniya5():
    con = mysql.connector.connect(
        host='localhost',
        user='root',  # Replace 'root' with the appropriate username
        password='Conamieas44',  # Replace 'your_password' with the correct password
        database='jeniyadb'
    )
    cur = con.cursor()
    sql = "select * from handcraft"
    cur.execute(sql)
    result = cur.fetchall()
    return render_template("handcraft.html", data=result)


@app.route("/addtocart")
def atd():
    con = mysql.connector.connect(
        host='localhost',
        user='root',  # Replace 'root' with the appropriate username
        password='Conamieas44',  # Replace 'your_password' with the correct password
        database='jeniyadb'
    )
    cur = con.cursor()
    sql = "select * from cart"
    cur.execute(sql)
    result = cur.fetchall()
    return render_template("addtocart.html", data=result)


@app.route("/addtocartSave", methods=["POST", "GET"])
def addtocart():
    id = request.args.get("id")
    con = mysql.connector.connect(
        host='localhost',
        user='root',  # Replace 'root' with the appropriate username
        password='Conamieas44',  
        database='jeniyadb'
    )
    cursor1 = con.cursor1()
    cursor1.execute("SELECT* FROM fruit where fruit_id='"+id+"'")
    record = cursor1.fetchone()
    cursor = con.cursor()
    cursor.execute("insert into cart(user_id , fruit_id , fruit_weight, quantity , fruit_desc ) values('44', '"+session['id']+"', '"+record[0]+"','"+record[2]+"','2','"+record[4]+"')")
    con.commit()
    return render_template("addtocart.html")


@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('username', None)
    return render_template("index.html")


if __name__ == '__main__':
   app.run(debug=True)

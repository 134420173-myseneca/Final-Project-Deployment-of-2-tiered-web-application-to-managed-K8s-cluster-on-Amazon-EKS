from flask import Flask, render_template, request, url_for
from pymysql import connections
import os
import random
import argparse
import boto3
import botocore
import logging
from botocore.exceptions import NoCredentialsError, ClientError

app = Flask(__name__)

DBPORT_str = os.environ.get("DBPORT")
DBPORT = int(DBPORT_str) if DBPORT_str else 3306
DBHOST = os.environ.get("DBHOST") or "localhost"
DBUSER = os.environ.get("DBUSER") or "root"
DBPWD = os.environ.get("DBPWD") or "passwors"
DATABASE = os.environ.get("DATABASE") or "employees"
COLOR_FROM_ENV = os.environ.get("APP_COLOR") or "lime"
#image_file_name = os.environ.get("image_file_name") or "background_image.jpg"
image_file_name = os.environ.get("IMAGE_FILE_NAME") 
bucket_name = os.environ.get("BUCKET_NAME") or "clo835-group9"
#group_name = os.environ.get("GROUP_NAME") or "Group9"
group_name = os.environ.get("GROUP_NAME")
#group_slogan = os.environ.get("GROUP_SLOGAN") or "Anything can happen with a good team"
group_slogan = os.environ.get("GROUP_SLOGAN")
#image_url = os.environ.get("IMAGE_URL") or "https://clo835-group9.s3.amazonaws.com/background_image.jpg"
image_url = os.environ.get("IMAGE_URL")
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_SESSION_TOKEN = os.getenv("AWS_SESSION_TOKEN", None)


#Create a connection to the 

db_conn = connections.Connection(
    host= DBHOST,
    port=DBPORT,
    user= DBUSER,
    password= DBPWD, 
    db= DATABASE
    
)

output = {}
table = 'employee'

color_codes = {
    "red": "#e74c3c",
    "green": "#16a085",
    "blue": "#89CFF0",
    "blue2": "#30336b",
    "pink": "#f4c2c2",
    "darkblue": "#130f40",
    "lime": "#C1FF9C",
}

SUPPORTED_COLORS = ",".join(color_codes.keys())

# function to get image from private s3 bucket and dowwnlaod locally
def download_background_image(bucket_name, image_file_name):
    try:
        # Create 'static' directory if it doesn't exist
        if not os.path.exists('static'):
            os.makedirs('static')

        s3_client = boto3.client(
            's3',
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
            aws_session_token=AWS_SESSION_TOKEN
        )

        # Get the list of objects in the bucket
        response = s3_client.list_objects_v2(Bucket=bucket_name)
        
        # Search for the image file in the bucket
        object_key = None
        for obj in response.get('Contents', []):
            if obj['Key'].endswith(image_file_name):
                object_key = obj['Key']
                break

        if object_key:
            local_filename = os.path.join("static", "background_image.jpg")
            s3_client.download_file(bucket_name, object_key, local_filename)
            print("Background image downloaded successfully from S3.")
            # Added logging of background image location
            bucket = bucket_name
            object_name = image_file_name
            logging.basicConfig(level=logging.INFO)
            image_url = f"https://{bucket}.s3.amazonaws.com/{object_name}"
            logging.info(" Background Image URL for Group9 for CLO835---> %s", image_url)

           
            
            return local_filename
        else:
            print("Image file not found in the bucket:", image_file_name)
            return None
    except Exception as e:
        print("Error downloading background image:", e)
        return None

@app.route("/download_image", methods=['GET', 'POST'])
def download_image_route():
    image_file_path = download_background_image(bucket_name, image_file_name)
    return image_file_path or "Error: Failed to download image."

@app.route("/", methods=['GET', 'POST'])
def home():
    try:
        image_file_path = download_image_route()
        print(image_file_path)
        return render_template('addemp.html', background_image=image_file_path, group_name=group_name, group_slogan=group_slogan, image_url=image_url)
    except Exception as e:
        print(f"An error occurred while rendering the homepage: {e}")
        return "Error: Failed to render homepage."


@app.route("/about", methods=['GET','POST'])
def about():
    try:
        image_file_path = download_image_route()
        s3 = boto3.client('s3')
        response = s3.list_buckets()
        if response:
            buckets = [bucket["Name"] for bucket in response['Buckets']]
            print('Buckets exist..')
            for bucket in buckets:
                print(f'  {bucket}')
    except Exception as e:
        logging.error(e)
        return render_template('error.html', error_message="Error occurred while fetching buckets") 
    return render_template('about.html', buckets=buckets, background_image=image_file_path, group_name=group_name, group_slogan=group_slogan)
    
@app.route("/addemp", methods=['POST'])
def AddEmp():
    emp_id = request.form['emp_id']
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    primary_skill = request.form['primary_skill']
    location = request.form['location']
    
    insert_sql = "INSERT INTO employee VALUES (%s, %s, %s, %s, %s)"
    cursor = db_conn.cursor()

    try:
        cursor.execute(insert_sql, (emp_id, first_name, last_name, primary_skill, location))
        db_conn.commit()
        emp_name = "" + first_name + " " + last_name
    finally:
        cursor.close()

    print("all modification done...")

    image_file_path = download_image_route()
    return render_template('addempoutput.html', background_image=image_file_path, name=emp_name , group_name=group_name, group_slogan=group_slogan, image_url=image_url)
    
@app.route("/getemp", methods=['GET', 'POST'])
def GetEmp():
    image_file_path = download_image_route()
    return render_template("getemp.html", background_image=image_file_path, group_name=group_name, group_slogan=group_slogan, image_url=image_url)
    

@app.route("/fetchdata", methods=['GET', 'POST'])
def FetchData():
    emp_id = request.form['emp_id']

    output = {}
    select_sql = "SELECT emp_id, first_name, last_name, primary_skill, location from employee where emp_id=%s"
    cursor = db_conn.cursor()

    try:
        cursor.execute(select_sql, (emp_id))
        result = cursor.fetchone()

        output["emp_id"] = result[0]
        output["first_name"] = result[1]
        output["last_name"] = result[2]
        output["primary_skills"] = result[3]
        output["location"] = result[4]

    except Exception as e:
        print(e)
    finally:
        cursor.close()
    image_file_path = download_image_route()
    return render_template("getempoutput.html", id=output["emp_id"], fname=output["first_name"],
                          lname=output["last_name"], interest=output["primary_skills"],
                          location=output["location"], background_image=image_file_path,group_name=group_name, group_slogan=group_slogan, image_url=image_url)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=81, debug=True)




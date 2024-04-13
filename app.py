from flask import Flask, render_template, request, url_for
from pymysql import connections
import os
import random
import argparse
import boto3
from botocore.exceptions import NoCredentialsError, ClientError
import logging


app = Flask(__name__)

DBHOST = os.environ.get("DBHOST") or "localhost"
DBUSER = os.environ.get("DBUSER") or "root"
DBPWD = os.environ.get("DBPWD") or "passwors"
DATABASE = os.environ.get("DATABASE") or "employees"
COLOR_FROM_ENV = os.environ.get('APP_COLOR') or "lime"
BACKGROUND_IMAGE = os.environ.get("BACKGROUND_IMAGE") or "Invalid Image been passed"
GROUP_NAME = os.environ.get('GROUP_NAME') or "GROUP9"
DBPORT = int(os.environ.get("DBPORT"))

# Create a connection to the MySQL database
db_conn = connections.Connection(
    host= DBHOST,
    port=DBPORT,
    user= DBUSER,
    password= DBPWD, 
    db= DATABASE
    
)
output = {}
table = 'employee';

# Define the supported color codes
color_codes = {
    "red": "#e74c3c",
    "green": "#16a085",
    "blue": "#89CFF0",
    "blue2": "#30336b",
    "pink": "#f4c2c2",
    "darkblue": "#130f40",
    "lime": "#C1FF9C",
}


# Create a string of supported colors
SUPPORTED_COLORS = ",".join(color_codes.keys())

# Generate a random color
COLOR = random.choice(["red", "green", "blue", "blue2", "darkblue", "pink", "lime"])

AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
AWS_S3_BUCKET = os.environ.get("AWS_S3_BUCKET")
BACKGROUND_IMAGE_KEY = os.environ.get("BACKGROUND_IMAGE_KEY")


@app.route("/", methods=['GET', 'POST'])
def home():
    background_image_url = download_background_image()
    return render_template('addemp.html', background_image=background_image_url, color=color_codes[COLOR])

def download_background_image():
    """Download the background image from the S3 bucket and return the local URL."""
    # Check if all required environment variables are set
    if not all([AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_S3_BUCKET, BACKGROUND_IMAGE_KEY]):
        print("Required AWS environment variables are not set.")
        return url_for('static', filename='default_background.png')  # You should have a default image
    s3_client = boto3.client(
        's3',
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY
        # Session token is not needed unless you are using temporary credentials
    )
    local_filename = 'static/background_image.png'
    try:
        s3_client.download_file(AWS_S3_BUCKET, BACKGROUND_IMAGE_KEY, local_filename)
        print("Background image downloaded successfully from S3.")
    except NoCredentialsError:
        print("Credentials not available for downloading the background image.")
        return url_for('static', filename='default_background.png')  # Fallback to a default image
    except ClientError as e:
        if e.response['Error']['Code'] == '404':
            print("The background image does not exist in the bucket.")
        else:
            print(f"Client error occurred: {e}")
        return url_for('static', filename='default_background.png')  # Fallback to a default image
    except Exception as e:
        print(f"Error downloading background image: {e}")
        return url_for('static', filename='default_background.png')  # Fallback to a default image

    return url_for('static', filename='background_image.png')


@app.route("/about", methods=['GET','POST'])
def about():
    return render_template('about.html', color=color_codes[COLOR])
    
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
        
        cursor.execute(insert_sql,(emp_id, first_name, last_name, primary_skill, location))
        db_conn.commit()
        emp_name = "" + first_name + " " + last_name

    finally:
        cursor.close()

    print("all modification done...")
    return render_template('addempoutput.html', name=emp_name, color=color_codes[COLOR])

@app.route("/getemp", methods=['GET', 'POST'])
def GetEmp():
    return render_template("getemp.html", color=color_codes[COLOR])


@app.route("/fetchdata", methods=['GET','POST'])
def FetchData():
    emp_id = request.form['emp_id']

    output = {}
    select_sql = "SELECT emp_id, first_name, last_name, primary_skill, location from employee where emp_id=%s"
    cursor = db_conn.cursor()

    try:
        cursor.execute(select_sql,(emp_id))
        result = cursor.fetchone()
        
        # Add No Employee found form
        output["emp_id"] = result[0]
        output["first_name"] = result[1]
        output["last_name"] = result[2]
        output["primary_skills"] = result[3]
        output["location"] = result[4]
        
    except Exception as e:
        print(e)

    finally:
        cursor.close()

    return render_template("getempoutput.html", id=output["emp_id"], fname=output["first_name"],
                           lname=output["last_name"], interest=output["primary_skills"], location=output["location"], color=color_codes[COLOR])

if __name__ == '__main__':
    
    # Check for Command Line Parameters for color
    parser = argparse.ArgumentParser()
    parser.add_argument('--color', required=False)
    args = parser.parse_args()

    if args.color:
        print("Color from command line argument =" + args.color)
        COLOR = args.color
        if COLOR_FROM_ENV:
            print("A color was set through environment variable -" + COLOR_FROM_ENV + ". However, color from command line argument takes precendence.")
    elif COLOR_FROM_ENV:
        print("No Command line argument. Color from environment variable =" + COLOR_FROM_ENV)
        COLOR = COLOR_FROM_ENV
    else:
        print("No command line argument or environment variable. Picking a Random Color =" + COLOR)

    # Check if input color is a supported one
    if COLOR not in color_codes:
        print("Color not supported. Received '" + COLOR + "' expected one of " + SUPPORTED_COLORS)
        exit(1)

    app.run(host='0.0.0.0',port=81,debug=True)

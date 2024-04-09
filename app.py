from flask import Flask, render_template, request, url_for
from pymysql import connections
import os
import random
import argparse
import boto3
import logging
import botocore

app = Flask(__name__)

DBHOST = os.environ.get("DBHOST") or "localhost"
DBUSER = os.environ.get("DBUSER") or "root"
DBPWD = os.environ.get("DBPWD") or "passwors"
DATABASE = os.environ.get("DATABASE") or "employees"
COLOR_FROM_ENV = os.environ.get('APP_COLOR') or "lime"
BACKGROUND_IMAGE = os.environ.get("BACKGROUND_IMAGE") or "Invalid Image been passed"
GROUP_NAME = os.environ.get('GROUP_NAME') or "GROUP9"
#DBPORT = int(os.environ.get("DBPORT"))

# Create a connection to the MySQL database
# db_conn = connections.Connection(
#     host= DBHOST,
#     port=DBPORT,
#     user= DBUSER,
#     password= DBPWD, 
#     db= DATABASE
    
# )
# output = {}
# table = 'employee';

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

# Read the list of existing buckets
# def list_bucket():
#     # Create bucket
#     try:
#         s3 = boto3.client('s3')
#         response = s3.list_buckets()
#         if response:
#             print('Buckets exists..')
#             for bucket in response['Buckets']:
#                 print(f'  {bucket["Name"]}')
#     except Exception as e:
#         logging.error(e)
#         return False
#     return True
    
#     list_bucket()



@app.route("/", methods=['GET', 'POST'])
def home():
    return render_template('addemp.html', color=color_codes[COLOR])
    
from flask import render_template
import boto3
import logging

from flask import render_template

@app.route("/about", methods=['GET','POST'])
def about():
    try:
        s3 = boto3.client('s3')
        response = s3.list_buckets()
        if response:
            buckets = [bucket["Name"] for bucket in response['Buckets']]
            print('Buckets exist..')
            for bucket in buckets:
                print(f'  {bucket}')
    except Exception as e:
        logging.error(e)
        return render_template('error.html', error_message="Error occurred while fetching buckets")  # Return an error template or handle the error appropriately

    # Call the download function to get the image URL
    image_url = download("background_image.png")  # Replace "background_image.png" with the actual file name in S3
    
    # Assuming you have defined color_codes and COLOR somewhere in your code
    color = color_codes[COLOR]

    return render_template('about.html', buckets=buckets, color=color, background_image=image_url)

# Define the download function to get the S3 URL of the image
def download(object_name):
    try:
        s3 = boto3.client('s3')
        bucket_name = 'clo835-group9'  # Replace 'your_bucket_name' with the actual bucket name
        #https://clo835-group9.s3.amazonaws.com/background_image.png
        image_url = f"https://{bucket_name}.s3.amazonaws.com/{object_name}"
        #prints the bucket name which is clo835-group9
        print(bucket_name) 
        #prints the image name which is background_image.png
        print(bucket_name) 
        print(object_name)  
        print("Background Image Location ---> " + image_url) # Added for Logging of Background Image Path
        return image_url
    except Exception as e:
        logging.error(e)
        return None


# @app.route("/about", methods=['GET','POST'])
# def about():
#     try:
#         s3 = boto3.client('s3')
#         response = s3.list_buckets()
#         if response:
#             buckets = [bucket["Name"] for bucket in response['Buckets']]
#             print('Buckets exist..')
#             for bucket in buckets:
#                 print(f'  {bucket}')
#     except Exception as e:
#         logging.error(e)
#         return render_template('error.html', error_message="Error occurred while fetching buckets")  # Return an error template or handle the error appropriately

#     # Assuming you have defined color_codes and COLOR somewhere in your code
#     return render_template('about.html', buckets=buckets, color=color_codes[COLOR])
    
#     return render_template('about.html', background_image = image_url, group_name = GROUP_NAME)
# # @app.route("/download", methods=['GET','POST'])    
# # def download_file(file_name, bucket):
# #     # """
# #     # Function to download a given file from an S3 bucket
# #     # """
    
# #     s3 = boto3.resource('s3')
# #     output = f"downloads/{file_name}"
# #     s3.Bucket(bucket).download_file(file_name, output)

# #     return output
    
# def download(image_url):
#   try:
#          bucket = image_url.split('//')[1].split('.')[0]
#          object_name = '/'.join(image_url.split('//')[1].split('/')[1:])
#          print(bucket)  # prints 'privatebucketclo835'
#          print(object_name)  # prints 'minionparty.png'
#          print("Background Image Location --->" + image_url) # Added for Logging of Background Image Path
#          s3 = boto3.resource('s3')
#          output_dir = "static"
#          if not os.path.exists(output_dir):
#                  os.makedirs(output_dir)
#          output = os.path.join(output_dir, "background_image.png")
#          s3.Bucket(bucket).download_file(object_name, output)

#          return output

#   except botocore.exceptions.ClientError as e:
#                 if e.response['Error']['Code'] == "404":
#                     print("The object does not exist.")
#                 else:
#                     raise

    
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
    
        image_url = url_for('static', filename='background_image.png')

        return render_template("getemp.html", background_image = image_url, color=color_codes[COLOR])


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

    app.run(host='0.0.0.0',port=8081,debug=True)

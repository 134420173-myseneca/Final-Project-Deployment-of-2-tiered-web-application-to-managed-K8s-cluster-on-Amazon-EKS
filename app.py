# from flask import Flask, render_template, request, url_for
# from pymysql import connections
# import os
# import random
# import argparse
# import boto3
# import logging
# import botocore


# app = Flask(__name__)

# DBHOST = os.environ.get("DBHOST") or "localhost"
# DBUSER = os.environ.get("DBUSER") or "root"
# DBPWD = os.environ.get("DBPWD") or "passwors"
# DATABASE = os.environ.get("DATABASE") or "employees"
# COLOR_FROM_ENV = os.environ.get('APP_COLOR') or "lime"
# BACKGROUND_IMAGE = os.environ.get("BACKGROUND_IMAGE") or "Invalid Image been passed"
# GROUP_NAME = os.environ.get('GROUP_NAME') or "GROUP9"
# DBPORT = int(os.environ.get("DBPORT"))

# #Create a connection to the MySQL database
# db_conn = connections.Connection(
#     host= DBHOST,
#     port=DBPORT,
#     user= DBUSER,
#     password= DBPWD, 
#     db= DATABASE
    
# )
# output = {}
# table = 'employee';

# # Define the supported color codes
# color_codes = {
#     "red": "#e74c3c",
#     "green": "#16a085",
#     "blue": "#89CFF0",
#     "blue2": "#30336b",
#     "pink": "#f4c2c2",
#     "darkblue": "#130f40",
#     "lime": "#C1FF9C",
# }


# # Create a string of supported colors
# SUPPORTED_COLORS = ",".join(color_codes.keys())

# # Generate a random color
# COLOR = random.choice(["red", "green", "blue", "blue2", "darkblue", "pink", "lime"])

# # Read the list of existing buckets
# # def list_bucket():
# #     # Create bucket
# #     try:
# #         s3 = boto3.client('s3')
# #         response = s3.list_buckets()
# #         if response:
# #             print('Buckets exists..')
# #             for bucket in response['Buckets']:
# #                 print(f'  {bucket["Name"]}')
# #     except Exception as e:
# #         logging.error(e)
# #         return False
# #     return True
    
# #     list_bucket()



# @app.route("/", methods=['GET', 'POST'])
# def home():
#   # return render_template('addemp.html', color=color_codes[COLOR])
#   #  print('show me the background image url',BACKGROUND_IMAGE)
#   # image_url = url_for('static', filename='background_image.png')
#     image_url = download("background_image.png") 
#     return render_template('addemp.html', background_image = image_url, group_name = GROUP_NAME)
    

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

#     # Call the download function to get the image URL
#     image_url = download("background_image.png")  # Replace "background_image.png" with the actual file name in S3
    
#     # Assuming you have defined color_codes and COLOR somewhere in your code
#     color = color_codes[COLOR]

#     return render_template('about.html', buckets=buckets, color=color, background_image=image_url)

# # Define the download function to get the S3 URL of the image
# def download(object_name):
#     try:
#         s3 = boto3.client('s3')
#         bucket_name = 'clo835-group9'  # Replace 'your_bucket_name' with the actual bucket name
#         #https://clo835-group9.s3.amazonaws.com/background_image.png
#         image_url = f"https://{bucket_name}.s3.amazonaws.com/{object_name}"
#         #prints the bucket name which is clo835-group9
#         print(bucket_name) 
#         #prints the image name which is background_image.png
#         print(bucket_name) 
#         print(object_name)  
#         print("Background Image Location ---> " + image_url) # Added for Logging of Background Image Path
#         return image_url
#     except Exception as e:
#         logging.error(e)
#         return None


# # @app.route("/about", methods=['GET','POST'])
# # def about():
# #     try:
# #         s3 = boto3.client('s3')
# #         response = s3.list_buckets()
# #         if response:
# #             buckets = [bucket["Name"] for bucket in response['Buckets']]
# #             print('Buckets exist..')
# #             for bucket in buckets:
# #                 print(f'  {bucket}')
# #     except Exception as e:
# #         logging.error(e)
# #         return render_template('error.html', error_message="Error occurred while fetching buckets")  # Return an error template or handle the error appropriately

# #     # Assuming you have defined color_codes and COLOR somewhere in your code
# #     return render_template('about.html', buckets=buckets, color=color_codes[COLOR])
    
# #     return render_template('about.html', background_image = image_url, group_name = GROUP_NAME)
# # # @app.route("/download", methods=['GET','POST'])    
# # # def download_file(file_name, bucket):
# # #     # """
# # #     # Function to download a given file from an S3 bucket
# # #     # """
    
# # #     s3 = boto3.resource('s3')
# # #     output = f"downloads/{file_name}"
# # #     s3.Bucket(bucket).download_file(file_name, output)

# # #     return output
    
# # def download(image_url):
# #   try:
# #          bucket = image_url.split('//')[1].split('.')[0]
# #          object_name = '/'.join(image_url.split('//')[1].split('/')[1:])
# #          print(bucket)  # prints 'privatebucketclo835'
# #          print(object_name)  # prints 'minionparty.png'
# #          print("Background Image Location --->" + image_url) # Added for Logging of Background Image Path
# #          s3 = boto3.resource('s3')
# #          output_dir = "static"
# #          if not os.path.exists(output_dir):
# #                  os.makedirs(output_dir)
# #          output = os.path.join(output_dir, "background_image.png")
# #          s3.Bucket(bucket).download_file(object_name, output)

# #          return output

# #   except botocore.exceptions.ClientError as e:
# #                 if e.response['Error']['Code'] == "404":
# #                     print("The object does not exist.")
# #                 else:
# #                     raise

    
# @app.route("/addemp", methods=['POST'])
# def AddEmp():
#     emp_id = request.form['emp_id']
#     first_name = request.form['first_name']
#     last_name = request.form['last_name']
#     primary_skill = request.form['primary_skill']
#     location = request.form['location']

  
#     insert_sql = "INSERT INTO employee VALUES (%s, %s, %s, %s, %s)"
#     cursor = db_conn.cursor()

#     try:
        
#         cursor.execute(insert_sql,(emp_id, first_name, last_name, primary_skill, location))
#         db_conn.commit()
#         emp_name = "" + first_name + " " + last_name

#     finally:
#         cursor.close()
        
        
    

#     print("all modification done...")
    
    
#         image_url = download("background_image.png") 
#         return render_template('addempoutput.html', background_image = image_url, name=emp_name)

# @app.route("/getemp", methods=['GET', 'POST'])
# def GetEmp():
    
#       # image_url = url_for('static', filename='background_image.png')
#         image_url = download("background_image.png") 
#         return render_template("getemp.html", background_image = image_url, group_name = GROUP_NAME)


# @app.route("/fetchdata", methods=['GET','POST'])
# def FetchData():
#     emp_id = request.form['emp_id']

#     output = {}
#     select_sql = "SELECT emp_id, first_name, last_name, primary_skill, location from employee where emp_id=%s"
#     cursor = db_conn.cursor()

#     try:
#         cursor.execute(select_sql,(emp_id))
#         result = cursor.fetchone()
        
#         # Add No Employee found form
#         output["emp_id"] = result[0]
#         output["first_name"] = result[1]
#         output["last_name"] = result[2]
#         output["primary_skills"] = result[3]
#         output["location"] = result[4]
        
#     except Exception as e:
#         print(e)

#     finally:
#         cursor.close()

#     return render_template("getempoutput.html", id=output["emp_id"], fname=output["first_name"],
#                           lname=output["last_name"], interest=output["primary_skills"], location=output["location"], color=color_codes[COLOR])

# if __name__ == '__main__':
    
#     # Check for Command Line Parameters for color
#     parser = argparse.ArgumentParser()
#     parser.add_argument('--color', required=False)
#     args = parser.parse_args()

#     if args.color:
#         print("Color from command line argument =" + args.color)
#         COLOR = args.color
#         if COLOR_FROM_ENV:
#             print("A color was set through environment variable -" + COLOR_FROM_ENV + ". However, color from command line argument takes precendence.")
#     elif COLOR_FROM_ENV:
#         print("No Command line argument. Color from environment variable =" + COLOR_FROM_ENV)
#         COLOR = COLOR_FROM_ENV
#     else:
#         print("No command line argument or environment variable. Picking a Random Color =" + COLOR)

#     # Check if input color is a supported one
#     if COLOR not in color_codes:
#         print("Color not supported. Received '" + COLOR + "' expected one of " + SUPPORTED_COLORS)
#         exit(1)

#     app.run(host='0.0.0.0',port=8081,debug=True)

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
image_file_name = os.environ.get("image_file_name") or "background_image.jpg"
bucket_name = os.environ.get("BUCKET_NAME") or "clo835-group9"
group_name = os.environ.get("GROUP_NAME") or "Group9"
group_slogan = os.environ.get("GROUP_SLOGAN") or "Anything can happen with a good team"
image_url = os.environ.get("IMAGE_URL") or "https://clo835-group9.s3.amazonaws.com/background_image.jpg"
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_SESSION_TOKEN = os.getenv("AWS_SESSION_TOKEN", None)


#Create a connection to the MySQL database

# db_conn = connections.Connection(
#     host= DBHOST,
#     port=DBPORT,
#     user= DBUSER,
#     password= DBPWD, 
#     db= DATABASE
    
# )

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
            local_filename = os.path.join("static", "background_image.png")
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
        return render_template('error.html', error_message="Error occurred while fetching buckets")  # Return an error template or handle the error appropriately

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
    app.run(host='0.0.0.0', port=8080, debug=True)


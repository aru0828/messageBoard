from flask import Blueprint, request,jsonify
import mysql.connector
from pool import closePool, conncetPool
from mysql.connector import pooling
from dotenv import load_dotenv
import os 
import boto3
load_dotenv()


# Let's use Amazon S3
s3 = boto3.client('s3',
         aws_access_key_id=os.getenv('S3_KEY'),
         aws_secret_access_key= os.getenv('S3_SECRET'))


messageAPI = Blueprint('messageAPI', __name__)



@messageAPI.route('/api/message', methods=['POST'])

def POSTmessage(): 
    mydb = conncetPool.get_connection()
    mycursor = mydb.cursor(dictionary=True)
    file = request.files['file']
    text = request.form.get('text')


    # 將圖片新增到s3後回傳網址
    S3ImgUrl = upload_file_to_s3(file, os.getenv("S3_BUCKET"))

    # 將圖片網址跟文字訊息傳到db
    try:
        if mydb.is_connected():
            mycursor.execute(f'''INSERT INTO message SET
                                message_text = "{text}",
                                message_img_url = "{S3ImgUrl}"'''
                            )
            mydb.commit()
            
    finally:
        closePool(mydb, mycursor)

    return S3ImgUrl

@messageAPI.route('/api/message', methods=["GET"])
def GETmessage():
    mydb = conncetPool.get_connection()
    mycursor = mydb.cursor(dictionary=True) 
    try:
        if mydb.is_connected():
            mycursor.execute(f'SELECT * FROM message ORDER BY message_id desc')
            result = mycursor.fetchall()
    finally:
        closePool(mydb, mycursor)
   
    return jsonify({
        'data':result
    })
  
def upload_file_to_s3(file, bucket_name, acl="public-read"):
    
    try:

        s3.upload_fileobj(
            file,
            bucket_name,
            file.filename,
            ExtraArgs={
                "ACL": acl,
                "ContentType": file.content_type,
            }
        )

    except Exception as e:
        # This is a catch all exception, edit this part to fit your needs.
        print("Something Happened: ", e)
        return jsonify({
            'ok':false,
            'message':e
        })
    
    return f'https://{os.getenv("S3_LOCATION")}.amazonaws.com/{file.filename}'
    
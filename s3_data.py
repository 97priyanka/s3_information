import boto3
import csv
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart

def lambda_handler(event, context):
    
    s3=boto3.client('s3')
    ses = boto3.client('ses',region_name='us-east-1')
    body=['Bucket Name','Objects','Size','Last Modified','Bucket Region','Bucket Creation Date']
    with open('/tmp/s3data.csv', 'w') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(body)
    buckets = s3.list_buckets() 
    for bucket in buckets['Buckets']:
        flag=0
        loc=s3.get_bucket_location(Bucket=bucket['Name'])
        if(str(loc['LocationConstraint'])=='None'):
            location='us-east-1'
        else:
            location=loc['LocationConstraint']
        objects = s3.list_objects(Bucket=bucket['Name'])
        data=str(objects)
        if(data.find('Contents')!=-1):
            for obj in objects['Contents']:
                if(flag==0):
                    body=[bucket['Name'],obj['Key'],str(obj['Size']),str(obj['LastModified']),str(location),str(bucket['CreationDate'])]
                    flag+=1
                else:
                    body=[' ',obj['Key'],str(obj['Size']),str(obj['LastModified']),' ',' ']
                with open('/tmp/s3data.csv', 'a') as csvFile:
                    writer = csv.writer(csvFile)
                    writer.writerow(body)
        else:
            body=[bucket['Name'],' - ',' - ',' - ',str(location),str(bucket['CreationDate'])]
            with open('/tmp/s3data.csv', 'a') as csvFile:
                writer = csv.writer(csvFile)
                writer.writerow(body)
        body=[' ',' ',' ',' ',' ',' ']
        with open('/tmp/s3data.csv', 'a') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(body)
            
    msg=MIMEMultipart()
    recipients = ['xyz@example.com','abcd@example.com']  
    msg['Subject']='S3 Bucket Information'
    msg['From']='mnop@example.com'
    msg['To'] = ', '.join(recipients)
    part = MIMEText('This is the data of S3 buckets.')
    msg.attach(part)
    part = MIMEApplication(open('/tmp/s3data.csv','rb').read())
    part.add_header('Content-Disposition', 'attachment', filename='s3data.csv')
    msg.attach(part)
    ses.send_raw_email(RawMessage={'Data':msg.as_string()},Source=msg['From'],Destinations=recipients)

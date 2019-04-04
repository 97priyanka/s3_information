# s3_information

This is a script for s3 which retrieve all the information of buckets from the aws account in which it is running. The script is to be executed in the lambda function.
It only require ses mail id's to be configured which are used to send as well as receive mails. This is done using AWS Simple Email service.
This script create a csv file from the data retrieved from s3 which is then mailed to the respective mail id's.

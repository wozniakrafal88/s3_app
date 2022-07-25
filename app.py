import logging
import boto3
from botocore.exceptions import ClientError
from flask import Flask, render_template, request, url_for, redirect
import requests    # To install: pip install requests

app = Flask(__name__)

def create_presigned_post(bucket_name, object_name,
                          fields=None, conditions=None, expiration=3600):
    """Generate a presigned URL S3 POST request to upload a file

    :param bucket_name: string
    :param object_name: string
    :param fields: Dictionary of prefilled form fields
    :param conditions: List of conditions to include in the policy
    :param expiration: Time in seconds for the presigned URL to remain valid
    :return: Dictionary with the following keys:
        url: URL to post to
        fields: Dictionary of form fields and values to submit with the POST
    :return: None if error.
    """

    # Generate a presigned S3 POST URL
    s3_client = boto3.client('s3')
    try:
        response = s3_client.generate_presigned_post(bucket_name,
                                                     object_name,
                                                     Fields=fields,
                                                     Conditions=conditions,
                                                     ExpiresIn=expiration)
    except ClientError as e:
        logging.error(e)
        return None

    # The response contains the presigned URL and required fields
    return response

def create_presigned_url(bucket_name, object_name, expiration=3600):
    """Generate a presigned URL to share an S3 object

    :param bucket_name: string
    :param object_name: string
    :param expiration: Time in seconds for the presigned URL to remain valid
    :return: Presigned URL as string. If error, returns None.
    """

    # Generate a presigned URL for the S3 object
    s3_client = boto3.client('s3')
    try:
        response = s3_client.generate_presigned_url('get_object',
                                                    Params={'Bucket': bucket_name,
                                                            'Key': object_name},
                                                    ExpiresIn=expiration)
    except ClientError as e:
        logging.error(e)
        return None

    # The response contains the presigned URL
    return response


def list(bucket):
    s3 = boto3.client('s3')
    objects = s3.list_objects(Bucket=bucket)
    return objects

def list_with_url(objects):

    lists = []
    for item in objects['Contents']:
        url = create_presigned_url("rwozniak-s3",item['Key'])
        file_name = item['Key']
        new_item = {'Key':file_name,'url':url}
        lists.append(new_item)

    return lists



@app.route('/s3')
def index():
    objects = list("rwozniak-s3")
    lists = list_with_url(objects)
    return render_template('index_s3.html',lists=lists)

@app.route('/s3/presigned_form', methods=['GET'])
def presigned_form_s3():

        response = create_presigned_post('rwozniak-s3', '${filename}')
        if response is None:
            exit(1)
        return render_template('s3_form.html',presigned_s3_data=response)
import logging
import boto3
from botocore.exceptions import ClientError
from flask import Flask, render_template, request, url_for, redirect
import requests    # To install: pip install requests

app = Flask(__name__)

def create_presigned_post(bucket_name, object_name,
                          fields=None, conditions=None, expiration=3600):
    """Generate a presigned URL S3 POST request to upload a file

    :param bucket_name: string
    :param object_name: string
    :param fields: Dictionary of prefilled form fields
    :param conditions: List of conditions to include in the policy
    :param expiration: Time in seconds for the presigned URL to remain valid
    :return: Dictionary with the following keys:
        url: URL to post to
        fields: Dictionary of form fields and values to submit with the POST
    :return: None if error.
    """

    # Generate a presigned S3 POST URL
    s3_client = boto3.client('s3')
    try:
        response = s3_client.generate_presigned_post(bucket_name,
                                                     object_name,
                                                     Fields=fields,
                                                     Conditions=conditions,
                                                     ExpiresIn=expiration)
    except ClientError as e:
        logging.error(e)
        return None

    # The response contains the presigned URL and required fields
    return response

def create_presigned_url(bucket_name, object_name, expiration=3600):
    """Generate a presigned URL to share an S3 object

    :param bucket_name: string
    :param object_name: string
    :param expiration: Time in seconds for the presigned URL to remain valid
    :return: Presigned URL as string. If error, returns None.
    """

    # Generate a presigned URL for the S3 object
    s3_client = boto3.client('s3')
    try:
        response = s3_client.generate_presigned_url('get_object',
                                                    Params={'Bucket': bucket_name,
                                                            'Key': object_name},
                                                    ExpiresIn=expiration)
    except ClientError as e:
        logging.error(e)
        return None

    # The response contains the presigned URL
    return response


def list(bucket):
    s3 = boto3.client('s3')
    objects = s3.list_objects(Bucket=bucket)
    return objects

def list_with_url(objects):

    lists = []
    for item in objects['Contents']:
        url = create_presigned_url("rwozniak-s3",item['Key'])
        file_name = item['Key']
        new_item = {'Key':file_name,'url':url}
        lists.append(new_item)

    return lists



@app.route('/s3')
def index():
    objects = list("rwozniak-s3")
    lists = list_with_url(objects)
    return render_template('index_s3.html',lists=lists)

@app.route('/s3/presigned_form', methods=['GET'])
def presigned_form_s3():

        response = create_presigned_post('rwozniak-s3', '${filename}')
        if response is None:
            exit(1)
        return render_template('s3_form.html',presigned_s3_data=response)

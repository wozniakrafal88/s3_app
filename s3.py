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

@app.route('/s3')
def index():

    return render_template('index_s3.html')

@app.route('/s3/presigned_form', methods=['GET'])
def presigned_form_s3():

        response = create_presigned_post('rwozniak-s3', '${filename}')
        if response is None:
            exit(1)
        return render_template('s3_form.html',presigned_s3_data=response)

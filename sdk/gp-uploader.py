"""This Python3 script is used to upload a new .aab bundle to the play store. The execution of this Python script
    occurs through an AWS Lambda which is invoked when a new file is uploaded to the relevant S3 buckets"""

import json

import os
from urllib import request, parse
from google.oauth2 import service_account
import googleapiclient.discovery

#   Defining the scope of the authorization request
SCOPES = ['https://www.googleapis.com/auth/androidpublisher']
PACKAGE=home = os.environ['PACKAGE_NAME']
print(PACKAGE)
#   Package name for app
package_name = PACKAGE

#   This is the main handler function
def uploader():
    #   Create a new client S3 client and download the correct file from the bucket
    # s3 = boto3.client('s3')
    # s3.download_file('service-account-bucket-key', 'service-account-bucket-key.json', '/tmp/service-account-key.json')
    SERVICE_ACCOUNT_FILE = '/tmp/service-account-key.json'
    APP_BUNDLE = '/tmp/app-release.aab'

    
    #   Create a credentials object and create a service object using the credentials object
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES
    )
    service = googleapiclient.discovery.build('androidpublisher', 'v3', credentials=credentials, cache_discovery=False)
    
    #   Create an edit request using the service object and get the editId
    edit_request = service.edits().insert(body={}, packageName=package_name)
    result = edit_request.execute()
    edit_id = result['id']

    #   Create a request to upload the app bundle
    try:
        bundle_response = service.edits().bundles().upload(
            editId=edit_id,
            packageName=package_name,
            media_body=APP_BUNDLE,
            media_mime_type="application/octet-stream"
        ).execute()
    except Exception as err:
        message = f"There was an error while uploading a new version of {package_name}"
        # send_slack_message(message)
        raise err

    print(f"Version code {bundle_response['versionCode']} has been uploaded")

    #   Create a track request to upload the bundle to the beta track
    track_response = service.edits().tracks().update(
        editId=edit_id,
        track='internal',
        packageName=package_name,
        body={u'releases': [{
            u'versionCodes': [str(bundle_response['versionCode'])],
            u'status': u'draft',
        }]}
    ).execute()

    print("The bundle has been committed to the beta track")

    #   Create a commit request to commit the edit to BETA track
    commit_request = service.edits().commit(
        editId=edit_id,
        packageName=package_name
    ).execute()

    print(f"Edit {commit_request['id']} has been committed")

    message = f"Version code {bundle_response['versionCode']} has been uploaded from the bucket .\nEdit {commit_request['id']} has been committed"
    
   
    
    return {
        'statusCode': 200,
        'body': json.dumps('Successfully executed the app bundle release to beta')
    }

uploader()
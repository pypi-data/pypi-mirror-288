import boto3
from sawsi.aws import shared


class CloudSearchAPI:

    def __init__(self, credentials=None, region=shared.DEFAULT_REGION):
        self.boto3_session = shared.get_boto_session(credentials)
        self.client = self.boto3_session.client('cloudsearch', region_name=region)

from aws.boto3 import Boto3

class Cognito:
    def __init__(self, region=None, profile_name=None):
        self.boto3 = Boto3()
        session = self.boto3.get_app_session(profile_name=profile_name, region=region)
        self.client = session.client('cognito-idp')
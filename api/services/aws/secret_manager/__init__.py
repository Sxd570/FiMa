from aws.boto3 import Boto3

class SecretManager:
    def __init__(self, region=None, profile_name=None):
        self.boto3 = Boto3()
        session = self.boto3.get_app_session(profile_name=profile_name, region=region)
        self.client = session.client('secretsmanager')


    def get_secret(self, secret_name):
        try:
            response = self.client.get_secret_value(SecretId=secret_name)
            return response['SecretString']
        except Exception as e:
            print(f"Error retrieving secret {secret_name}: {e}")
            raise e

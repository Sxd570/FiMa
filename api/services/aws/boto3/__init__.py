import boto3

class Boto3:
    def __init__(self):
        self._session_params = {}
        self._app_session = None

    
    def get_app_session(self, profile_name=None, region=None):
        if profile_name:
            self._session_params['profile_name'] = profile_name
        if region:
            self._session_params['region_name'] = region

        self._app_session = boto3.Session(**self._session_params)

        return self._app_session
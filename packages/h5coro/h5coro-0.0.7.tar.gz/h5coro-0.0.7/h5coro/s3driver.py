import logging

import boto3
from botocore.handlers import disable_signing

###############################################################################
# Globals
###############################################################################

logger = logging.getLogger(__name__)

###############################################################################
# Exceptions
###############################################################################


class FatalError(RuntimeError):
    pass


###############################################################################
# S3Driver Class
###############################################################################


class S3Driver:
    #######################
    # Constructor
    #######################
    def __init__(self, resource, credentials):
        # construct path to resource
        self.resourcePath = list(filter(("").__ne__, resource.split("/")))

        if "annon" in credentials and credentials["annon"]:
            self.session = boto3.Session()
            # Register the event handler to disable signing
            self.session.events.register("choose-signer.s3.*", disable_signing)
        else:
            # apply credentials if supplied
            if "profile" in credentials:
                self.session = boto3.Session(profile_name=credentials["profile"])
            elif (
                "aws_access_key_id" in credentials
                and "aws_secret_access_key" in credentials
                and "aws_session_token" in credentials
            ):
                self.session = boto3.Session(
                    aws_access_key_id=credentials["aws_access_key_id"],
                    aws_secret_access_key=credentials["aws_secret_access_key"],
                    aws_session_token=credentials["aws_session_token"],
                )
            elif (
                "accessKeyId" in credentials
                and "secretAccessKey" in credentials
                and "sessionToken" in credentials
            ):
                self.session = boto3.Session(
                    aws_access_key_id=credentials["accessKeyId"],
                    aws_secret_access_key=credentials["secretAccessKey"],
                    aws_session_token=credentials["sessionToken"],
                )
            elif len(credentials) == 0:
                self.session = boto3.Session()
            else:
                raise FatalError(
                    "invalid credential keys provided, looking for: aws_access_key_id, aws_secret_access_key, and aws_session_token"
                )

        # open resource
        self.obj = self.session.resource("s3").Object(
            self.resourcePath[0], "/".join(self.resourcePath[1:])
        )

    #######################
    # read
    #######################
    def read(self, pos, size):
        stream = self.obj.get(Range=f"bytes={pos}-{pos+size-1}")["Body"]
        return stream.read()

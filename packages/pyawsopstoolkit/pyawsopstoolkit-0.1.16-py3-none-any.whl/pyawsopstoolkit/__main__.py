import os
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Union

from pyawsopstoolkit.__interfaces__ import ICredentials, IAccount, ISession
from pyawsopstoolkit.__validations__ import Validation
from pyawsopstoolkit.exceptions import AssumeRoleError
from pyawsopstoolkit.validators import ArnValidator, PolicyValidator, TagValidator, AccountValidator, Validator


@dataclass
class Credentials(ICredentials):
    """
    Represents a set of credentials including an access key, secret access key, token, and optional expiry datetime.
    """
    access_key: str
    secret_access_key: str
    token: Optional[str] = None
    expiry: Optional[datetime] = None

    def __post_init__(self):
        for field_name, field_value in self.__dataclass_fields__.items():
            self.__validate__(field_name)

    def __validate__(self, field_name):
        field_value = getattr(self, field_name)
        if field_name in ['access_key', 'secret_access_key']:
            Validation.validate_type(field_value, str, f'{field_name} should be a string.')
        elif field_name in ['token']:
            Validation.validate_type(field_value, Union[str, None], f'{field_name} should be a string.')
        elif field_name in ['expiry']:
            Validation.validate_type(field_value, Union[datetime, None], f'{field_name} should be a datetime.')

    def __setattr__(self, key, value):
        super().__setattr__(key, value)
        if key in self.__dataclass_fields__:
            self.__validate__(key)

    def to_dict(self) -> dict:
        """
        Convert Credentials object to dictionary.
        :return: Dictionary representation of Credentials object.
        :rtype: dict
        """
        return {
            "access_key": self.access_key,
            "secret_access_key": self.secret_access_key,
            "token": self.token if self.token is not None else None,
            "expiry": self.expiry.isoformat() if self.expiry is not None else None
        }


@dataclass
class Account(IAccount):
    """
    Represents an AWS account with various attributes. This class implements the IAccount interface, providing basic
    functionality for managing an AWS account.
    """
    number: str

    def __post_init__(self):
        for field_name, field_value in self.__dataclass_fields__.items():
            self.__validate__(field_name)

    def __validate__(self, field_name):
        field_value = getattr(self, field_name)
        if field_name in ['number']:
            AccountValidator.number(field_value, True)

    def __setattr__(self, key, value):
        super().__setattr__(key, value)
        if key in self.__dataclass_fields__:
            self.__validate__(key)

    def to_dict(self) -> dict:
        """
        Return a dictionary representation of the Account object.
        :return: Dictionary representation of the Account object.
        :rtype: dict
        """
        return {
            "number": self.number
        }


@dataclass
class Session(ISession):
    """
    This class represents a boto3 Session with various attributes. It implements the ISession interface, offering
    functionality to manage sessions. Additionally, it provides the option to assume a session.
    """
    profile_name: Optional[str] = None
    credentials: Optional[ICredentials] = None
    region_code: Optional[str] = 'eu-west-1'
    cert_path: Optional[str] = None

    def __post_init__(self):
        if (self.profile_name is not None) == (self.credentials is not None):
            raise ValueError('Either profile_name or credentials should be provided, but not both.')
        elif (self.profile_name is None) == (self.credentials is None):
            raise ValueError('At least profile_name or credentials is required.')

        for field_name, field_value in self.__dataclass_fields__.items():
            self.__validate__(field_name)

        if self.cert_path is not None:
            os.environ['AWS_CA_BUNDLE'] = self.cert_path

    def __validate__(self, field_name):
        field_value = getattr(self, field_name)
        if field_name in ['profile_name', 'cert_path']:
            Validation.validate_type(field_value, Union[str, None], f'{field_name} should be a string.')
        elif field_name in ['region_code']:
            Validator.region(field_value, True)
        elif field_name in ['credentials']:
            Validation.validate_type(
                field_value, Union[ICredentials, None], f'{field_name} should be of ICredentials type.'
            )

    def __setattr__(self, key, value):
        super().__setattr__(key, value)
        if key in self.__dataclass_fields__:
            self.__validate__(key)

    def get_session(self):
        """
        Returns the boto3.Session object based on the specified parameters within the class object.
        Priority is given to profile_name, followed by credentials.
        This method performs a quick S3 list buckets action to verify if the session is valid.
        :return: The boto3 Session object based on the specified parameters within the class object.
        :rtype: boto3.Session
        """
        import boto3

        from botocore.exceptions import ClientError, ProfileNotFound

        session = None
        try:
            if self.profile_name:
                session = boto3.Session(profile_name=self.profile_name)
            elif self.credentials:
                session = boto3.Session(
                    aws_access_key_id=self.credentials.access_key,
                    aws_secret_access_key=self.credentials.secret_access_key,
                    aws_session_token=self.credentials.token
                )
            else:
                raise ValueError('At least profile_name or credentials is required.')

            session.client('s3').list_buckets()
        except ProfileNotFound:
            raise ValueError(f'Profile "{self.profile_name}" not found.')
        except ClientError as e:
            if e.response['Error']['Code'] != 'AccessDenied':
                raise ValueError(f'Failed to create session: {e}.')

        return session

    def get_config(self):
        """
        Returns the botocore.config.Config based on the specified region code within the class object.
        :return: The botocore Config object based on the specified region code within the class object.
        :rtype: botocore.config.Config
        """
        from botocore.config import Config

        return Config(region_name=self.region_code)

    def get_account(self) -> IAccount:
        """
        Returns the AWS account number based on the get_session with specified parameters within the class object.
        :return: The AWS account number.
        :rtype: Account
        """
        from botocore.exceptions import ClientError

        session = self.get_session()
        try:
            account_id = session.client('sts').get_caller_identity().get('Account', '')
            if account_id:
                return Account(account_id)
        except ClientError as e:
            raise ValueError(f'Failed to retrieve AWS account number: {e}.')

    def get_credentials_for_profile(self) -> ICredentials:
        """
        Returns the AWS credentials, i.e., access key, secret access key, and token based on the get_session with
        specified parameters within the class object.
        :return: The AWS credentials.
        :rtype: Credentials
        """
        from botocore.exceptions import ClientError, ProfileNotFound

        if self.profile_name is None:
            raise ValueError('profile_name is not set.')

        session = self.get_session()
        try:
            creds = session.get_credentials()
            return Credentials(
                access_key=creds.access_key,
                secret_access_key=creds.secret_key,
                token=creds.token
            )
        except ProfileNotFound:
            raise ValueError(f'Profile "{self.profile_name}" not found.')
        except ClientError as e:
            raise ValueError(f'Failed to retrieve AWS credentials: {e}.')

    def assume_role(
            self,
            role_arn: str,
            role_session_name: Optional[str] = 'AssumeSession',
            policy_arns: Optional[list] = None,
            policy: Optional[Union[str, dict]] = None,
            duration_seconds: Optional[int] = 3600,
            tags: Optional[list] = None
    ):
        """
        Returns the boto3.Session object for the assumed role based on the specified parameters.
        :param role_arn: The AWS ARN of the role to be assumed.
        :type role_arn: str
        :param role_session_name: Optional, The name for the AWS assumed session. Default is considered
        as 'AssumeSession'.
        :type role_session_name: str
        :param policy_arns: Optional, The list of IAM policy ARNs to attach to the assumed role session.
        :type policy_arns: list
        :param policy: Optional, The policy to be attached to the assumed role session.
        :type policy: str or dict
        :param duration_seconds: Optional, The duration (in seconds) to be set to the assumed role session.
        Default is considered as 3600 seconds.
        :type duration_seconds: int
        :param tags: Optional, The tags to be applied to the assumed role session.
        :type tags: dict
        :return: The Session object of the assumed role session.
        :rtype: ISession
        """
        from botocore.exceptions import ClientError

        ArnValidator.arn(role_arn)
        Validation.validate_type(role_session_name, Union[str, None], 'role_session_name should be a string.')
        Validation.validate_type(policy_arns, Union[list, None], 'policy_arns should be list of strings.')
        if policy_arns:
            ArnValidator.arn(policy_arns)
        if policy:
            PolicyValidator.policy(policy)
        Validation.validate_type(duration_seconds, Union[int, None], 'duration_seconds should be an integer.')
        if tags:
            TagValidator.tag(tags)

        session = self.get_session()
        try:
            sts_client = session.client('sts')
            params = {
                "RoleArn": role_arn,
                "RoleSessionName": role_session_name,
                "DurationSeconds": duration_seconds
            }
            if policy_arns:
                params.update({"PolicyArns": policy_arns})
            if policy:
                params.update({"Policy": policy})
            if tags:
                params.update({"Tags": tags})
            response = sts_client.assume_role(**params)
            if response:
                creds = response.get('Credentials', {})
                if creds:
                    return Session(credentials=Credentials(
                        access_key=creds.get('AccessKeyId', ''),
                        secret_access_key=creds.get('SecretAccessKey', ''),
                        token=creds.get('SessionToken', ''),
                        expiry=creds.get('Expiration', datetime.utcnow())
                    ), cert_path=self.cert_path)
        except ClientError as e:
            raise AssumeRoleError(role_arn=role_arn, exception=e)

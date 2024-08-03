from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Union

from pyawsopstoolkit.__interfaces__ import IAccount
from pyawsopstoolkit.__validations__ import Validation
from pyawsopstoolkit.models.iam.__main__ import PermissionsBoundary
from pyawsopstoolkit.validators import Validator, ArnValidator


@dataclass
class LastUsed:
    """
    A class representing the last used information of an IAM role.
    """
    used_date: Optional[datetime] = None
    region: Optional[str] = None

    def __post_init__(self):
        for field_name, field_value in self.__dataclass_fields__.items():
            self.__validate__(field_name)

    def __validate__(self, field_name):
        field_value = getattr(self, field_name)
        if field_name in ['used_date']:
            Validation.validate_type(field_value, Union[datetime, None], f'{field_name} should be a datetime.')
        elif field_name in ['region']:
            if field_value is not None:
                Validator.region(field_value, True)

    def __setattr__(self, key, value):
        super().__setattr__(key, value)
        if key in self.__dataclass_fields__:
            self.__validate__(key)

    def to_dict(self) -> dict:
        """
        Returns a dictionary representation of the LastUsed instance.
        :return: Dictionary representation of the LastUsed instance.
        :rtype: dict
        """
        return {
            "used_date": self.used_date.isoformat() if self.used_date is not None else None,
            "region": self.region
        }


@dataclass
class Role:
    """
    A class representing an IAM role.
    """
    account: IAccount
    name: str
    id: str
    arn: str
    max_session_duration: int
    path: str = '/'
    created_date: Optional[datetime] = None
    assume_role_policy_document: Optional[dict] = None
    description: Optional[str] = None
    permissions_boundary: Optional[PermissionsBoundary] = None
    last_used: Optional[LastUsed] = None
    tags: Optional[list] = None

    def __post_init__(self):
        for field_name, field_value in self.__dataclass_fields__.items():
            self.__validate__(field_name)

    def __validate__(self, field_name):
        mappings = {
            'account': IAccount,
            'created_date': datetime,
            'assume_role_policy_document': dict,
            'permissions_boundary': PermissionsBoundary,
            'last_used': LastUsed,
            'tags': list
        }
        field_value = getattr(self, field_name)
        field_type = mappings.get(field_name)
        if field_name in ['account']:
            Validation.validate_type(field_value, field_type, f'{field_name} should be of {field_type.__name__} type.')
        elif field_name in ['name', 'id', 'path']:
            Validation.validate_type(field_value, str, f'{field_name} should be a string.')
        elif field_name in ['arn']:
            ArnValidator.arn(field_value, True)
        elif field_name in ['max_session_duration']:
            Validation.validate_type(field_value, int, f'{field_name} should be an integer.')
        elif field_name in ['created_date', 'assume_role_policy_document', 'permissions_boundary', 'last_used', 'tags']:
            Validation.validate_type(
                field_value, Union[field_type, None], f'{field_name} should be of {field_type.__name__} type.'
            )
        elif field_name in ['description']:
            Validation.validate_type(field_value, Union[str, None], f'{field_name} should be a string.')

    def __setattr__(self, key, value):
        super().__setattr__(key, value)
        if key in self.__dataclass_fields__:
            self.__validate__(key)

    def to_dict(self) -> dict:
        """
        Return a dictionary representation of the Role object.
        :return: Dictionary representation of the Role object.
        :rtype: dict
        """
        return {
            "account": self.account.to_dict(),
            "path": self.path,
            "name": self.name,
            "id": self.id,
            "arn": self.arn,
            "created_date": self.created_date.isoformat() if self.created_date is not None else None,
            "assume_role_policy_document": self.assume_role_policy_document,
            "description": self.description,
            "max_session_duration": self.max_session_duration,
            "permissions_boundary": (
                self.permissions_boundary.to_dict() if self.permissions_boundary is not None else None
            ),
            "last_used": self.last_used.to_dict() if self.last_used is not None else None,
            "tags": self.tags
        }

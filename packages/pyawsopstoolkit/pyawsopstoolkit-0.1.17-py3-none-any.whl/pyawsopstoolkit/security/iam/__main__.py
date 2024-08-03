import re
from dataclasses import dataclass

from pyawsopstoolkit.__interfaces__ import ISession
from pyawsopstoolkit.__validations__ import Validation


@dataclass
class Role:
    """
    A class representing security risks and vulnerabilities related with IAM roles.
    """
    session: ISession

    def __post_init__(self):
        for field_name, field_value in self.__dataclass_fields__.items():
            self.__validate__(field_name)

    def __validate__(self, field_name):
        field_value = getattr(self, field_name)
        if field_name in ['session']:
            Validation.validate_type(field_value, ISession, f'{field_name} should be of ISession type.')

    def __setattr__(self, key, value):
        super().__setattr__(key, value)
        if key in self.__dataclass_fields__:
            self.__validate__(key)

    def roles_without_permissions_boundary(self) -> list:
        """
        Returns a list of IAM roles that do not have an associated permissions boundary.
        :return: A list of IAM roles without an associated permissions boundary.
        :rtype: list
        """
        from pyawsopstoolkit.advsearch.iam import Role

        role_object = Role(self.session)
        iam_roles = role_object.search_roles(include_details=True)

        if iam_roles is None:
            return []

        roles_without_permissions_boundary = []

        for role in iam_roles:
            if not re.search(r'/aws-service-role/', role.path, re.IGNORECASE):
                if role.permissions_boundary is None:
                    roles_without_permissions_boundary.append(role)

        return roles_without_permissions_boundary


@dataclass
class User:
    """
    A class representing security risks and vulnerabilities related with IAM users.
    """
    session: ISession

    def __post_init__(self):
        for field_name, field_value in self.__dataclass_fields__.items():
            self.__validate__(field_name)

    def __validate__(self, field_name):
        field_value = getattr(self, field_name)
        if field_name in ['session']:
            Validation.validate_type(field_value, ISession, f'{field_name} should be of ISession type.')

    def __setattr__(self, key, value):
        super().__setattr__(key, value)
        if key in self.__dataclass_fields__:
            self.__validate__(key)

    def users_without_permissions_boundary(self) -> list:
        """
        Returns a list of IAM users that do not have an associated permissions boundary.
        :return: A list of IAM users without an associated permissions boundary.
        :rtype: list
        """
        from pyawsopstoolkit.advsearch.iam import User

        user_object = User(self.session)
        iam_users = user_object.search_users(include_details=True)

        if iam_users is None:
            return []

        return [
            user for user in iam_users
            if user.permissions_boundary is None
        ]

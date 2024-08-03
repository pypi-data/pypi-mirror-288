import re
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from pyawsopstoolkit.__interfaces__ import ISession
from pyawsopstoolkit.__validations__ import Validation


@dataclass
class Role:
    """
    A class representing insights related with IAM roles.
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

    def unused_roles(
            self,
            no_of_days: Optional[int] = 90,
            include_newly_created: Optional[bool] = False
    ) -> list:
        """
        Returns a list of unused IAM roles based on the specified parameters.
        :param no_of_days: The number of days (integer) to check if the IAM role has been used within the
        specified period. Defaults to 90 days.
        :type no_of_days: int
        :param include_newly_created: A flag indicating whether to include newly created IAM roles within the
        specified number of days. Defaults to False.
        :type include_newly_created: bool
        :return: A list of unused IAM roles.
        :rtype: list
        """
        from pyawsopstoolkit.advsearch.iam import Role

        Validation.validate_type(no_of_days, int, 'no_of_days should be an integer.')
        Validation.validate_type(include_newly_created, bool, 'include_newly_created should be a boolean.')

        current_date = datetime.today().replace(tzinfo=None)
        role_object = Role(self.session)
        iam_roles = role_object.search_roles(include_details=True)

        if iam_roles is None:
            return []

        def role_is_unused(_role):
            if _role.last_used is None:
                return True

            if (current_date - _role.last_used.used_date.replace(tzinfo=None)).days <= no_of_days:
                return False

            return True

        unused_roles_list = []

        for role in iam_roles:
            if not re.search(r'/aws-service-role/', role.path, re.IGNORECASE):
                if include_newly_created:
                    if role_is_unused(role):
                        unused_roles_list.append(role)
                else:
                    if (
                            (current_date - role.created_date.replace(tzinfo=None)).days > no_of_days
                            and role_is_unused(role)
                    ):
                        unused_roles_list.append(role)

        return unused_roles_list


@dataclass
class User:
    """
    A class representing insights related with IAM users.
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

    def unused_users(
            self,
            no_of_days: Optional[int] = 90,
            include_newly_created: Optional[bool] = False
    ) -> list:
        """
        Returns a list of unused IAM users based on the specified parameters.
        :param no_of_days: The number of days (integer) to check if the IAM user has been used within the
        specified period. Defaults to 90 days.
        :type no_of_days: int
        :param include_newly_created: A flag indicating whether to include newly created IAM users within the
        specified number of days. Defaults to False.
        :type include_newly_created: bool
        :return: A list of unused IAM users.
        :rtype: list
        """
        from pyawsopstoolkit.advsearch.iam import User

        Validation.validate_type(no_of_days, int, 'no_of_days should be an integer.')
        Validation.validate_type(include_newly_created, bool, 'include_newly_created should be a boolean.')

        current_date = datetime.today().replace(tzinfo=None)
        user_object = User(self.session)
        iam_users = user_object.search_users(include_details=True)

        if iam_users is None:
            return []

        def user_is_unused(_user):
            _last_login = None
            _access_key_last_used = None

            if _user.login_profile is not None:
                _last_login = _user.login_profile.created_date

            if _user.access_keys is not None:
                for _key in _user.access_keys:
                    _last_used_date = _key.last_used_date
                    if not _access_key_last_used or _last_used_date > _access_key_last_used:
                        _access_key_last_used = _last_used_date

            _password_last_used = _user.password_last_used_date

            _recent_activity_date: datetime = max(
                filter(None, [_last_login, _access_key_last_used, _password_last_used]), default=None
            )

            if _recent_activity_date is None:
                return True

            if (current_date - _recent_activity_date.replace(tzinfo=None)).days <= no_of_days:
                return False

            return True

        unused_users_list = []

        for user in iam_users:
            if include_newly_created:
                if user_is_unused(user):
                    unused_users_list.append(user)
            else:
                if (
                        (current_date - user.created_date.replace(tzinfo=None)).days > no_of_days
                        and user_is_unused(user)
                ):
                    unused_users_list.append(user)

        return unused_users_list

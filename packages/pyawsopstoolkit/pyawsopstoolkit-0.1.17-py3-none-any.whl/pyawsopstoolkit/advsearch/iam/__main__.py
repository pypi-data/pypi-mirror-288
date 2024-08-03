from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from pyawsopstoolkit.__globals__ import MAX_WORKERS
from pyawsopstoolkit.__interfaces__ import ISession, IAccount
from pyawsopstoolkit.__validations__ import Validation
from pyawsopstoolkit.advsearch import OR, AND
from pyawsopstoolkit.advsearch.__main__ import _match_compare_condition, _match_tag_condition, _match_condition
from pyawsopstoolkit.advsearch.iam.__handlers__ import _get_role, _list_roles, _get_user, _get_login_profile, \
    _list_access_keys, _get_access_key_last_used, _list_users
from pyawsopstoolkit.exceptions import SearchAttributeError, AdvanceSearchError


@dataclass
class Role:
    """
    A class representing advance search features related with IAM roles.
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

    @staticmethod
    def _convert_to_iam_role(account: IAccount, role: dict):
        """
        This function transforms the dictionary response from boto3 IAM into a format compatible with the
        AWS Ops Toolkit, adhering to the pyawsopstoolkit.models structure. Additionally, it incorporates
        account-related summary information into the IAM role details.
        :param account: An IAccount object containing AWS account information.
        :type account: IAccount
        :param role: The boto3 IAM service response for an IAM role.
        :type role: dict
        :return: An AWS Ops Toolkit compatible object containing all IAM role details.
        :rtype: pyawsopstoolkit.models.iam.role.Role
        """
        from pyawsopstoolkit.models.iam.role import Role, LastUsed
        from pyawsopstoolkit.models.iam import PermissionsBoundary

        iam_role = Role(
            account=account,
            name=role.get('RoleName', ''),
            id=role.get('RoleId', ''),
            arn=role.get('Arn', ''),
            max_session_duration=role.get('MaxSessionDuration', 0),
            path=role.get('Path', ''),
            created_date=role.get('CreateDate', None),
            assume_role_policy_document=role.get('AssumeRolePolicyDocument', None),
            description=role.get('Description', None)
        )

        boundary = role.get('PermissionsBoundary', {})
        if boundary:
            iam_role.permissions_boundary = PermissionsBoundary(
                type=boundary.get('PermissionsBoundaryType', ''),
                arn=boundary.get('PermissionsBoundaryArn', '')
            )

        last_used = role.get('RoleLastUsed')
        if last_used:
            iam_role.last_used = LastUsed(
                used_date=last_used.get('LastUsedDate', None),
                region=last_used.get('Region', None)
            )

        iam_role.tags = role.get('Tags', [])

        return iam_role

    def search_roles(
            self,
            condition: str = OR,
            include_details: bool = False,
            **kwargs
    ) -> list:
        """
        Returns a list of IAM roles using advanced search features supported by the specified arguments.
        For details on supported kwargs, please refer to the readme document.
        :param condition: The condition to be applied: 'OR' or 'AND'.
        :type condition: str
        :param include_details: Flag to indicate to include additional details of the IAM role.
        This includes information about permissions boundary, last used, and tags. Default is False.
        :type include_details: bool
        :param kwargs: Key-based arguments defining search criteria.
        :return: A list of IAM roles.
        :rtype: list
        """
        Validation.validate_type(condition, str, 'condition should be a string and should be either "OR" or "AND".')
        Validation.validate_type(include_details, bool, 'include_details should be a boolean.')

        def _process_role(role_detail):
            if include_details:
                role_detail = _get_role(self.session, role_detail.get('RoleName', '')).get('Role', {})

            return self._convert_to_iam_role(self.session.get_account(), role_detail)

        def _match_role(role_detail):
            if role_detail:
                matched = False if condition == OR else True
                for key, value in kwargs.items():
                    if value is not None:
                        role_field = ''
                        if key.lower() == 'path':
                            role_field = role_detail.get('Path', '')
                        elif key.lower() == 'name':
                            role_field = role_detail.get('RoleName', '')
                        elif key.lower() == 'id':
                            role_field = role_detail.get('RoleId', '')
                        elif key.lower() == 'arn':
                            role_field = role_detail.get('Arn', '')
                        elif key.lower() == 'description':
                            role_field = role_detail.get('Description', '')
                        elif key.lower() == 'permissions_boundary_type':
                            if include_details:
                                role_detail = _get_role(self.session, role_detail.get('RoleName', '')).get('Role', {})
                                _permissions_boundary = role_detail.get('PermissionsBoundary', {})
                                role_field = _permissions_boundary.get('PermissionsBoundaryType', '')
                        elif key.lower() == 'permissions_boundary_arn':
                            if include_details:
                                role_detail = _get_role(self.session, role_detail.get('RoleName', '')).get('Role', {})
                                _permissions_boundary = role_detail.get('PermissionsBoundary', {})
                                role_field = _permissions_boundary.get('PermissionsBoundaryArn', '')
                        elif key.lower() == 'max_session_duration':
                            role_field = role_detail.get('MaxSessionDuration', 0)
                            matched = _match_compare_condition(value, role_field, condition, matched)
                        elif key.lower() == 'created_date':
                            role_field = role_detail.get('CreateDate', None)
                            if isinstance(role_field, datetime):
                                role_field = role_field.replace(tzinfo=None)
                                matched = _match_compare_condition(value, role_field, condition, matched)
                        elif key.lower() == 'last_used_date':
                            if include_details:
                                role_detail = _get_role(self.session, role_detail.get('RoleName', '')).get('Role', {})
                                _last_used = role_detail.get('RoleLastUsed', {})
                                role_field = _last_used.get('LastUsedDate', None)
                                if isinstance(role_field, datetime):
                                    role_field = role_field.replace(tzinfo=None)
                                    matched = _match_compare_condition(value, role_field, condition, matched)
                        elif key.lower() == 'last_used_region':
                            if include_details:
                                role_detail = _get_role(self.session, role_detail.get('RoleName', '')).get('Role', {})
                                _last_used = role_detail.get('RoleLastUsed', {})
                                role_field = _last_used.get('Region', '')
                        elif key.lower() == 'tag_key':
                            if include_details:
                                role_detail = _get_role(self.session, role_detail.get('RoleName', '')).get('Role', {})
                                tags = {tag['Key']: tag['Value'] for tag in role_detail.get('Tags', [])}
                                matched = _match_tag_condition(value, tags, condition, matched, key_only=True)
                        elif key.lower() == 'tag':
                            if include_details:
                                role_detail = _get_role(self.session, role_detail.get('RoleName', '')).get('Role', {})
                                tags = {tag['Key']: tag['Value'] for tag in role_detail.get('Tags', [])}
                                matched = _match_tag_condition(value, tags, condition, matched, key_only=False)

                        if key.lower() not in [
                            'max_session_duration', 'created_date', 'last_used_date', 'tag_key', 'tag'
                        ]:
                            matched = _match_condition(value, role_field, condition, matched)

                        if (condition == OR and matched) or (condition == AND and not matched):
                            break

                if matched:
                    return _process_role(role_detail)

        roles_to_return = []

        from botocore.exceptions import ClientError
        try:
            include_details_keys = {
                'permissions_boundary_type',
                'permissions_boundary_arn',
                'last_used_date',
                'last_used_region',
                'tag',
                'tag_key'
            }

            if not include_details and any(k in include_details_keys for k in kwargs):
                raise SearchAttributeError(
                    f'include_details is required for below keys: {", ".join(sorted(include_details_keys))}'
                )

            roles_to_process = _list_roles(self.session)

            if len(kwargs) == 0:
                with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
                    future_to_role = {executor.submit(_process_role, role): role for role in roles_to_process}
                    for future in as_completed(future_to_role):
                        role_result = future.result()
                        if role_result is not None:
                            roles_to_return.append(role_result)
            else:
                with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
                    future_to_role = {executor.submit(_match_role, role): role for role in roles_to_process}
                    for future in as_completed(future_to_role):
                        role_result = future.result()
                        if role_result is not None:
                            roles_to_return.append(role_result)
        except ClientError as e:
            raise AdvanceSearchError('search_roles', e)

        return roles_to_return


@dataclass
class User:
    """
    A class representing advance search features related with IAM users.
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

    @staticmethod
    def _convert_to_iam_user(
            account: IAccount,
            user: dict,
            login_profile: Optional[dict] = None,
            access_keys: Optional[list] = None
    ):
        """
        This function transforms the dictionary response from boto3 IAM into a format compatible with the
        AWS Ops Toolkit, adhering to the pyawsopstoolkit.models structure. Additionally, it incorporates
        account-related summary information into the IAM user details.
        :param account: An IAccount object containing AWS account information.
        :type account: IAccount
        :param user: The boto3 IAM service response for an IAM user.
        :type user: dict
        :param login_profile: The boto3 IAM login profile service response for an IAM user.
        :type login_profile: dict
        :param access_keys: The boto3 IAM access keys service response for an IAM user.
        :type access_keys: list
        :return: An AWS Ops Toolkit compatible object containing all IAM user details.
        :rtype: pyawsopstoolkit.models.iam.user.User
        """
        from pyawsopstoolkit.models.iam.user import User, AccessKey, LoginProfile
        from pyawsopstoolkit.models.iam import PermissionsBoundary

        iam_user = User(
            account=account,
            name=user.get('UserName', ''),
            id=user.get('UserId', ''),
            arn=user.get('Arn', ''),
            path=user.get('Path', ''),
            created_date=user.get('CreateDate', None),
            password_last_used_date=user.get('PasswordLastUsed', None)
        )

        boundary = user.get('PermissionsBoundary', {})
        if boundary:
            iam_user.permissions_boundary = PermissionsBoundary(
                type=boundary.get('PermissionsBoundaryType', ''),
                arn=boundary.get('PermissionsBoundaryArn', '')
            )

        if login_profile:
            iam_user.login_profile = LoginProfile(
                created_date=login_profile.get('CreateDate', None),
                password_reset_required=login_profile.get('PasswordResetRequired', False)
            )

        if access_keys:
            iam_user.access_keys = [
                AccessKey(
                    id=key.get('access_key', {}).get('AccessKeyId', ''),
                    status=key.get('access_key', {}).get('Status', ''),
                    created_date=key.get('access_key', {}).get('CreateDate', None),
                    last_used_date=key.get('last_used', {}).get('AccessKeyLastUsed', {}).get('LastUsedDate', None),
                    last_used_service=key.get('last_used', {}).get('AccessKeyLastUsed', {}).get('ServiceName', None),
                    last_used_region=key.get('last_used', {}).get('AccessKeyLastUsed', {}).get('Region', None)
                )
                for key in access_keys
            ]

        iam_user.tags = user.get('Tags', [])

        return iam_user

    def search_users(
            self,
            condition: str = OR,
            include_details: bool = False,
            **kwargs
    ) -> list:
        """
        Returns a list of IAM users using advanced search feature supported by the specified arguments.
        For details on supported kwargs, please refer to the readme document.
        :param condition: The condition to be applied: 'OR' or 'AND'.
        :type condition: str
        :param include_details: Flag to indicate to include additional details of the IAM user.
        This includes information about permissions boundary and tags. Default is False.
        :type include_details: bool
        :param kwargs: Key-based arguments defining search criteria.
        :return: A list of IAM users.
        :rtype: list
        """
        Validation.validate_type(condition, str, 'condition should be a string and should be either "OR" or "AND".')
        Validation.validate_type(include_details, bool, 'include_details should be a boolean.')

        def _process_user(user_detail):
            login_profile_detail = None
            access_keys_detail = []

            if include_details:
                user_detail = _get_user(self.session, user_detail.get('UserName', '')).get('User', {})
                login_profile_detail = _get_login_profile(self.session, user_detail.get('UserName', '')).get(
                    'LoginProfile', {})
                for a_key in _list_access_keys(self.session, user_detail.get('UserName', '')):
                    a_key_last_used = _get_access_key_last_used(self.session, a_key.get('AccessKeyId', ''))
                    access_keys_detail.append({
                        'access_key': a_key,
                        'last_used': a_key_last_used
                    })

            return self._convert_to_iam_user(
                self.session.get_account(), user_detail, login_profile_detail, access_keys_detail
            )

        def _match_user(user_detail):
            if user_detail:
                matched = False if condition == OR else True
                for key, value in kwargs.items():
                    if value is not None:
                        user_field = ''
                        if key.lower() == 'path':
                            user_field = user_detail.get('Path', '')
                        elif key.lower() == 'name':
                            user_field = user_detail.get('UserName', '')
                        elif key.lower() == 'id':
                            user_field = user_detail.get('UserId', '')
                        elif key.lower() == 'arn':
                            user_field = user_detail.get('Arn', '')
                        elif key.lower() == 'created_date':
                            user_field = user_detail.get('CreateDate', None)
                            if isinstance(user_field, datetime):
                                user_field = user_field.replace(tzinfo=None)
                                matched = _match_compare_condition(value, user_field, condition, matched)
                        elif key.lower() == 'password_last_used_date':
                            user_field = user_detail.get('PasswordLastUsed', None)
                            if isinstance(user_field, datetime):
                                user_field = user_field.replace(tzinfo=None)
                                matched = _match_compare_condition(value, user_field, condition, matched)
                        elif key.lower() == 'permissions_boundary_type':
                            if include_details:
                                user_detail = _get_user(self.session, user_detail.get('UserName', '')).get('User', {})
                                _permissions_boundary = user_detail.get('PermissionsBoundary', {})
                                user_field = _permissions_boundary.get('PermissionsBoundaryType', '')
                        elif key.lower() == 'permissions_boundary_arn':
                            if include_details:
                                user_detail = _get_user(self.session, user_detail.get('UserName', '')).get('User', {})
                                _permissions_boundary = user_detail.get('PermissionsBoundary', {})
                                user_field = _permissions_boundary.get('PermissionsBoundaryArn', '')
                        elif key.lower() == 'tag_key':
                            if include_details:
                                user_detail = _get_user(self.session, user_detail.get('UserName', '')).get('User', {})
                                tags = {tag['Key']: tag['Value'] for tag in user_detail.get('Tags', [])}
                                matched = _match_tag_condition(value, tags, condition, matched, key_only=True)
                        elif key.lower() == 'tag':
                            if include_details:
                                user_detail = _get_user(self.session, user_detail.get('UserName', '')).get('User', {})
                                tags = {tag['Key']: tag['Value'] for tag in user_detail.get('Tags', [])}
                                matched = _match_tag_condition(value, tags, condition, matched, key_only=False)
                        elif key.lower() == 'login_profile_created_date':
                            if include_details:
                                login_profile_detail = (
                                    _get_login_profile(self.session, user_detail.get('UserName', '')).get(
                                        'LoginProfile', {})
                                )
                                user_field = login_profile_detail.get('CreateDate', None)
                                if isinstance(user_field, datetime):
                                    user_field = user_field.replace(tzinfo=None)
                                    matched = _match_compare_condition(value, user_field, condition, matched)
                        elif key.lower() == 'login_profile_password_reset_required':
                            if include_details:
                                login_profile_detail = (
                                    _get_login_profile(self.session, user_detail.get('UserName', '')).get(
                                        'LoginProfile', {})
                                )
                                user_field = login_profile_detail.get('PasswordResetRequired', False)
                        elif key.lower() == 'access_key_id':
                            if include_details:
                                user_field = []
                                for access_key in _list_access_keys(self.session, user_detail.get('UserName', '')):
                                    user_field.append(access_key.get('AccessKeyId', ''))
                        elif key.lower() == 'access_key_status':
                            if include_details:
                                user_field = []
                                for access_key in _list_access_keys(self.session, user_detail.get('UserName', '')):
                                    user_field.append(access_key.get('Status', ''))
                        elif key.lower() == 'access_key_service':
                            if include_details:
                                user_field = []
                                for access_key in _list_access_keys(self.session, user_detail.get('UserName', '')):
                                    detail = _get_access_key_last_used(self.session, access_key.get('AccessKeyId', ''))
                                    if detail is not None:
                                        user_field.append(detail.get('AccessKeyLastUsed', {}).get('ServiceName', ''))
                        elif key.lower() == 'access_key_region':
                            if include_details:
                                user_field = []
                                for access_key in _list_access_keys(self.session, user_detail.get('UserName', '')):
                                    detail = _get_access_key_last_used(self.session, access_key.get('AccessKeyId', ''))
                                    if detail is not None:
                                        user_field.append(detail.get('AccessKeyLastUsed', {}).get('Region', ''))

                        if key.lower() not in [
                            'created_date', 'password_last_used_date', 'tag_key', 'tag', 'login_profile_created_date'
                        ]:
                            matched = _match_condition(value, user_field, condition, matched)

                        if (condition == OR and matched) or (condition == AND and not matched):
                            break

                if matched:
                    return _process_user(user_detail)

        users_to_return = []

        from botocore.exceptions import ClientError
        try:
            include_details_keys = {
                'permissions_boundary_type',
                'permissions_boundary_arn',
                'tag',
                'tag_key',
                'login_profile_created_date',
                'login_profile_password_reset_required',
                'access_key_id',
                'access_key_status',
                'access_key_service',
                'access_key_region'
            }

            if not include_details and any(k in include_details_keys for k in kwargs):
                raise SearchAttributeError(
                    f'include_details is required for below keys: {", ".join(sorted(include_details_keys))}'
                )

            users_to_process = _list_users(self.session)

            if len(kwargs) == 0:
                with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
                    future_to_user = {executor.submit(_process_user, user): user for user in users_to_process}
                    for future in as_completed(future_to_user):
                        user_result = future.result()
                        if user_result is not None:
                            users_to_return.append(user_result)
            else:
                with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
                    future_to_user = {executor.submit(_match_user, user): user for user in users_to_process}
                    for future in as_completed(future_to_user):
                        user_result = future.result()
                        if user_result is not None:
                            users_to_return.append(user_result)
        except ClientError as e:
            raise AdvanceSearchError('search_users', e)

        return users_to_return

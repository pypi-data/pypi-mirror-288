from botocore.exceptions import ClientError

from pyawsopstoolkit.__interfaces__ import ISession


def _get_role(session: ISession, role_name: str) -> dict:
    """
    Utilizing boto3 IAM, this method retrieves comprehensive details of an IAM role identified by the
    specified role name. Reference:
    https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/client/get_role.html
    :param session: The ISession object which provide access to AWS services.
    :type session: ISession
    :param role_name: The name of the IAM role.
    :type role_name: str
    :return: Details of the IAM role.
    :rtype: dict
    """
    try:
        iam_client = session.get_session().client('iam')
        return iam_client.get_role(RoleName=role_name)
    except ClientError as e:
        raise e


def _list_roles(session: ISession) -> list:
    """
    Utilizing boto3 IAM, this method retrieves a list of all roles leveraging the provided ISession object.
    Note: The returned dictionary excludes PermissionsBoundary, LastUsed, and Tags. Reference:
    https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/paginator/ListRoles.html
    :param session: The ISession object which provide access to AWS services.
    :type session: ISession
    :return: A list containing IAM roles.
    :rtype: list
    """
    roles_to_process = []

    try:
        iam_client = session.get_session().client('iam')
        iam_paginator = iam_client.get_paginator('list_roles')

        for page in iam_paginator.paginate():
            roles_to_process.extend(page.get('Roles', []))
    except ClientError as e:
        raise e

    return roles_to_process


def _get_access_key_last_used(session: ISession, access_key_id: str) -> dict:
    """
    Utilizing boto3 IAM, this method retrieves comprehensive details of IAM user access key last used information
    identified by the specified username. Reference:
    https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/client/get_access_key_last_used.html
    :param session: The ISession object which provide access to AWS services.
    :type session: ISession
    :param access_key_id: The ID of the IAM user access key.
    :type access_key_id: str
    :return: Details of the IAM user access key last used.
    :rtype: dict
    """
    try:
        iam_client = session.get_session().client('iam')
        return iam_client.get_access_key_last_used(AccessKeyId=access_key_id)
    except ClientError as e:
        raise e


def _get_login_profile(session: ISession, user_name: str) -> dict:
    """
    Utilizing boto3 IAM, this method retrieves comprehensive details of an IAM user login profile identified
    by the specified username. Reference:
    https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/client/get_login_profile.html
    :param session: The ISession object which provide access to AWS services.
    :type session: ISession
    :param user_name: The name of the IAM user.
    :type user_name: str
    :return: Details of the IAM user login profile.
    :rtype: dict
    """
    try:
        iam_client = session.get_session().client('iam')
        return iam_client.get_login_profile(UserName=user_name)
    except ClientError as e:
        raise e


def _get_user(session: ISession, user_name: str) -> dict:
    """
    Utilizing boto3 IAM, this method retrieves comprehensive details of an IAM user identified by the
    specified username. Reference:
    https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/client/get_user.html
    :param session: The ISession object which provide access to AWS services.
    :type session: ISession
    :param user_name: The name of the IAM user.
    :type user_name: str
    :return: Details of the IAM user.
    :rtype: dict
    """
    try:
        iam_client = session.get_session().client('iam')
        return iam_client.get_user(UserName=user_name)
    except ClientError as e:
        raise e


def _list_access_keys(session: ISession, user_name: str) -> list:
    """
    Utilizing boto3 IAM, this method retrieves a list of all access keys associated with IAM user leveraging the
    provided ISession object. Reference:
    https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/paginator/ListAccessKeys.html
    :param session: The ISession object which provide access to AWS services.
    :type session: ISession
    :param user_name: The name of the IAM user.
    :type user_name: str
    :return: A list containing IAM user access keys.
    :rtype: list
    """
    access_keys_to_process = []

    try:
        iam_client = session.get_session().client('iam')
        iam_paginator = iam_client.get_paginator('list_access_keys')

        for page in iam_paginator.paginate(UserName=user_name):
            access_keys_to_process.extend(page.get('AccessKeyMetadata', []))
    except ClientError as e:
        raise e

    return access_keys_to_process


def _list_users(session: ISession) -> list:
    """
    Utilizing boto3 IAM, this method retrieves a list of all users leveraging the provided ISession object.
    Note: The returned dictionary excludes PermissionsBoundary and Tags. Reference:
    https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/paginator/ListUsers.html
    :param session: The ISession object which provide access to AWS services.
    :type session: ISession
    :return: A list containing IAM users.
    :rtype: list
    """
    users_to_process = []

    try:
        iam_client = session.get_session().client('iam')
        iam_paginator = iam_client.get_paginator('list_users')

        for page in iam_paginator.paginate():
            users_to_process.extend(page.get('Users', []))
    except ClientError as e:
        raise e

    return users_to_process

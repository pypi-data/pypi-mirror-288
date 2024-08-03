from botocore.config import Config
from botocore.exceptions import ClientError

from pyawsopstoolkit.__interfaces__ import ISession


def _list_security_groups(session: ISession, region: str) -> list:
    """
    Utilizing boto3 IAM, this method retrieves a list of all security groups leveraging the provided ISession object.
    Reference:
    https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeSecurityGroups.html
    :param session: The ISession object which provide access to AWS services.
    :type session: ISession
    :param region: The region to search security groups for.
    :type region: str
    :return: A list of EC2 security groups.
    :rtype: list
    """
    security_groups_to_process = []

    try:
        ec2_client = session.get_session().client('ec2', config=Config(region))
        ec2_paginator = ec2_client.get_paginator('describe_security_groups')

        for page in ec2_paginator.paginate():
            security_groups_to_process.extend(page.get('SecurityGroups', []))
    except ClientError as e:
        raise e

    return security_groups_to_process

from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass

from pyawsopstoolkit.__globals__ import MAX_WORKERS
from pyawsopstoolkit.__interfaces__ import ISession, IAccount
from pyawsopstoolkit.__validations__ import Validation
from pyawsopstoolkit.advsearch import OR, AND
from pyawsopstoolkit.advsearch.__main__ import _match_condition, _match_tag_condition, _match_number_condition, \
    _match_number_range_condition
from pyawsopstoolkit.advsearch.ec2.__handlers__ import _list_security_groups
from pyawsopstoolkit.exceptions import AdvanceSearchError
from pyawsopstoolkit.validators import Validator


@dataclass
class SecurityGroup:
    """
    A class representing advance search features related with EC2 security groups.
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
    def _convert_to_ec2_security_group(account: IAccount, region: str, sg: dict):
        """
        This function transforms the dictionary response from boto3 EC2 into a format compatible with the
        AWS Ops Toolkit, adhering to the pyawsopstoolkit.models structure. Additionally, it incorporates
        account-related summary information into the EC2 security group details.
        :param account: An IAccount object containing AWS account information.
        :type account: IAccount
        :param region: The region associated with the EC2 security group.
        :type region: str
        :param sg: The boto3 EC2 service response for the security group.
        :type sg: dict
        :return: An AWS Ops Toolkit compatible object containing all EC2 security group details.
        :rtype: pyawsopstoolkit.models.ec2.security_group.SecurityGroup
        """
        from pyawsopstoolkit.models.ec2.security_group import SecurityGroup, IPPermission, IPRange, IPv6Range, \
            PrefixList, UserIDGroupPair

        def _create_ip_permission(perm):
            ip_permission = IPPermission(
                from_port=perm.get('FromPort', 0),
                to_port=perm.get('ToPort', 0),
                ip_protocol=perm.get('IpProtocol', '')
            )

            ip_permission.ip_ranges = [
                IPRange(cidr_ip=ip.get('CidrIp', ''), description=ip.get('Description', ''))
                for ip in perm.get('IpRanges', [])
            ]

            ip_permission.ipv6_ranges = [
                IPv6Range(cidr_ipv6=ip.get('CidrIpv6', ''), description=ip.get('Description', ''))
                for ip in perm.get('Ipv6Ranges', [])
            ]

            ip_permission.prefix_lists = [
                PrefixList(id=prefix.get('PrefixListId', ''), description=prefix.get('Description', ''))
                for prefix in perm.get('PrefixListIds', [])
            ]

            ip_permission.user_id_group_pairs = [
                UserIDGroupPair(
                    id=pair.get('GroupId', ''),
                    name=pair.get('GroupName', ''),
                    status=pair.get('PeeringStatus', ''),
                    user_id=pair.get('UserId', ''),
                    vpc_id=pair.get('VpcId', ''),
                    description=pair.get('Description', ''),
                    vpc_peering_connection_id=pair.get('VpcPeeringConnectionId', '')
                )
                for pair in perm.get('UserIdGroupPairs', [])
            ]

            return ip_permission

        ec2_security_group = SecurityGroup(
            account=account,
            region=region,
            id=sg.get('GroupId', ''),
            name=sg.get('GroupName', ''),
            owner_id=sg.get('OwnerId', ''),
            vpc_id=sg.get('VpcId', '')
        )

        ec2_security_group.ip_permissions = [
            _create_ip_permission(perm) for perm in sg.get('IpPermissions', [])
        ]

        ec2_security_group.ip_permissions_egress = [
            _create_ip_permission(perm) for perm in sg.get('IpPermissionsEgress', [])
        ]

        ec2_security_group.tags = sg.get('Tags', [])

        return ec2_security_group

    def search_security_groups(
            self,
            condition: str = OR,
            region: str | list = 'eu-west-1',
            **kwargs
    ) -> list:
        """
        Returns a list of EC2 security groups using advanced search feature supported by the specified arguments.
        For details on supported kwargs, please refer to the readme document.
        """
        Validation.validate_type(condition, str, 'condition should be a string and should be either "OR" or "AND".')
        if isinstance(region, str):
            Validator.region(region, True)
        elif isinstance(region, list):
            all(Validator.region(r, True) for r in region)
        else:
            raise ValueError('region should be a string or list of strings.')

        def _process_security_group(sg_detail, _region):
            return self._convert_to_ec2_security_group(self.session.get_account(), _region, sg_detail)

        def _match_security_group(sg_detail, _region):
            if sg_detail:
                matched = False if condition == OR else True
                for key, value in kwargs.items():
                    if value is not None:
                        sg_field = ''
                        if key.lower() == 'id':
                            sg_field = sg_detail.get('GroupId', '')
                        elif key.lower() == 'name':
                            sg_field = sg_detail.get('GroupName', '')
                        elif key.lower() == 'owner_id':
                            sg_field = sg_detail.get('OwnerId', '')
                        elif key.lower() == 'vpc_id':
                            sg_field = sg_detail.get('VpcId', '')
                        elif key.lower() == 'description':
                            sg_field = sg_detail.get('Description', '')
                        elif key.lower() == 'tag_key':
                            tags = {tag['Key']: tag['Value'] for tag in sg_detail.get('Tags', [])}
                            matched = _match_tag_condition(value, tags, condition, matched, key_only=True)
                        elif key.lower() == 'tag':
                            tags = {tag['Key']: tag['Value'] for tag in sg_detail.get('Tags', [])}
                            matched = _match_tag_condition(value, tags, condition, matched, key_only=False)
                        elif key.lower() == 'in_from_port':
                            ip_permissions = sg_detail.get('IpPermissions', [])
                            sg_field = [ip_prem.get('FromPort', 0) for ip_prem in ip_permissions]
                            matched = _match_number_condition(value, sg_field, condition, matched)
                        elif key.lower() == 'out_from_port':
                            ip_permissions = sg_detail.get('IpPermissionsEgress', [])
                            sg_field = [ip_prem.get('FromPort', 0) for ip_prem in ip_permissions]
                            matched = _match_number_condition(value, sg_field, condition, matched)
                        elif key.lower() == 'in_to_port':
                            ip_permissions = sg_detail.get('IpPermissions', [])
                            sg_field = [ip_prem.get('ToPort', 0) for ip_prem in ip_permissions]
                            matched = _match_number_condition(value, sg_field, condition, matched)
                        elif key.lower() == 'out_to_port':
                            ip_permissions = sg_detail.get('IpPermissionsEgress', [])
                            sg_field = [ip_prem.get('ToPort', 0) for ip_prem in ip_permissions]
                            matched = _match_number_condition(value, sg_field, condition, matched)
                        elif key.lower() == 'in_port_range':
                            ip_permissions = sg_detail.get('IpPermissions', [])
                            sg_field = [
                                (ip_prem.get('FromPort', 0), ip_prem.get('ToPort', 0)) for ip_prem in ip_permissions
                            ]
                            matched = _match_number_range_condition(value, sg_field, condition, matched)
                        elif key.lower() == 'out_port_range':
                            ip_permissions = sg_detail.get('IpPermissionsEgress', [])
                            sg_field = [
                                (ip_prem.get('FromPort', 0), ip_prem.get('ToPort', 0)) for ip_prem in ip_permissions
                            ]
                            matched = _match_number_range_condition(value, sg_field, condition, matched)
                        elif key.lower() == 'in_ip_protocol':
                            ip_permissions = sg_detail.get('IpPermissions', [])
                            sg_field = [
                                ip_prem.get('IpProtocol', '').replace('-1', 'all') for ip_prem in ip_permissions
                            ]
                        elif key.lower() == 'out_ip_protocol':
                            ip_permissions = sg_detail.get('IpPermissionsEgress', [])
                            sg_field = [
                                ip_prem.get('IpProtocol', '').replace('-1', value) for ip_prem in ip_permissions
                            ]

                        if key.lower() not in [
                            'tag_key', 'tag', 'in_from_port', 'out_from_port', 'in_to_port', 'out_to_port',
                            'in_port_range', 'out_port_range'
                        ]:
                            matched = _match_condition(value, sg_field, condition, matched)

                        if (condition == OR and matched) or (condition == AND and not matched):
                            break

                if matched:
                    return _process_security_group(sg_detail, _region)

        security_groups_to_return = []
        regions_to_process = [region] if isinstance(region, str) else region

        from botocore.exceptions import ClientError
        try:
            for _region in regions_to_process:
                security_groups_to_process = _list_security_groups(self.session, _region)

                if len(kwargs) == 0:
                    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
                        future_to_sg = {
                            executor.submit(_process_security_group, sg, _region): sg
                            for sg in security_groups_to_process
                        }
                        for future in as_completed(future_to_sg):
                            sg_result = future.result()
                            if sg_result is not None:
                                security_groups_to_return.append(sg_result)
                else:
                    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
                        future_to_sg = {
                            executor.submit(_match_security_group, sg, _region): sg
                            for sg in security_groups_to_process
                        }
                        for future in as_completed(future_to_sg):
                            sg_result = future.result()
                            if sg_result is not None:
                                security_groups_to_return.append(sg_result)
        except ClientError as e:
            raise AdvanceSearchError('search_security_groups', e)

        return security_groups_to_return

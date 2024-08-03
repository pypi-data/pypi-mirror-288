from dataclasses import dataclass
from typing import Optional, Union

from pyawsopstoolkit.__interfaces__ import IAccount
from pyawsopstoolkit.__validations__ import Validation
from pyawsopstoolkit.validators import Validator


@dataclass
class IPRange:
    """
    A class representing IPv4 range for a EC2 Security Group.
    """
    cidr_ip: str
    description: Optional[str] = None

    def __post_init__(self):
        for field_name, field_value in self.__dataclass_fields__.items():
            self.__validate__(field_name)

    def __validate__(self, field_name):
        field_value = getattr(self, field_name)
        if field_name in ['cidr_ip']:
            Validation.validate_type(field_value, str, f'{field_name} should be a string.')
        elif field_name in ['description']:
            Validation.validate_type(field_value, Union[str, None], f'{field_name} should be a string.')

    def __setattr__(self, key, value):
        super().__setattr__(key, value)
        if key in self.__dataclass_fields__:
            self.__validate__(key)

    def to_dict(self) -> dict:
        """
        Returns a dictionary representation of the IPRange instance.
        :return: Dictionary representation of the IPRange instance.
        :rtype: dict
        """
        return {
            "cidr_ip": self.cidr_ip,
            "description": self.description
        }


@dataclass
class IPv6Range:
    """
    A class representing IPv6 range for a EC2 Security Group.
    """
    cidr_ipv6: str
    description: Optional[str] = None

    def __post_init__(self):
        for field_name, field_value in self.__dataclass_fields__.items():
            self.__validate__(field_name)

    def __validate__(self, field_name):
        field_value = getattr(self, field_name)
        if field_name in ['cidr_ipv6']:
            Validation.validate_type(field_value, str, f'{field_name} should be a string.')
        elif field_name in ['description']:
            Validation.validate_type(field_value, Union[str, None], f'{field_name} should be a string.')

    def __setattr__(self, key, value):
        super().__setattr__(key, value)
        if key in self.__dataclass_fields__:
            self.__validate__(key)

    def to_dict(self) -> dict:
        """
        Returns a dictionary representation of the IPv6Range instance.
        :return: Dictionary representation of the IPv6Range instance.
        :rtype: dict
        """
        return {
            "cidr_ipv6": self.cidr_ipv6,
            "description": self.description
        }


@dataclass
class PrefixList:
    """
    A class representing Prefix List for a EC2 Security Group.
    """
    id: str
    description: Optional[str] = None

    def __post_init__(self):
        for field_name, field_value in self.__dataclass_fields__.items():
            self.__validate__(field_name)

    def __validate__(self, field_name):
        field_value = getattr(self, field_name)
        if field_name in ['id']:
            Validation.validate_type(field_value, str, f'{field_name} should be a string.')
        elif field_name in ['description']:
            Validation.validate_type(field_value, Union[str, None], f'{field_name} should be a string.')

    def __setattr__(self, key, value):
        super().__setattr__(key, value)
        if key in self.__dataclass_fields__:
            self.__validate__(key)

    def to_dict(self) -> dict:
        """
        Returns a dictionary representation of the PrefixList instance.
        :return: Dictionary representation of the PrefixList instance.
        :rtype: dict
        """
        return {
            "id": self.id,
            "description": self.description
        }


@dataclass
class UserIDGroupPair:
    """
    A class representing User ID Group Pair for a EC2 Security Group.
    """
    id: str
    name: str
    status: str
    user_id: str
    vpc_id: str
    description: Optional[str] = None
    vpc_peering_connection_id: Optional[str] = None

    def __post_init__(self):
        for field_name, field_value in self.__dataclass_fields__.items():
            self.__validate__(field_name)

    def __validate__(self, field_name):
        field_value = getattr(self, field_name)
        if field_name in ['id', 'name', 'status', 'user_id', 'vpc_id']:
            Validation.validate_type(field_value, str, f'{field_name} should be a string.')
        elif field_name in ['description', 'vpc_peering_connection_id']:
            Validation.validate_type(field_value, Union[str, None], f'{field_name} should be a string.')

    def __setattr__(self, key, value):
        super().__setattr__(key, value)
        if key in self.__dataclass_fields__:
            self.__validate__(key)

    def to_dict(self) -> dict:
        """
        Returns a dictionary representation of the UserIDGroupPair instance.
        :return: Dictionary representation of the UserIDGroupPair instance.
        :rtype: dict
        """
        return {
            "id": self.id,
            "name": self.name,
            "status": self.status,
            "user_id": self.user_id,
            "vpc_id": self.vpc_id,
            "description": self.description,
            "vpc_peering_connection_id": self.vpc_peering_connection_id
        }


@dataclass
class IPPermission:
    """
    A class representing the IP Permissions for a EC2 Security Group.
    """
    from_port: int
    to_port: int
    ip_protocol: str
    ip_ranges: Optional[list[IPRange]] = None
    ipv6_ranges: Optional[list[IPv6Range]] = None
    prefix_lists: Optional[list[PrefixList]] = None
    user_id_group_pairs: Optional[list[UserIDGroupPair]] = None

    def __post_init__(self):
        for field_name, field_value in self.__dataclass_fields__.items():
            self.__validate__(field_name)

    def __validate__(self, field_name):
        mappings = {
            'ip_ranges': IPRange,
            'ipv6_ranges': IPv6Range,
            'prefix_lists': PrefixList,
            'user_id_group_pairs': UserIDGroupPair
        }
        field_value = getattr(self, field_name)
        if field_name in ['from_port', 'to_port']:
            Validation.validate_type(field_value, int, f'{field_name} should be an integer.')
        elif field_name in ['ip_protocol']:
            Validation.validate_type(field_value, str, f'{field_name} should be a string.')
        elif field_name in ['ip_ranges', 'ipv6_ranges', 'prefix_lists', 'user_id_group_pairs']:
            field_type = mappings.get(field_name)
            message = f'{field_name} should be of {field_type.__name__} type.'
            Validation.validate_type(field_value, Union[list, None], message)
            if field_value is not None and len(field_value) > 0:
                all(Validation.validate_type(item, field_type, message) for item in field_value)

    def __setattr__(self, key, value):
        super().__setattr__(key, value)
        if key in self.__dataclass_fields__:
            self.__validate__(key)

    def to_dict(self) -> dict:
        """
        Returns a dictionary representation of the IPPermission instance.
        :return: Dictionary representation of the IPPermission instance.
        :rtype: dict
        """
        return {
            "from_port": self.from_port,
            "to_port": self.to_port,
            "ip_protocol": self.ip_protocol,
            "ip_ranges": [
                ip.to_dict() for ip in self.ip_ranges
            ] if self.ip_ranges and len(self.ip_ranges) > 0 else None,
            "ipv6_ranges": [
                ip.to_dict() for ip in self.ipv6_ranges
            ] if self.ipv6_ranges and len(self.ipv6_ranges) > 0 else None,
            "prefix_lists": [
                prefix.to_dict() for prefix in self.prefix_lists
            ] if self.prefix_lists and len(self.prefix_lists) > 0 else None,
            "user_id_group_pairs": [
                pair.to_dict() for pair in self.user_id_group_pairs
            ] if self.user_id_group_pairs and len(self.user_id_group_pairs) > 0 else None
        }


@dataclass
class SecurityGroup:
    """
    A class representing the EC2 Security Group.
    """
    account: IAccount
    region: str
    id: str
    name: str
    owner_id: str
    vpc_id: str
    ip_permissions: Optional[list[IPPermission]] = None
    ip_permissions_egress: Optional[list[IPPermission]] = None
    description: Optional[str] = None
    tags: Optional[list] = None

    def __post_init__(self):
        for field_name, field_value in self.__dataclass_fields__.items():
            self.__validate__(field_name)

    def __validate__(self, field_name):
        mappings = {
            'account': IAccount,
            'ip_permissions': IPPermission,
            'ip_permissions_egress': IPPermission,
            'tags': list
        }
        field_value = getattr(self, field_name)
        field_type = mappings.get(field_name)
        if field_name in ['account']:
            Validation.validate_type(field_value, field_type, f'{field_name} should be of {field_type.__name__} type.')
        elif field_name in ['region']:
            Validator.region(field_value, True)
        elif field_name in ['id', 'name', 'owner_id', 'vpc_id']:
            Validation.validate_type(field_value, str, f'{field_name} should be a string.')
        elif field_name in ['ip_permissions', 'ip_permissions_egress', 'tags']:
            Validation.validate_type(
                field_value, Union[list, None], f'{field_name} should be a list of {field_type.__name__} type.'
            )
            if field_name != 'tags':
                if field_value is not None and len(field_value) > 0:
                    all(
                        Validation.validate_type(
                            item, field_type, f'{field_name} should be a list of {field_type.__name__} type.'
                        ) for item in field_value
                    )
        elif field_name in ['description']:
            Validation.validate_type(field_value, Union[str, None], f'{field_name} should be of string.')

    def __setattr__(self, key, value):
        super().__setattr__(key, value)
        if key in self.__dataclass_fields__:
            self.__validate__(key)

    def to_dict(self) -> dict:
        """
        Returns a dictionary representation of the SecurityGroup instance.
        :return: Dictionary representation of the SecurityGroup instance.
        :rtype: dict
        """
        return {
            "account": self.account.to_dict(),
            "region": self.region,
            "id": self.id,
            "name": self.name,
            "owner_id": self.owner_id,
            "vpc_id": self.vpc_id,
            "ip_permissions": [
                ip_perm.to_dict() for ip_perm in self.ip_permissions
            ] if self.ip_permissions and len(self.ip_permissions) > 0 else None,
            "ip_permissions_egress": [
                ip_perm.to_dict() for ip_perm in self.ip_permissions_egress
            ] if self.ip_permissions_egress and len(self.ip_permissions_egress) > 0 else None,
            "description": self.description,
            "tags": self.tags
        }

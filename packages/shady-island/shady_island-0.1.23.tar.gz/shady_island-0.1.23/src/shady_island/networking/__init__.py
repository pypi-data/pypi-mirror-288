from pkgutil import extend_path
__path__ = extend_path(__path__, __name__)

import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from typeguard import check_type

from .._jsii import *

import aws_cdk as _aws_cdk_ceddda9d
import aws_cdk.aws_certificatemanager as _aws_cdk_aws_certificatemanager_ceddda9d
import aws_cdk.aws_ec2 as _aws_cdk_aws_ec2_ceddda9d
import aws_cdk.aws_elasticloadbalancingv2 as _aws_cdk_aws_elasticloadbalancingv2_ceddda9d
import aws_cdk.aws_iam as _aws_cdk_aws_iam_ceddda9d
import aws_cdk.aws_secretsmanager as _aws_cdk_aws_secretsmanager_ceddda9d
import constructs as _constructs_77d1e7e8


class AddressingV4(
    metaclass=jsii.JSIIMeta,
    jsii_type="shady-island.networking.AddressingV4",
):
    '''Used to assign IPv4 addresses to a Network Interface.'''

    @jsii.member(jsii_name="prefixCount")
    @builtins.classmethod
    def prefix_count(cls, count: jsii.Number) -> "AddressingV4":
        '''Specify a number of IPv4 delegated prefixes to automatically assign.

        :param count: - The number of automatic IPv4 delegated prefixes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b2cddb2547e4ed3f4826e1acff079d40a4ba476ac141e3281f8b106c7455a04f)
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
        return typing.cast("AddressingV4", jsii.sinvoke(cls, "prefixCount", [count]))

    @jsii.member(jsii_name="prefixes")
    @builtins.classmethod
    def prefixes(cls, prefixes: typing.Sequence[builtins.str]) -> "AddressingV4":
        '''Specify one or more IPv4 delegated prefixes to assign.

        IPv4 prefixes must be within a CIDR of /28.

        :param prefixes: - The IPv4 delegated prefixes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__01734a2088506c2015ca7bad849bebf81f4652662c5abd2af6e22d7e89d72a62)
            check_type(argname="argument prefixes", value=prefixes, expected_type=type_hints["prefixes"])
        return typing.cast("AddressingV4", jsii.sinvoke(cls, "prefixes", [prefixes]))

    @jsii.member(jsii_name="privateAddress")
    @builtins.classmethod
    def private_address(cls, ip: builtins.str) -> "AddressingV4":
        '''Specify a private IPv4 address.

        :param ip: - The actual IP address.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a558c981ad684205ae14b30ac86b63891341637e8de2255215f0d7fa9890c208)
            check_type(argname="argument ip", value=ip, expected_type=type_hints["ip"])
        return typing.cast("AddressingV4", jsii.sinvoke(cls, "privateAddress", [ip]))

    @jsii.member(jsii_name="privateAddressAndSecondaryCount")
    @builtins.classmethod
    def private_address_and_secondary_count(
        cls,
        primary: builtins.str,
        count: jsii.Number,
    ) -> "AddressingV4":
        '''Specify a primary IPv4 address and a number of secondary addresses.

        :param primary: - The primary address.
        :param count: - The number of secondary addresses.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dbd385d7d0a4b0a0306d6f92007994dc4caacd4f45b60696b74868ae7d9af7dc)
            check_type(argname="argument primary", value=primary, expected_type=type_hints["primary"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
        return typing.cast("AddressingV4", jsii.sinvoke(cls, "privateAddressAndSecondaryCount", [primary, count]))

    @jsii.member(jsii_name="privateAddresses")
    @builtins.classmethod
    def private_addresses(
        cls,
        primary: builtins.str,
        *secondary: builtins.str,
    ) -> "AddressingV4":
        '''Specify a primary IPv4 address and one or more secondary IPv4 addresses.

        :param primary: - The primary address.
        :param secondary: - Any secondary addresses.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__116c136600050bf89a1560721d3862fb3f20a3f55eeb11598bcf8676ad8363f8)
            check_type(argname="argument primary", value=primary, expected_type=type_hints["primary"])
            check_type(argname="argument secondary", value=secondary, expected_type=typing.Tuple[type_hints["secondary"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast("AddressingV4", jsii.sinvoke(cls, "privateAddresses", [primary, *secondary]))

    @builtins.property
    @jsii.member(jsii_name="props")
    def props(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "props"))


class AddressingV6(
    metaclass=jsii.JSIIMeta,
    jsii_type="shady-island.networking.AddressingV6",
):
    '''Used to assign IPv6 addresses to a Network Interface.'''

    @jsii.member(jsii_name="addressCount")
    @builtins.classmethod
    def address_count(
        cls,
        count: jsii.Number,
        enable_primary: typing.Optional[builtins.bool] = None,
    ) -> "AddressingV6":
        '''Specify a number of IPv6 addresses to automatically assign.

        :param count: - The number of automatic IPv6 addresses.
        :param enable_primary: - Whether to enable a primary IPv6 GUA (default: no).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ed7da7903260aeba9877acff158981d9b2220d2610bb60c1601ce4a1cd07c80)
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument enable_primary", value=enable_primary, expected_type=type_hints["enable_primary"])
        return typing.cast("AddressingV6", jsii.sinvoke(cls, "addressCount", [count, enable_primary]))

    @jsii.member(jsii_name="addresses")
    @builtins.classmethod
    def addresses(
        cls,
        ips: typing.Sequence[builtins.str],
        enable_primary: typing.Optional[builtins.bool] = None,
    ) -> "AddressingV6":
        '''Specify one or more IPv6 addresses to assign.

        :param ips: - The IPv6 addresses.
        :param enable_primary: - Whether to enable a primary IPv6 GUA (default: no).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16d92cdccfc5fcd12837debeb037bdf436f91a88257fd9f12e9dbea4b9846925)
            check_type(argname="argument ips", value=ips, expected_type=type_hints["ips"])
            check_type(argname="argument enable_primary", value=enable_primary, expected_type=type_hints["enable_primary"])
        return typing.cast("AddressingV6", jsii.sinvoke(cls, "addresses", [ips, enable_primary]))

    @jsii.member(jsii_name="prefixCount")
    @builtins.classmethod
    def prefix_count(
        cls,
        count: jsii.Number,
        enable_primary: typing.Optional[builtins.bool] = None,
    ) -> "AddressingV6":
        '''Specify a number of IPv6 delegated prefixes to automatically assign.

        :param count: - The number of automatic IPv6 delegated prefixes.
        :param enable_primary: - Whether to enable a primary IPv6 GUA (default: no).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3cd14df44bfcf87b8b5d2f04ad616f4497ecc8908a4f4f91379e46248a6772ee)
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument enable_primary", value=enable_primary, expected_type=type_hints["enable_primary"])
        return typing.cast("AddressingV6", jsii.sinvoke(cls, "prefixCount", [count, enable_primary]))

    @jsii.member(jsii_name="prefixes")
    @builtins.classmethod
    def prefixes(
        cls,
        prefixes: typing.Sequence[builtins.str],
        enable_primary: typing.Optional[builtins.bool] = None,
    ) -> "AddressingV6":
        '''Specify one or more IPv6 delegated prefixes to assign.

        IPv6 prefixes must be within a CIDR of /80.

        :param prefixes: - The IPv6 delegated prefixes.
        :param enable_primary: - Whether to enable a primary IPv6 GUA (default: no).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4a8ad5afeb3637eae637f3afd75db4bc00b4274d8a8d486fdf734229f61687f)
            check_type(argname="argument prefixes", value=prefixes, expected_type=type_hints["prefixes"])
            check_type(argname="argument enable_primary", value=enable_primary, expected_type=type_hints["enable_primary"])
        return typing.cast("AddressingV6", jsii.sinvoke(cls, "prefixes", [prefixes, enable_primary]))

    @builtins.property
    @jsii.member(jsii_name="props")
    def props(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "props"))


@jsii.data_type(
    jsii_type="shady-island.networking.ElasticIpProps",
    jsii_struct_bases=[],
    name_mapping={"removal_policy": "removalPolicy"},
)
class ElasticIpProps:
    def __init__(
        self,
        *,
        removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
    ) -> None:
        '''Constructor properties for ElasticIp.

        :param removal_policy: The removal policy for this resource.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e06451a98b33ab08a35c0a78b3d4d4c1c765f25e0a9ce8b560db827f5e389a61)
            check_type(argname="argument removal_policy", value=removal_policy, expected_type=type_hints["removal_policy"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if removal_policy is not None:
            self._values["removal_policy"] = removal_policy

    @builtins.property
    def removal_policy(self) -> typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy]:
        '''The removal policy for this resource.'''
        result = self._values.get("removal_policy")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ElasticIpProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.interface(jsii_type="shady-island.networking.IElasticIp")
class IElasticIp(_aws_cdk_ceddda9d.IResource, typing_extensions.Protocol):
    '''An EC2 Elastic IP address.'''

    @builtins.property
    @jsii.member(jsii_name="allocationId")
    def allocation_id(self) -> builtins.str:
        '''The allocation ID of the Elastic IP address.'''
        ...

    @builtins.property
    @jsii.member(jsii_name="elasticIpArn")
    def elastic_ip_arn(self) -> builtins.str:
        '''The ARN of the Elastic IP address.'''
        ...

    @jsii.member(jsii_name="grant")
    def grant(
        self,
        identity: _aws_cdk_aws_iam_ceddda9d.IGrantable,
        *actions: builtins.str,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''Grant the given identity custom permissions.

        e.g. ``ec2:AssociateAddress``, ``ec2:DisableAddressTransfer``,
        ``ec2:DisassociateAddress``, ``ec2:EnableAddressTransfer``, among others.

        :param identity: - The resource with a grantPrincipal property.
        :param actions: - The IAM actions to allow.

        :return: The new Grant
        '''
        ...


class _IElasticIpProxy(
    jsii.proxy_for(_aws_cdk_ceddda9d.IResource), # type: ignore[misc]
):
    '''An EC2 Elastic IP address.'''

    __jsii_type__: typing.ClassVar[str] = "shady-island.networking.IElasticIp"

    @builtins.property
    @jsii.member(jsii_name="allocationId")
    def allocation_id(self) -> builtins.str:
        '''The allocation ID of the Elastic IP address.'''
        return typing.cast(builtins.str, jsii.get(self, "allocationId"))

    @builtins.property
    @jsii.member(jsii_name="elasticIpArn")
    def elastic_ip_arn(self) -> builtins.str:
        '''The ARN of the Elastic IP address.'''
        return typing.cast(builtins.str, jsii.get(self, "elasticIpArn"))

    @jsii.member(jsii_name="grant")
    def grant(
        self,
        identity: _aws_cdk_aws_iam_ceddda9d.IGrantable,
        *actions: builtins.str,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''Grant the given identity custom permissions.

        e.g. ``ec2:AssociateAddress``, ``ec2:DisableAddressTransfer``,
        ``ec2:DisassociateAddress``, ``ec2:EnableAddressTransfer``, among others.

        :param identity: - The resource with a grantPrincipal property.
        :param actions: - The IAM actions to allow.

        :return: The new Grant
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c038201c2cdaabf12b23bf40d541b0618f6bd20657383b850c9ff3a6d96fdfb)
            check_type(argname="argument identity", value=identity, expected_type=type_hints["identity"])
            check_type(argname="argument actions", value=actions, expected_type=typing.Tuple[type_hints["actions"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.Grant, jsii.invoke(self, "grant", [identity, *actions]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IElasticIp).__jsii_proxy_class__ = lambda : _IElasticIpProxy


@jsii.interface(jsii_type="shady-island.networking.INetworkInterface")
class INetworkInterface(
    _constructs_77d1e7e8.IConstruct,
    _aws_cdk_aws_ec2_ceddda9d.IConnectable,
    typing_extensions.Protocol,
):
    '''An Elastic Network Interface.'''

    @builtins.property
    @jsii.member(jsii_name="networkInterfaceId")
    def network_interface_id(self) -> builtins.str:
        '''The ID of this Network Interface.'''
        ...


class _INetworkInterfaceProxy(
    jsii.proxy_for(_constructs_77d1e7e8.IConstruct), # type: ignore[misc]
    jsii.proxy_for(_aws_cdk_aws_ec2_ceddda9d.IConnectable), # type: ignore[misc]
):
    '''An Elastic Network Interface.'''

    __jsii_type__: typing.ClassVar[str] = "shady-island.networking.INetworkInterface"

    @builtins.property
    @jsii.member(jsii_name="networkInterfaceId")
    def network_interface_id(self) -> builtins.str:
        '''The ID of this Network Interface.'''
        return typing.cast(builtins.str, jsii.get(self, "networkInterfaceId"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, INetworkInterface).__jsii_proxy_class__ = lambda : _INetworkInterfaceProxy


@jsii.interface(jsii_type="shady-island.networking.ISecretHttpHeader")
class ISecretHttpHeader(_constructs_77d1e7e8.IConstruct, typing_extensions.Protocol):
    '''Interface for SecretHttpHeader.'''

    @builtins.property
    @jsii.member(jsii_name="headerName")
    def header_name(self) -> builtins.str:
        '''The name of the secret header.'''
        ...

    @builtins.property
    @jsii.member(jsii_name="headerValue")
    def header_value(self) -> _aws_cdk_ceddda9d.SecretValue:
        '''The value of the secret header.'''
        ...

    @jsii.member(jsii_name="createListenerCondition")
    def create_listener_condition(
        self,
    ) -> _aws_cdk_aws_elasticloadbalancingv2_ceddda9d.ListenerCondition:
        '''Get a ListenerCondition that represents this secret header.

        :return: The appropriate ListenerCondition.
        '''
        ...

    @jsii.member(jsii_name="createOriginCustomHeaders")
    def create_origin_custom_headers(
        self,
    ) -> typing.Mapping[builtins.str, builtins.str]:
        '''Gets the custom headers for a CloudFront origin configuration.

        :return: An object with the header name and header value.
        '''
        ...


class _ISecretHttpHeaderProxy(
    jsii.proxy_for(_constructs_77d1e7e8.IConstruct), # type: ignore[misc]
):
    '''Interface for SecretHttpHeader.'''

    __jsii_type__: typing.ClassVar[str] = "shady-island.networking.ISecretHttpHeader"

    @builtins.property
    @jsii.member(jsii_name="headerName")
    def header_name(self) -> builtins.str:
        '''The name of the secret header.'''
        return typing.cast(builtins.str, jsii.get(self, "headerName"))

    @builtins.property
    @jsii.member(jsii_name="headerValue")
    def header_value(self) -> _aws_cdk_ceddda9d.SecretValue:
        '''The value of the secret header.'''
        return typing.cast(_aws_cdk_ceddda9d.SecretValue, jsii.get(self, "headerValue"))

    @jsii.member(jsii_name="createListenerCondition")
    def create_listener_condition(
        self,
    ) -> _aws_cdk_aws_elasticloadbalancingv2_ceddda9d.ListenerCondition:
        '''Get a ListenerCondition that represents this secret header.

        :return: The appropriate ListenerCondition.
        '''
        return typing.cast(_aws_cdk_aws_elasticloadbalancingv2_ceddda9d.ListenerCondition, jsii.invoke(self, "createListenerCondition", []))

    @jsii.member(jsii_name="createOriginCustomHeaders")
    def create_origin_custom_headers(
        self,
    ) -> typing.Mapping[builtins.str, builtins.str]:
        '''Gets the custom headers for a CloudFront origin configuration.

        :return: An object with the header name and header value.
        '''
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.invoke(self, "createOriginCustomHeaders", []))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, ISecretHttpHeader).__jsii_proxy_class__ = lambda : _ISecretHttpHeaderProxy


@jsii.enum(jsii_type="shady-island.networking.InterfaceType")
class InterfaceType(enum.Enum):
    '''The type of Network Interface.'''

    INTERFACE = "INTERFACE"
    '''A standard ENI.'''
    EFA = "EFA"
    '''An Elastic Fabric Adapter ENI.'''
    TRUNK = "TRUNK"
    '''An ENI for use with ECS awsvpc trunking.'''


@jsii.implements(INetworkInterface)
class NetworkInterface(
    _aws_cdk_ceddda9d.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="shady-island.networking.NetworkInterface",
):
    '''A Network Interface.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        subnet: _aws_cdk_aws_ec2_ceddda9d.ISubnet,
        vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
        description: typing.Optional[builtins.str] = None,
        elastic_ip: typing.Optional[IElasticIp] = None,
        enable_source_dest_check: typing.Optional[builtins.bool] = None,
        interface_type: typing.Optional[InterfaceType] = None,
        ipv4: typing.Optional[AddressingV4] = None,
        ipv6: typing.Optional[AddressingV6] = None,
        removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
        security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
    ) -> None:
        '''Creates a new Example.

        :param scope: - The scope in which to define this construct.
        :param id: - The scoped construct ID.
        :param subnet: The subnet where this Network Interface will be created.
        :param vpc: The VPC where this Network Interface will be created.
        :param description: A description for this Network Interface.
        :param elastic_ip: An Elastic IP Address to associate with this Network Interface. Provding an Elastic IP
        :param enable_source_dest_check: Enable the source/destination check. Default: - true
        :param interface_type: The type of interface (i.e. interface, efa, trunk). Default: - InterfaceType.INTERFACE
        :param ipv4: How to assign IPv4 addresses. The default behavior depends on the VPC. If it's a dual stack VPC, EC2 will allocate a single private IP address from the VPC IPv4 CIDR range. If it's IPv6-only, EC2 won't allocate an IPv4 address. Default: - Dependent on VPC settings
        :param ipv6: How to assign IPv6 addresses. The default behavior depends on the VPC. If there are no IPv6 CIDRs defined for the VPC, EC2 won't allocate an IPv6 address. If it's a dual stack or an IPv6-only VPC, EC2 will allocate an IPv6 address if the subnet auto-assigns one. Default: - Dependent on VPC and subnet settings.
        :param removal_policy: The removal policy for this resource.
        :param security_groups: The security groups to assign to the Network Interface. Default: - A new one is created
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b7881cbf5a93f60fb5d54843bd46460258c8f6351f8714f9e0bf51936cfb33a8)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = NetworkInterfaceProps(
            subnet=subnet,
            vpc=vpc,
            description=description,
            elastic_ip=elastic_ip,
            enable_source_dest_check=enable_source_dest_check,
            interface_type=interface_type,
            ipv4=ipv4,
            ipv6=ipv6,
            removal_policy=removal_policy,
            security_groups=security_groups,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="fromNetworkInterfaceAttributes")
    @builtins.classmethod
    def from_network_interface_attributes(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        network_interface_id: builtins.str,
        security_groups: typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup],
    ) -> INetworkInterface:
        '''Import an existing Network Interface from the given attributes.

        :param scope: - The scope in which to define this construct.
        :param id: - The scoped construct ID.
        :param network_interface_id: The ID of this Network Interface.
        :param security_groups: The security groups assigned to the Network Interface.

        :return: The imported Network Interface
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba90bf577e30a95879b04adea6a10e02d8003e632a56c3750ac72371cd4c3c19)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        attribs = NetworkInterfaceAttributes(
            network_interface_id=network_interface_id, security_groups=security_groups
        )

        return typing.cast(INetworkInterface, jsii.sinvoke(cls, "fromNetworkInterfaceAttributes", [scope, id, attribs]))

    @builtins.property
    @jsii.member(jsii_name="connections")
    def connections(self) -> _aws_cdk_aws_ec2_ceddda9d.Connections:
        '''The network connections associated with this resource.'''
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.Connections, jsii.get(self, "connections"))

    @builtins.property
    @jsii.member(jsii_name="ipv6Address")
    def ipv6_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ipv6Address"))

    @builtins.property
    @jsii.member(jsii_name="networkInterfaceId")
    def network_interface_id(self) -> builtins.str:
        '''The ID of this Network Interface.'''
        return typing.cast(builtins.str, jsii.get(self, "networkInterfaceId"))

    @builtins.property
    @jsii.member(jsii_name="privateIpv4Address")
    def private_ipv4_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "privateIpv4Address"))

    @builtins.property
    @jsii.member(jsii_name="subnet")
    def subnet(self) -> _aws_cdk_aws_ec2_ceddda9d.ISubnet:
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.ISubnet, jsii.get(self, "subnet"))


@jsii.data_type(
    jsii_type="shady-island.networking.NetworkInterfaceAttributes",
    jsii_struct_bases=[],
    name_mapping={
        "network_interface_id": "networkInterfaceId",
        "security_groups": "securityGroups",
    },
)
class NetworkInterfaceAttributes:
    def __init__(
        self,
        *,
        network_interface_id: builtins.str,
        security_groups: typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup],
    ) -> None:
        '''Attributes to import an existing Network Interface.

        :param network_interface_id: The ID of this Network Interface.
        :param security_groups: The security groups assigned to the Network Interface.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__872ccdb97fb0caa6e086ac3826a89fb56cf8c89635737fdeec3c5edba3585c2e)
            check_type(argname="argument network_interface_id", value=network_interface_id, expected_type=type_hints["network_interface_id"])
            check_type(argname="argument security_groups", value=security_groups, expected_type=type_hints["security_groups"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "network_interface_id": network_interface_id,
            "security_groups": security_groups,
        }

    @builtins.property
    def network_interface_id(self) -> builtins.str:
        '''The ID of this Network Interface.'''
        result = self._values.get("network_interface_id")
        assert result is not None, "Required property 'network_interface_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def security_groups(self) -> typing.List[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]:
        '''The security groups assigned to the Network Interface.'''
        result = self._values.get("security_groups")
        assert result is not None, "Required property 'security_groups' is missing"
        return typing.cast(typing.List[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkInterfaceAttributes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="shady-island.networking.NetworkInterfaceProps",
    jsii_struct_bases=[],
    name_mapping={
        "subnet": "subnet",
        "vpc": "vpc",
        "description": "description",
        "elastic_ip": "elasticIp",
        "enable_source_dest_check": "enableSourceDestCheck",
        "interface_type": "interfaceType",
        "ipv4": "ipv4",
        "ipv6": "ipv6",
        "removal_policy": "removalPolicy",
        "security_groups": "securityGroups",
    },
)
class NetworkInterfaceProps:
    def __init__(
        self,
        *,
        subnet: _aws_cdk_aws_ec2_ceddda9d.ISubnet,
        vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
        description: typing.Optional[builtins.str] = None,
        elastic_ip: typing.Optional[IElasticIp] = None,
        enable_source_dest_check: typing.Optional[builtins.bool] = None,
        interface_type: typing.Optional[InterfaceType] = None,
        ipv4: typing.Optional[AddressingV4] = None,
        ipv6: typing.Optional[AddressingV6] = None,
        removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
        security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
    ) -> None:
        '''Constructor properties for NetworkInterface.

        :param subnet: The subnet where this Network Interface will be created.
        :param vpc: The VPC where this Network Interface will be created.
        :param description: A description for this Network Interface.
        :param elastic_ip: An Elastic IP Address to associate with this Network Interface. Provding an Elastic IP
        :param enable_source_dest_check: Enable the source/destination check. Default: - true
        :param interface_type: The type of interface (i.e. interface, efa, trunk). Default: - InterfaceType.INTERFACE
        :param ipv4: How to assign IPv4 addresses. The default behavior depends on the VPC. If it's a dual stack VPC, EC2 will allocate a single private IP address from the VPC IPv4 CIDR range. If it's IPv6-only, EC2 won't allocate an IPv4 address. Default: - Dependent on VPC settings
        :param ipv6: How to assign IPv6 addresses. The default behavior depends on the VPC. If there are no IPv6 CIDRs defined for the VPC, EC2 won't allocate an IPv6 address. If it's a dual stack or an IPv6-only VPC, EC2 will allocate an IPv6 address if the subnet auto-assigns one. Default: - Dependent on VPC and subnet settings.
        :param removal_policy: The removal policy for this resource.
        :param security_groups: The security groups to assign to the Network Interface. Default: - A new one is created
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ad8d033df0b3a5892f2030211876beee3fab00f8b29e23f9591cb251b26d102)
            check_type(argname="argument subnet", value=subnet, expected_type=type_hints["subnet"])
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument elastic_ip", value=elastic_ip, expected_type=type_hints["elastic_ip"])
            check_type(argname="argument enable_source_dest_check", value=enable_source_dest_check, expected_type=type_hints["enable_source_dest_check"])
            check_type(argname="argument interface_type", value=interface_type, expected_type=type_hints["interface_type"])
            check_type(argname="argument ipv4", value=ipv4, expected_type=type_hints["ipv4"])
            check_type(argname="argument ipv6", value=ipv6, expected_type=type_hints["ipv6"])
            check_type(argname="argument removal_policy", value=removal_policy, expected_type=type_hints["removal_policy"])
            check_type(argname="argument security_groups", value=security_groups, expected_type=type_hints["security_groups"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "subnet": subnet,
            "vpc": vpc,
        }
        if description is not None:
            self._values["description"] = description
        if elastic_ip is not None:
            self._values["elastic_ip"] = elastic_ip
        if enable_source_dest_check is not None:
            self._values["enable_source_dest_check"] = enable_source_dest_check
        if interface_type is not None:
            self._values["interface_type"] = interface_type
        if ipv4 is not None:
            self._values["ipv4"] = ipv4
        if ipv6 is not None:
            self._values["ipv6"] = ipv6
        if removal_policy is not None:
            self._values["removal_policy"] = removal_policy
        if security_groups is not None:
            self._values["security_groups"] = security_groups

    @builtins.property
    def subnet(self) -> _aws_cdk_aws_ec2_ceddda9d.ISubnet:
        '''The subnet where this Network Interface will be created.'''
        result = self._values.get("subnet")
        assert result is not None, "Required property 'subnet' is missing"
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.ISubnet, result)

    @builtins.property
    def vpc(self) -> _aws_cdk_aws_ec2_ceddda9d.IVpc:
        '''The VPC where this Network Interface will be created.'''
        result = self._values.get("vpc")
        assert result is not None, "Required property 'vpc' is missing"
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.IVpc, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description for this Network Interface.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def elastic_ip(self) -> typing.Optional[IElasticIp]:
        '''An Elastic IP Address to associate with this Network Interface.

        Provding an Elastic IP
        '''
        result = self._values.get("elastic_ip")
        return typing.cast(typing.Optional[IElasticIp], result)

    @builtins.property
    def enable_source_dest_check(self) -> typing.Optional[builtins.bool]:
        '''Enable the source/destination check.

        :default: - true
        '''
        result = self._values.get("enable_source_dest_check")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def interface_type(self) -> typing.Optional[InterfaceType]:
        '''The type of interface (i.e. interface, efa, trunk).

        :default: - InterfaceType.INTERFACE
        '''
        result = self._values.get("interface_type")
        return typing.cast(typing.Optional[InterfaceType], result)

    @builtins.property
    def ipv4(self) -> typing.Optional[AddressingV4]:
        '''How to assign IPv4 addresses.

        The default behavior depends on the VPC. If it's a dual stack VPC, EC2 will
        allocate a single private IP address from the VPC IPv4 CIDR range. If it's
        IPv6-only, EC2 won't allocate an IPv4 address.

        :default: - Dependent on VPC settings
        '''
        result = self._values.get("ipv4")
        return typing.cast(typing.Optional[AddressingV4], result)

    @builtins.property
    def ipv6(self) -> typing.Optional[AddressingV6]:
        '''How to assign IPv6 addresses.

        The default behavior depends on the VPC. If there are no IPv6 CIDRs defined
        for the VPC, EC2 won't allocate an IPv6 address. If it's a dual stack or an
        IPv6-only VPC, EC2 will allocate an IPv6 address if the subnet auto-assigns
        one.

        :default: - Dependent on VPC and subnet settings.
        '''
        result = self._values.get("ipv6")
        return typing.cast(typing.Optional[AddressingV6], result)

    @builtins.property
    def removal_policy(self) -> typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy]:
        '''The removal policy for this resource.'''
        result = self._values.get("removal_policy")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy], result)

    @builtins.property
    def security_groups(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]]:
        '''The security groups to assign to the Network Interface.

        :default: - A new one is created
        '''
        result = self._values.get("security_groups")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkInterfaceProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(ISecretHttpHeader)
class SecretHttpHeader(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="shady-island.networking.SecretHttpHeader",
):
    '''Configure a secret header an ALB can require for every request.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        header_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Creates a new SecretHttpHeader.

        :param scope: - The parent scope.
        :param id: - The construct identifier.
        :param header_name: The name of the secret HTTP header. Default: - X-Secret-Passphrase
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__150cf8e22f1e7d05a47117e8f77da25561199d5daa7118eb196893fa55cfd796)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = SecretHttpHeaderProps(header_name=header_name)

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="fromSecret")
    @builtins.classmethod
    def from_secret(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        secret: _aws_cdk_aws_secretsmanager_ceddda9d.ISecret,
    ) -> ISecretHttpHeader:
        '''Create a SecretHttpHeader from an existing Secrets Manager secret.

        The secret must be in JSON format and have two fields: ``name`` and ``value``.

        :param scope: - The parent scope.
        :param id: - The ID for the new construct.
        :param secret: - The existing Secrets Manager secret.

        :return: The new ISecretHttpHeader
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__40fccea94b7e684de60e1f55e353e1a03b85c56db9135f4d67a939d5448d4694)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument secret", value=secret, expected_type=type_hints["secret"])
        return typing.cast(ISecretHttpHeader, jsii.sinvoke(cls, "fromSecret", [scope, id, secret]))

    @jsii.member(jsii_name="createListenerCondition")
    def create_listener_condition(
        self,
    ) -> _aws_cdk_aws_elasticloadbalancingv2_ceddda9d.ListenerCondition:
        return typing.cast(_aws_cdk_aws_elasticloadbalancingv2_ceddda9d.ListenerCondition, jsii.invoke(self, "createListenerCondition", []))

    @jsii.member(jsii_name="createOriginCustomHeaders")
    def create_origin_custom_headers(
        self,
    ) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.invoke(self, "createOriginCustomHeaders", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="defaultHeaderName")
    def default_header_name(cls) -> builtins.str:
        '''Gets the default header name.

        :return: the default header name
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "defaultHeaderName"))

    @builtins.property
    @jsii.member(jsii_name="headerName")
    def header_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "headerName"))

    @builtins.property
    @jsii.member(jsii_name="headerValue")
    def header_value(self) -> _aws_cdk_ceddda9d.SecretValue:
        return typing.cast(_aws_cdk_ceddda9d.SecretValue, jsii.get(self, "headerValue"))

    @builtins.property
    @jsii.member(jsii_name="secret")
    def secret(self) -> _aws_cdk_aws_secretsmanager_ceddda9d.ISecret:
        '''The Secrets Manager secret that contains the name and value of the header.'''
        return typing.cast(_aws_cdk_aws_secretsmanager_ceddda9d.ISecret, jsii.get(self, "secret"))


@jsii.data_type(
    jsii_type="shady-island.networking.SecretHttpHeaderProps",
    jsii_struct_bases=[],
    name_mapping={"header_name": "headerName"},
)
class SecretHttpHeaderProps:
    def __init__(self, *, header_name: typing.Optional[builtins.str] = None) -> None:
        '''Properties for the SecretHttpHeader constructor.

        :param header_name: The name of the secret HTTP header. Default: - X-Secret-Passphrase
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c95f74423d937b8be51b1b147dac2d7c254b40cc4b250c45909e61f91bd46e8)
            check_type(argname="argument header_name", value=header_name, expected_type=type_hints["header_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if header_name is not None:
            self._values["header_name"] = header_name

    @builtins.property
    def header_name(self) -> typing.Optional[builtins.str]:
        '''The name of the secret HTTP header.

        :default: - X-Secret-Passphrase
        '''
        result = self._values.get("header_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SecretHttpHeaderProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="shady-island.networking.TargetOptions",
    jsii_struct_bases=[
        _aws_cdk_aws_elasticloadbalancingv2_ceddda9d.ApplicationTargetGroupProps
    ],
    name_mapping={
        "deregistration_delay": "deregistrationDelay",
        "health_check": "healthCheck",
        "target_group_name": "targetGroupName",
        "target_type": "targetType",
        "vpc": "vpc",
        "load_balancing_algorithm_type": "loadBalancingAlgorithmType",
        "port": "port",
        "protocol": "protocol",
        "protocol_version": "protocolVersion",
        "slow_start": "slowStart",
        "stickiness_cookie_duration": "stickinessCookieDuration",
        "stickiness_cookie_name": "stickinessCookieName",
        "targets": "targets",
        "hostnames": "hostnames",
        "priority": "priority",
    },
)
class TargetOptions(
    _aws_cdk_aws_elasticloadbalancingv2_ceddda9d.ApplicationTargetGroupProps,
):
    def __init__(
        self,
        *,
        deregistration_delay: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        health_check: typing.Optional[typing.Union[_aws_cdk_aws_elasticloadbalancingv2_ceddda9d.HealthCheck, typing.Dict[builtins.str, typing.Any]]] = None,
        target_group_name: typing.Optional[builtins.str] = None,
        target_type: typing.Optional[_aws_cdk_aws_elasticloadbalancingv2_ceddda9d.TargetType] = None,
        vpc: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc] = None,
        load_balancing_algorithm_type: typing.Optional[_aws_cdk_aws_elasticloadbalancingv2_ceddda9d.TargetGroupLoadBalancingAlgorithmType] = None,
        port: typing.Optional[jsii.Number] = None,
        protocol: typing.Optional[_aws_cdk_aws_elasticloadbalancingv2_ceddda9d.ApplicationProtocol] = None,
        protocol_version: typing.Optional[_aws_cdk_aws_elasticloadbalancingv2_ceddda9d.ApplicationProtocolVersion] = None,
        slow_start: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        stickiness_cookie_duration: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        stickiness_cookie_name: typing.Optional[builtins.str] = None,
        targets: typing.Optional[typing.Sequence[_aws_cdk_aws_elasticloadbalancingv2_ceddda9d.IApplicationLoadBalancerTarget]] = None,
        hostnames: typing.Optional[typing.Sequence[builtins.str]] = None,
        priority: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''Options for adding a new target group.

        :param deregistration_delay: The amount of time for Elastic Load Balancing to wait before deregistering a target. The range is 0-3600 seconds. Default: 300
        :param health_check: Health check configuration. Default: - The default value for each property in this configuration varies depending on the target.
        :param target_group_name: The name of the target group. This name must be unique per region per account, can have a maximum of 32 characters, must contain only alphanumeric characters or hyphens, and must not begin or end with a hyphen. Default: - Automatically generated.
        :param target_type: The type of targets registered to this TargetGroup, either IP or Instance. All targets registered into the group must be of this type. If you register targets to the TargetGroup in the CDK app, the TargetType is determined automatically. Default: - Determined automatically.
        :param vpc: The virtual private cloud (VPC). only if ``TargetType`` is ``Ip`` or ``InstanceId`` Default: - undefined
        :param load_balancing_algorithm_type: The load balancing algorithm to select targets for routing requests. Default: TargetGroupLoadBalancingAlgorithmType.ROUND_ROBIN
        :param port: The port on which the target receives traffic. This is not applicable for Lambda targets. Default: - Determined from protocol if known
        :param protocol: The protocol used for communication with the target. This is not applicable for Lambda targets. Default: - Determined from port if known
        :param protocol_version: The protocol version to use. Default: ApplicationProtocolVersion.HTTP1
        :param slow_start: The time period during which the load balancer sends a newly registered target a linearly increasing share of the traffic to the target group. The range is 30-900 seconds (15 minutes). Default: 0
        :param stickiness_cookie_duration: The stickiness cookie expiration period. Setting this value enables load balancer stickiness. After this period, the cookie is considered stale. The minimum value is 1 second and the maximum value is 7 days (604800 seconds). Default: Duration.days(1)
        :param stickiness_cookie_name: The name of an application-based stickiness cookie. Names that start with the following prefixes are not allowed: AWSALB, AWSALBAPP, and AWSALBTG; they're reserved for use by the load balancer. Note: ``stickinessCookieName`` parameter depends on the presence of ``stickinessCookieDuration`` parameter. If ``stickinessCookieDuration`` is not set, ``stickinessCookieName`` will be omitted. Default: - If ``stickinessCookieDuration`` is set, a load-balancer generated cookie is used. Otherwise, no stickiness is defined.
        :param targets: The targets to add to this target group. Can be ``Instance``, ``IPAddress``, or any self-registering load balancing target. If you use either ``Instance`` or ``IPAddress`` as targets, all target must be of the same type. Default: - No targets.
        :param hostnames: The hostnames on which traffic is served.
        :param priority: The priority of the listener rule. Default: - Automatically determined
        '''
        if isinstance(health_check, dict):
            health_check = _aws_cdk_aws_elasticloadbalancingv2_ceddda9d.HealthCheck(**health_check)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__efa2d39cd1f01bf3758addd640ec7d1a822d75c3cc97424ddff8b739dca8d900)
            check_type(argname="argument deregistration_delay", value=deregistration_delay, expected_type=type_hints["deregistration_delay"])
            check_type(argname="argument health_check", value=health_check, expected_type=type_hints["health_check"])
            check_type(argname="argument target_group_name", value=target_group_name, expected_type=type_hints["target_group_name"])
            check_type(argname="argument target_type", value=target_type, expected_type=type_hints["target_type"])
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
            check_type(argname="argument load_balancing_algorithm_type", value=load_balancing_algorithm_type, expected_type=type_hints["load_balancing_algorithm_type"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
            check_type(argname="argument protocol", value=protocol, expected_type=type_hints["protocol"])
            check_type(argname="argument protocol_version", value=protocol_version, expected_type=type_hints["protocol_version"])
            check_type(argname="argument slow_start", value=slow_start, expected_type=type_hints["slow_start"])
            check_type(argname="argument stickiness_cookie_duration", value=stickiness_cookie_duration, expected_type=type_hints["stickiness_cookie_duration"])
            check_type(argname="argument stickiness_cookie_name", value=stickiness_cookie_name, expected_type=type_hints["stickiness_cookie_name"])
            check_type(argname="argument targets", value=targets, expected_type=type_hints["targets"])
            check_type(argname="argument hostnames", value=hostnames, expected_type=type_hints["hostnames"])
            check_type(argname="argument priority", value=priority, expected_type=type_hints["priority"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if deregistration_delay is not None:
            self._values["deregistration_delay"] = deregistration_delay
        if health_check is not None:
            self._values["health_check"] = health_check
        if target_group_name is not None:
            self._values["target_group_name"] = target_group_name
        if target_type is not None:
            self._values["target_type"] = target_type
        if vpc is not None:
            self._values["vpc"] = vpc
        if load_balancing_algorithm_type is not None:
            self._values["load_balancing_algorithm_type"] = load_balancing_algorithm_type
        if port is not None:
            self._values["port"] = port
        if protocol is not None:
            self._values["protocol"] = protocol
        if protocol_version is not None:
            self._values["protocol_version"] = protocol_version
        if slow_start is not None:
            self._values["slow_start"] = slow_start
        if stickiness_cookie_duration is not None:
            self._values["stickiness_cookie_duration"] = stickiness_cookie_duration
        if stickiness_cookie_name is not None:
            self._values["stickiness_cookie_name"] = stickiness_cookie_name
        if targets is not None:
            self._values["targets"] = targets
        if hostnames is not None:
            self._values["hostnames"] = hostnames
        if priority is not None:
            self._values["priority"] = priority

    @builtins.property
    def deregistration_delay(self) -> typing.Optional[_aws_cdk_ceddda9d.Duration]:
        '''The amount of time for Elastic Load Balancing to wait before deregistering a target.

        The range is 0-3600 seconds.

        :default: 300
        '''
        result = self._values.get("deregistration_delay")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Duration], result)

    @builtins.property
    def health_check(
        self,
    ) -> typing.Optional[_aws_cdk_aws_elasticloadbalancingv2_ceddda9d.HealthCheck]:
        '''Health check configuration.

        :default: - The default value for each property in this configuration varies depending on the target.

        :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-targetgroup.html#aws-resource-elasticloadbalancingv2-targetgroup-properties
        '''
        result = self._values.get("health_check")
        return typing.cast(typing.Optional[_aws_cdk_aws_elasticloadbalancingv2_ceddda9d.HealthCheck], result)

    @builtins.property
    def target_group_name(self) -> typing.Optional[builtins.str]:
        '''The name of the target group.

        This name must be unique per region per account, can have a maximum of
        32 characters, must contain only alphanumeric characters or hyphens, and
        must not begin or end with a hyphen.

        :default: - Automatically generated.
        '''
        result = self._values.get("target_group_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def target_type(
        self,
    ) -> typing.Optional[_aws_cdk_aws_elasticloadbalancingv2_ceddda9d.TargetType]:
        '''The type of targets registered to this TargetGroup, either IP or Instance.

        All targets registered into the group must be of this type. If you
        register targets to the TargetGroup in the CDK app, the TargetType is
        determined automatically.

        :default: - Determined automatically.
        '''
        result = self._values.get("target_type")
        return typing.cast(typing.Optional[_aws_cdk_aws_elasticloadbalancingv2_ceddda9d.TargetType], result)

    @builtins.property
    def vpc(self) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc]:
        '''The virtual private cloud (VPC).

        only if ``TargetType`` is ``Ip`` or ``InstanceId``

        :default: - undefined
        '''
        result = self._values.get("vpc")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc], result)

    @builtins.property
    def load_balancing_algorithm_type(
        self,
    ) -> typing.Optional[_aws_cdk_aws_elasticloadbalancingv2_ceddda9d.TargetGroupLoadBalancingAlgorithmType]:
        '''The load balancing algorithm to select targets for routing requests.

        :default: TargetGroupLoadBalancingAlgorithmType.ROUND_ROBIN
        '''
        result = self._values.get("load_balancing_algorithm_type")
        return typing.cast(typing.Optional[_aws_cdk_aws_elasticloadbalancingv2_ceddda9d.TargetGroupLoadBalancingAlgorithmType], result)

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        '''The port on which the target receives traffic.

        This is not applicable for Lambda targets.

        :default: - Determined from protocol if known
        '''
        result = self._values.get("port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def protocol(
        self,
    ) -> typing.Optional[_aws_cdk_aws_elasticloadbalancingv2_ceddda9d.ApplicationProtocol]:
        '''The protocol used for communication with the target.

        This is not applicable for Lambda targets.

        :default: - Determined from port if known
        '''
        result = self._values.get("protocol")
        return typing.cast(typing.Optional[_aws_cdk_aws_elasticloadbalancingv2_ceddda9d.ApplicationProtocol], result)

    @builtins.property
    def protocol_version(
        self,
    ) -> typing.Optional[_aws_cdk_aws_elasticloadbalancingv2_ceddda9d.ApplicationProtocolVersion]:
        '''The protocol version to use.

        :default: ApplicationProtocolVersion.HTTP1
        '''
        result = self._values.get("protocol_version")
        return typing.cast(typing.Optional[_aws_cdk_aws_elasticloadbalancingv2_ceddda9d.ApplicationProtocolVersion], result)

    @builtins.property
    def slow_start(self) -> typing.Optional[_aws_cdk_ceddda9d.Duration]:
        '''The time period during which the load balancer sends a newly registered target a linearly increasing share of the traffic to the target group.

        The range is 30-900 seconds (15 minutes).

        :default: 0
        '''
        result = self._values.get("slow_start")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Duration], result)

    @builtins.property
    def stickiness_cookie_duration(self) -> typing.Optional[_aws_cdk_ceddda9d.Duration]:
        '''The stickiness cookie expiration period.

        Setting this value enables load balancer stickiness.

        After this period, the cookie is considered stale. The minimum value is
        1 second and the maximum value is 7 days (604800 seconds).

        :default: Duration.days(1)
        '''
        result = self._values.get("stickiness_cookie_duration")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Duration], result)

    @builtins.property
    def stickiness_cookie_name(self) -> typing.Optional[builtins.str]:
        '''The name of an application-based stickiness cookie.

        Names that start with the following prefixes are not allowed: AWSALB, AWSALBAPP,
        and AWSALBTG; they're reserved for use by the load balancer.

        Note: ``stickinessCookieName`` parameter depends on the presence of ``stickinessCookieDuration`` parameter.
        If ``stickinessCookieDuration`` is not set, ``stickinessCookieName`` will be omitted.

        :default: - If ``stickinessCookieDuration`` is set, a load-balancer generated cookie is used. Otherwise, no stickiness is defined.

        :see: https://docs.aws.amazon.com/elasticloadbalancing/latest/application/sticky-sessions.html
        '''
        result = self._values.get("stickiness_cookie_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def targets(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_elasticloadbalancingv2_ceddda9d.IApplicationLoadBalancerTarget]]:
        '''The targets to add to this target group.

        Can be ``Instance``, ``IPAddress``, or any self-registering load balancing
        target. If you use either ``Instance`` or ``IPAddress`` as targets, all
        target must be of the same type.

        :default: - No targets.
        '''
        result = self._values.get("targets")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_elasticloadbalancingv2_ceddda9d.IApplicationLoadBalancerTarget]], result)

    @builtins.property
    def hostnames(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The hostnames on which traffic is served.'''
        result = self._values.get("hostnames")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def priority(self) -> typing.Optional[jsii.Number]:
        '''The priority of the listener rule.

        :default: - Automatically determined
        '''
        result = self._values.get("priority")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TargetOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class WebLoadBalancing(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="shady-island.networking.WebLoadBalancing",
):
    '''A utility for creating a public-facing Application Load Balancer.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        certificates: typing.Sequence[_aws_cdk_aws_certificatemanager_ceddda9d.ICertificate],
        vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
        idle_timeout: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        ip_address_type: typing.Optional[_aws_cdk_aws_elasticloadbalancingv2_ceddda9d.IpAddressType] = None,
        require_known_hostname: typing.Optional[builtins.bool] = None,
        require_secret_header: typing.Optional[builtins.bool] = None,
        secret_header_name: typing.Optional[builtins.str] = None,
        security_group: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup] = None,
    ) -> None:
        '''Creates a new WebLoadBalancing.

        :param scope: - The scope in which to define this construct.
        :param id: - The scoped construct ID.
        :param certificates: The certificate to attach to the load balancer and CloudFront distribution.
        :param vpc: The VPC where these resources should be deployed.
        :param idle_timeout: The load balancer idle timeout, in seconds. If you have a reverse proxy in front of this load balancer, such as CloudFront, this number should be less than the reverse proxy's request timeout. Default: - 59 seconds
        :param ip_address_type: The type of IP addresses to use (IPv4 or Dual Stack). Default: - IPv4 only
        :param require_known_hostname: Forbid requests that ask for an unknown hostname. Requests for an unknown hostname will receive an HTTP 421 status response. Default: - false
        :param require_secret_header: Forbid requests that are missing an HTTP header with a specific value. If this option is set to ``true``, this construct will provide a new ``SecretHttpHeader`` accessible on the ``secretHeader`` property. Requests without the correct header name and value will receive an HTTP 421 status response. Default: - false
        :param secret_header_name: The name of the secret HTTP header. Providing this option implies that ``requireSecretHeader`` is ``true``. Default: - X-Secret-Passphrase
        :param security_group: A security group for the load balancer itself. Default: - A new security group will be created
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__56342186b82314e198297a3e5364d68b3f8d14f18d4e2c17b5f18a47bffc93d3)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = WebLoadBalancingProps(
            certificates=certificates,
            vpc=vpc,
            idle_timeout=idle_timeout,
            ip_address_type=ip_address_type,
            require_known_hostname=require_known_hostname,
            require_secret_header=require_secret_header,
            secret_header_name=secret_header_name,
            security_group=security_group,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="addTarget")
    def add_target(
        self,
        id: builtins.str,
        target: _aws_cdk_aws_elasticloadbalancingv2_ceddda9d.IApplicationLoadBalancerTarget,
        *,
        hostnames: typing.Optional[typing.Sequence[builtins.str]] = None,
        priority: typing.Optional[jsii.Number] = None,
        load_balancing_algorithm_type: typing.Optional[_aws_cdk_aws_elasticloadbalancingv2_ceddda9d.TargetGroupLoadBalancingAlgorithmType] = None,
        port: typing.Optional[jsii.Number] = None,
        protocol: typing.Optional[_aws_cdk_aws_elasticloadbalancingv2_ceddda9d.ApplicationProtocol] = None,
        protocol_version: typing.Optional[_aws_cdk_aws_elasticloadbalancingv2_ceddda9d.ApplicationProtocolVersion] = None,
        slow_start: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        stickiness_cookie_duration: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        stickiness_cookie_name: typing.Optional[builtins.str] = None,
        targets: typing.Optional[typing.Sequence[_aws_cdk_aws_elasticloadbalancingv2_ceddda9d.IApplicationLoadBalancerTarget]] = None,
        deregistration_delay: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        health_check: typing.Optional[typing.Union[_aws_cdk_aws_elasticloadbalancingv2_ceddda9d.HealthCheck, typing.Dict[builtins.str, typing.Any]]] = None,
        target_group_name: typing.Optional[builtins.str] = None,
        target_type: typing.Optional[_aws_cdk_aws_elasticloadbalancingv2_ceddda9d.TargetType] = None,
        vpc: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc] = None,
    ) -> _aws_cdk_aws_elasticloadbalancingv2_ceddda9d.IApplicationTargetGroup:
        '''Adds a target to the listener.

        If the following options are left undefined, these defaults will be used.

        - ``port``: 443
        - ``protocol``: HTTPS
        - ``deregistrationDelay``: load balancer idle timeout
        - ``healthCheck.path``: /
        - ``healthCheck.healthyThresholdCount``: 2
        - ``healthCheck.interval``: 30 seconds
        - ``healthCheck.timeout``: 29 seconds

        :param id: - The ID of the new target group.
        :param target: - The load balancing target to receive traffic.
        :param hostnames: The hostnames on which traffic is served.
        :param priority: The priority of the listener rule. Default: - Automatically determined
        :param load_balancing_algorithm_type: The load balancing algorithm to select targets for routing requests. Default: TargetGroupLoadBalancingAlgorithmType.ROUND_ROBIN
        :param port: The port on which the target receives traffic. This is not applicable for Lambda targets. Default: - Determined from protocol if known
        :param protocol: The protocol used for communication with the target. This is not applicable for Lambda targets. Default: - Determined from port if known
        :param protocol_version: The protocol version to use. Default: ApplicationProtocolVersion.HTTP1
        :param slow_start: The time period during which the load balancer sends a newly registered target a linearly increasing share of the traffic to the target group. The range is 30-900 seconds (15 minutes). Default: 0
        :param stickiness_cookie_duration: The stickiness cookie expiration period. Setting this value enables load balancer stickiness. After this period, the cookie is considered stale. The minimum value is 1 second and the maximum value is 7 days (604800 seconds). Default: Duration.days(1)
        :param stickiness_cookie_name: The name of an application-based stickiness cookie. Names that start with the following prefixes are not allowed: AWSALB, AWSALBAPP, and AWSALBTG; they're reserved for use by the load balancer. Note: ``stickinessCookieName`` parameter depends on the presence of ``stickinessCookieDuration`` parameter. If ``stickinessCookieDuration`` is not set, ``stickinessCookieName`` will be omitted. Default: - If ``stickinessCookieDuration`` is set, a load-balancer generated cookie is used. Otherwise, no stickiness is defined.
        :param targets: The targets to add to this target group. Can be ``Instance``, ``IPAddress``, or any self-registering load balancing target. If you use either ``Instance`` or ``IPAddress`` as targets, all target must be of the same type. Default: - No targets.
        :param deregistration_delay: The amount of time for Elastic Load Balancing to wait before deregistering a target. The range is 0-3600 seconds. Default: 300
        :param health_check: Health check configuration. Default: - The default value for each property in this configuration varies depending on the target.
        :param target_group_name: The name of the target group. This name must be unique per region per account, can have a maximum of 32 characters, must contain only alphanumeric characters or hyphens, and must not begin or end with a hyphen. Default: - Automatically generated.
        :param target_type: The type of targets registered to this TargetGroup, either IP or Instance. All targets registered into the group must be of this type. If you register targets to the TargetGroup in the CDK app, the TargetType is determined automatically. Default: - Determined automatically.
        :param vpc: The virtual private cloud (VPC). only if ``TargetType`` is ``Ip`` or ``InstanceId`` Default: - undefined

        :return: The new Application Target Group
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d7e0fb1b7097e928299c71e17989f2f1e1385330c18446d1a211d9b57fa16cc8)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument target", value=target, expected_type=type_hints["target"])
        options = TargetOptions(
            hostnames=hostnames,
            priority=priority,
            load_balancing_algorithm_type=load_balancing_algorithm_type,
            port=port,
            protocol=protocol,
            protocol_version=protocol_version,
            slow_start=slow_start,
            stickiness_cookie_duration=stickiness_cookie_duration,
            stickiness_cookie_name=stickiness_cookie_name,
            targets=targets,
            deregistration_delay=deregistration_delay,
            health_check=health_check,
            target_group_name=target_group_name,
            target_type=target_type,
            vpc=vpc,
        )

        return typing.cast(_aws_cdk_aws_elasticloadbalancingv2_ceddda9d.IApplicationTargetGroup, jsii.invoke(self, "addTarget", [id, target, options]))

    @builtins.property
    @jsii.member(jsii_name="listener")
    def listener(
        self,
    ) -> _aws_cdk_aws_elasticloadbalancingv2_ceddda9d.IApplicationListener:
        '''The HTTPS listener.'''
        return typing.cast(_aws_cdk_aws_elasticloadbalancingv2_ceddda9d.IApplicationListener, jsii.get(self, "listener"))

    @builtins.property
    @jsii.member(jsii_name="loadBalancer")
    def load_balancer(
        self,
    ) -> _aws_cdk_aws_elasticloadbalancingv2_ceddda9d.IApplicationLoadBalancer:
        '''The load balancer itself.'''
        return typing.cast(_aws_cdk_aws_elasticloadbalancingv2_ceddda9d.IApplicationLoadBalancer, jsii.get(self, "loadBalancer"))

    @builtins.property
    @jsii.member(jsii_name="secretHeader")
    def secret_header(self) -> typing.Optional[ISecretHttpHeader]:
        '''The secret header (if ``requireSecretHeader`` was set to ``true``).'''
        return typing.cast(typing.Optional[ISecretHttpHeader], jsii.get(self, "secretHeader"))


@jsii.data_type(
    jsii_type="shady-island.networking.WebLoadBalancingProps",
    jsii_struct_bases=[],
    name_mapping={
        "certificates": "certificates",
        "vpc": "vpc",
        "idle_timeout": "idleTimeout",
        "ip_address_type": "ipAddressType",
        "require_known_hostname": "requireKnownHostname",
        "require_secret_header": "requireSecretHeader",
        "secret_header_name": "secretHeaderName",
        "security_group": "securityGroup",
    },
)
class WebLoadBalancingProps:
    def __init__(
        self,
        *,
        certificates: typing.Sequence[_aws_cdk_aws_certificatemanager_ceddda9d.ICertificate],
        vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
        idle_timeout: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        ip_address_type: typing.Optional[_aws_cdk_aws_elasticloadbalancingv2_ceddda9d.IpAddressType] = None,
        require_known_hostname: typing.Optional[builtins.bool] = None,
        require_secret_header: typing.Optional[builtins.bool] = None,
        secret_header_name: typing.Optional[builtins.str] = None,
        security_group: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup] = None,
    ) -> None:
        '''Constructor properties for WebLoadBalancing.

        :param certificates: The certificate to attach to the load balancer and CloudFront distribution.
        :param vpc: The VPC where these resources should be deployed.
        :param idle_timeout: The load balancer idle timeout, in seconds. If you have a reverse proxy in front of this load balancer, such as CloudFront, this number should be less than the reverse proxy's request timeout. Default: - 59 seconds
        :param ip_address_type: The type of IP addresses to use (IPv4 or Dual Stack). Default: - IPv4 only
        :param require_known_hostname: Forbid requests that ask for an unknown hostname. Requests for an unknown hostname will receive an HTTP 421 status response. Default: - false
        :param require_secret_header: Forbid requests that are missing an HTTP header with a specific value. If this option is set to ``true``, this construct will provide a new ``SecretHttpHeader`` accessible on the ``secretHeader`` property. Requests without the correct header name and value will receive an HTTP 421 status response. Default: - false
        :param secret_header_name: The name of the secret HTTP header. Providing this option implies that ``requireSecretHeader`` is ``true``. Default: - X-Secret-Passphrase
        :param security_group: A security group for the load balancer itself. Default: - A new security group will be created
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0cf2c4b4f6d95905cc594637cb1f8523593a0d81a22f8200dc8eec640482dee1)
            check_type(argname="argument certificates", value=certificates, expected_type=type_hints["certificates"])
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
            check_type(argname="argument idle_timeout", value=idle_timeout, expected_type=type_hints["idle_timeout"])
            check_type(argname="argument ip_address_type", value=ip_address_type, expected_type=type_hints["ip_address_type"])
            check_type(argname="argument require_known_hostname", value=require_known_hostname, expected_type=type_hints["require_known_hostname"])
            check_type(argname="argument require_secret_header", value=require_secret_header, expected_type=type_hints["require_secret_header"])
            check_type(argname="argument secret_header_name", value=secret_header_name, expected_type=type_hints["secret_header_name"])
            check_type(argname="argument security_group", value=security_group, expected_type=type_hints["security_group"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "certificates": certificates,
            "vpc": vpc,
        }
        if idle_timeout is not None:
            self._values["idle_timeout"] = idle_timeout
        if ip_address_type is not None:
            self._values["ip_address_type"] = ip_address_type
        if require_known_hostname is not None:
            self._values["require_known_hostname"] = require_known_hostname
        if require_secret_header is not None:
            self._values["require_secret_header"] = require_secret_header
        if secret_header_name is not None:
            self._values["secret_header_name"] = secret_header_name
        if security_group is not None:
            self._values["security_group"] = security_group

    @builtins.property
    def certificates(
        self,
    ) -> typing.List[_aws_cdk_aws_certificatemanager_ceddda9d.ICertificate]:
        '''The certificate to attach to the load balancer and CloudFront distribution.'''
        result = self._values.get("certificates")
        assert result is not None, "Required property 'certificates' is missing"
        return typing.cast(typing.List[_aws_cdk_aws_certificatemanager_ceddda9d.ICertificate], result)

    @builtins.property
    def vpc(self) -> _aws_cdk_aws_ec2_ceddda9d.IVpc:
        '''The VPC where these resources should be deployed.'''
        result = self._values.get("vpc")
        assert result is not None, "Required property 'vpc' is missing"
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.IVpc, result)

    @builtins.property
    def idle_timeout(self) -> typing.Optional[_aws_cdk_ceddda9d.Duration]:
        '''The load balancer idle timeout, in seconds.

        If you have a reverse proxy in front of this load balancer, such as
        CloudFront, this number should be less than the reverse proxy's request
        timeout.

        :default: - 59 seconds
        '''
        result = self._values.get("idle_timeout")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Duration], result)

    @builtins.property
    def ip_address_type(
        self,
    ) -> typing.Optional[_aws_cdk_aws_elasticloadbalancingv2_ceddda9d.IpAddressType]:
        '''The type of IP addresses to use (IPv4 or Dual Stack).

        :default: - IPv4 only
        '''
        result = self._values.get("ip_address_type")
        return typing.cast(typing.Optional[_aws_cdk_aws_elasticloadbalancingv2_ceddda9d.IpAddressType], result)

    @builtins.property
    def require_known_hostname(self) -> typing.Optional[builtins.bool]:
        '''Forbid requests that ask for an unknown hostname.

        Requests for an unknown hostname will receive an HTTP 421 status response.

        :default: - false
        '''
        result = self._values.get("require_known_hostname")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def require_secret_header(self) -> typing.Optional[builtins.bool]:
        '''Forbid requests that are missing an HTTP header with a specific value.

        If this option is set to ``true``, this construct will provide a new
        ``SecretHttpHeader`` accessible on the ``secretHeader`` property.

        Requests without the correct header name and value will receive an HTTP 421
        status response.

        :default: - false
        '''
        result = self._values.get("require_secret_header")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def secret_header_name(self) -> typing.Optional[builtins.str]:
        '''The name of the secret HTTP header.

        Providing this option implies that ``requireSecretHeader`` is ``true``.

        :default: - X-Secret-Passphrase
        '''
        result = self._values.get("secret_header_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def security_group(
        self,
    ) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]:
        '''A security group for the load balancer itself.

        :default: - A new security group will be created
        '''
        result = self._values.get("security_group")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WebLoadBalancingProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(IElasticIp)
class ElasticIp(
    _aws_cdk_ceddda9d.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="shady-island.networking.ElasticIp",
):
    '''An EC2 Elastic IP address.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
    ) -> None:
        '''Creates a new Elastic IP address.

        :param scope: - The scope in which to define this construct.
        :param id: - The scoped construct ID.
        :param removal_policy: The removal policy for this resource.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__329313caf887f63821d7884bee2092f3a6d442a6c1c96f75770081998a95873e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = ElasticIpProps(removal_policy=removal_policy)

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="fromAllocationId")
    @builtins.classmethod
    def from_allocation_id(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        allocation_id: builtins.str,
    ) -> IElasticIp:
        '''Import an existing EIP from the given allocation ID.

        :param scope: - The scope in which to define this construct.
        :param id: - The scoped construct ID.
        :param allocation_id: - The EIP allocation ID.

        :return: The imported Elastic IP
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e82bf067154d978cd348f21fa71899f0687720ef3d7622a28287b58a275f1dd)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument allocation_id", value=allocation_id, expected_type=type_hints["allocation_id"])
        return typing.cast(IElasticIp, jsii.sinvoke(cls, "fromAllocationId", [scope, id, allocation_id]))

    @jsii.member(jsii_name="fromElasticIpArn")
    @builtins.classmethod
    def from_elastic_ip_arn(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        arn: builtins.str,
    ) -> IElasticIp:
        '''Import an existing EIP from its ARN.

        :param scope: - The scope in which to define this construct.
        :param id: - The scoped construct ID.
        :param arn: - The EIP ARN.

        :return: The imported Elastic IP
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__935c29310156a369b6e7213f9c82204a5cb0f35b37e585a9b48489f94e73980c)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument arn", value=arn, expected_type=type_hints["arn"])
        return typing.cast(IElasticIp, jsii.sinvoke(cls, "fromElasticIpArn", [scope, id, arn]))

    @jsii.member(jsii_name="grant")
    def grant(
        self,
        identity: _aws_cdk_aws_iam_ceddda9d.IGrantable,
        *actions: builtins.str,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''Grant the given identity custom permissions.

        e.g. ``ec2:AssociateAddress``, ``ec2:DisableAddressTransfer``,
        ``ec2:DisassociateAddress``, ``ec2:EnableAddressTransfer``, among others.

        :param identity: -
        :param actions: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__610789115b0fd3b9297114da0749e7767d3eeff76e4daa1ede9a061ac66887d0)
            check_type(argname="argument identity", value=identity, expected_type=type_hints["identity"])
            check_type(argname="argument actions", value=actions, expected_type=typing.Tuple[type_hints["actions"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.Grant, jsii.invoke(self, "grant", [identity, *actions]))

    @builtins.property
    @jsii.member(jsii_name="allocationId")
    def allocation_id(self) -> builtins.str:
        '''The allocation ID of the Elastic IP address.'''
        return typing.cast(builtins.str, jsii.get(self, "allocationId"))

    @builtins.property
    @jsii.member(jsii_name="elasticIpArn")
    def elastic_ip_arn(self) -> builtins.str:
        '''The ARN of the Elastic IP address.'''
        return typing.cast(builtins.str, jsii.get(self, "elasticIpArn"))

    @builtins.property
    @jsii.member(jsii_name="publicIp")
    def public_ip(self) -> builtins.str:
        '''The IPv4 address.'''
        return typing.cast(builtins.str, jsii.get(self, "publicIp"))


__all__ = [
    "AddressingV4",
    "AddressingV6",
    "ElasticIp",
    "ElasticIpProps",
    "IElasticIp",
    "INetworkInterface",
    "ISecretHttpHeader",
    "InterfaceType",
    "NetworkInterface",
    "NetworkInterfaceAttributes",
    "NetworkInterfaceProps",
    "SecretHttpHeader",
    "SecretHttpHeaderProps",
    "TargetOptions",
    "WebLoadBalancing",
    "WebLoadBalancingProps",
]

publication.publish()

def _typecheckingstub__b2cddb2547e4ed3f4826e1acff079d40a4ba476ac141e3281f8b106c7455a04f(
    count: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01734a2088506c2015ca7bad849bebf81f4652662c5abd2af6e22d7e89d72a62(
    prefixes: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a558c981ad684205ae14b30ac86b63891341637e8de2255215f0d7fa9890c208(
    ip: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dbd385d7d0a4b0a0306d6f92007994dc4caacd4f45b60696b74868ae7d9af7dc(
    primary: builtins.str,
    count: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__116c136600050bf89a1560721d3862fb3f20a3f55eeb11598bcf8676ad8363f8(
    primary: builtins.str,
    *secondary: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ed7da7903260aeba9877acff158981d9b2220d2610bb60c1601ce4a1cd07c80(
    count: jsii.Number,
    enable_primary: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16d92cdccfc5fcd12837debeb037bdf436f91a88257fd9f12e9dbea4b9846925(
    ips: typing.Sequence[builtins.str],
    enable_primary: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3cd14df44bfcf87b8b5d2f04ad616f4497ecc8908a4f4f91379e46248a6772ee(
    count: jsii.Number,
    enable_primary: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4a8ad5afeb3637eae637f3afd75db4bc00b4274d8a8d486fdf734229f61687f(
    prefixes: typing.Sequence[builtins.str],
    enable_primary: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e06451a98b33ab08a35c0a78b3d4d4c1c765f25e0a9ce8b560db827f5e389a61(
    *,
    removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c038201c2cdaabf12b23bf40d541b0618f6bd20657383b850c9ff3a6d96fdfb(
    identity: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    *actions: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7881cbf5a93f60fb5d54843bd46460258c8f6351f8714f9e0bf51936cfb33a8(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    subnet: _aws_cdk_aws_ec2_ceddda9d.ISubnet,
    vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
    description: typing.Optional[builtins.str] = None,
    elastic_ip: typing.Optional[IElasticIp] = None,
    enable_source_dest_check: typing.Optional[builtins.bool] = None,
    interface_type: typing.Optional[InterfaceType] = None,
    ipv4: typing.Optional[AddressingV4] = None,
    ipv6: typing.Optional[AddressingV6] = None,
    removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
    security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba90bf577e30a95879b04adea6a10e02d8003e632a56c3750ac72371cd4c3c19(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    network_interface_id: builtins.str,
    security_groups: typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__872ccdb97fb0caa6e086ac3826a89fb56cf8c89635737fdeec3c5edba3585c2e(
    *,
    network_interface_id: builtins.str,
    security_groups: typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ad8d033df0b3a5892f2030211876beee3fab00f8b29e23f9591cb251b26d102(
    *,
    subnet: _aws_cdk_aws_ec2_ceddda9d.ISubnet,
    vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
    description: typing.Optional[builtins.str] = None,
    elastic_ip: typing.Optional[IElasticIp] = None,
    enable_source_dest_check: typing.Optional[builtins.bool] = None,
    interface_type: typing.Optional[InterfaceType] = None,
    ipv4: typing.Optional[AddressingV4] = None,
    ipv6: typing.Optional[AddressingV6] = None,
    removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
    security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__150cf8e22f1e7d05a47117e8f77da25561199d5daa7118eb196893fa55cfd796(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    header_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40fccea94b7e684de60e1f55e353e1a03b85c56db9135f4d67a939d5448d4694(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    secret: _aws_cdk_aws_secretsmanager_ceddda9d.ISecret,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c95f74423d937b8be51b1b147dac2d7c254b40cc4b250c45909e61f91bd46e8(
    *,
    header_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__efa2d39cd1f01bf3758addd640ec7d1a822d75c3cc97424ddff8b739dca8d900(
    *,
    deregistration_delay: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    health_check: typing.Optional[typing.Union[_aws_cdk_aws_elasticloadbalancingv2_ceddda9d.HealthCheck, typing.Dict[builtins.str, typing.Any]]] = None,
    target_group_name: typing.Optional[builtins.str] = None,
    target_type: typing.Optional[_aws_cdk_aws_elasticloadbalancingv2_ceddda9d.TargetType] = None,
    vpc: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc] = None,
    load_balancing_algorithm_type: typing.Optional[_aws_cdk_aws_elasticloadbalancingv2_ceddda9d.TargetGroupLoadBalancingAlgorithmType] = None,
    port: typing.Optional[jsii.Number] = None,
    protocol: typing.Optional[_aws_cdk_aws_elasticloadbalancingv2_ceddda9d.ApplicationProtocol] = None,
    protocol_version: typing.Optional[_aws_cdk_aws_elasticloadbalancingv2_ceddda9d.ApplicationProtocolVersion] = None,
    slow_start: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    stickiness_cookie_duration: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    stickiness_cookie_name: typing.Optional[builtins.str] = None,
    targets: typing.Optional[typing.Sequence[_aws_cdk_aws_elasticloadbalancingv2_ceddda9d.IApplicationLoadBalancerTarget]] = None,
    hostnames: typing.Optional[typing.Sequence[builtins.str]] = None,
    priority: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56342186b82314e198297a3e5364d68b3f8d14f18d4e2c17b5f18a47bffc93d3(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    certificates: typing.Sequence[_aws_cdk_aws_certificatemanager_ceddda9d.ICertificate],
    vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
    idle_timeout: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    ip_address_type: typing.Optional[_aws_cdk_aws_elasticloadbalancingv2_ceddda9d.IpAddressType] = None,
    require_known_hostname: typing.Optional[builtins.bool] = None,
    require_secret_header: typing.Optional[builtins.bool] = None,
    secret_header_name: typing.Optional[builtins.str] = None,
    security_group: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7e0fb1b7097e928299c71e17989f2f1e1385330c18446d1a211d9b57fa16cc8(
    id: builtins.str,
    target: _aws_cdk_aws_elasticloadbalancingv2_ceddda9d.IApplicationLoadBalancerTarget,
    *,
    hostnames: typing.Optional[typing.Sequence[builtins.str]] = None,
    priority: typing.Optional[jsii.Number] = None,
    load_balancing_algorithm_type: typing.Optional[_aws_cdk_aws_elasticloadbalancingv2_ceddda9d.TargetGroupLoadBalancingAlgorithmType] = None,
    port: typing.Optional[jsii.Number] = None,
    protocol: typing.Optional[_aws_cdk_aws_elasticloadbalancingv2_ceddda9d.ApplicationProtocol] = None,
    protocol_version: typing.Optional[_aws_cdk_aws_elasticloadbalancingv2_ceddda9d.ApplicationProtocolVersion] = None,
    slow_start: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    stickiness_cookie_duration: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    stickiness_cookie_name: typing.Optional[builtins.str] = None,
    targets: typing.Optional[typing.Sequence[_aws_cdk_aws_elasticloadbalancingv2_ceddda9d.IApplicationLoadBalancerTarget]] = None,
    deregistration_delay: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    health_check: typing.Optional[typing.Union[_aws_cdk_aws_elasticloadbalancingv2_ceddda9d.HealthCheck, typing.Dict[builtins.str, typing.Any]]] = None,
    target_group_name: typing.Optional[builtins.str] = None,
    target_type: typing.Optional[_aws_cdk_aws_elasticloadbalancingv2_ceddda9d.TargetType] = None,
    vpc: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0cf2c4b4f6d95905cc594637cb1f8523593a0d81a22f8200dc8eec640482dee1(
    *,
    certificates: typing.Sequence[_aws_cdk_aws_certificatemanager_ceddda9d.ICertificate],
    vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
    idle_timeout: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    ip_address_type: typing.Optional[_aws_cdk_aws_elasticloadbalancingv2_ceddda9d.IpAddressType] = None,
    require_known_hostname: typing.Optional[builtins.bool] = None,
    require_secret_header: typing.Optional[builtins.bool] = None,
    secret_header_name: typing.Optional[builtins.str] = None,
    security_group: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__329313caf887f63821d7884bee2092f3a6d442a6c1c96f75770081998a95873e(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e82bf067154d978cd348f21fa71899f0687720ef3d7622a28287b58a275f1dd(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    allocation_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__935c29310156a369b6e7213f9c82204a5cb0f35b37e585a9b48489f94e73980c(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__610789115b0fd3b9297114da0749e7767d3eeff76e4daa1ede9a061ac66887d0(
    identity: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    *actions: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

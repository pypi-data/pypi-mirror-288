# flake8: noqa
# pylint: disable=C0301

# Neutron exception definitions are distributed across multiple modules/files
# and projects.
#
# neutron:
# find -name exception\*.py| xargs -l sed -rn 's/^class\s+(\S+)\(.+/    "\1",/p'
#
# neutron-lib:
# sed -rn 's/^class\s+(\S+)\(.+/    "\1",/p' ./neutron_lib/exceptions/*.py
#
# neutron extras
# sed -rn 's/\S+ (\S+)\(RuntimeError\):.*/    "\1",/p' ./neutron/privileged/agent/linux/ip_lib.py
NEUTRON_EXCEPTIONS = [
    # repo:neutron
    "OVSDBPortError",
    "SriovUnsupportedNetworkType",
    "SriovNicError",
    "InvalidDeviceError",
    "InvalidPciSlotError",
    "MechanismDriverError",
    "ExtensionDriverError",
    "ExtensionDriverNotFound",
    "UnknownNetworkType",
    "OVSFWPortNotFound",
    "OVSFWTagNotFound",
    "OVSFWPortNotHandled",
    "OvsdbSslConfigNotFound",
    "OvsdbSslRequiredOptError",
    "RevisionConflict",
    "UnknownResourceType",
    "StandardAttributeIDNotFound",
    "HashRingIsEmpty",
    "InvalidSubnetRequestType",
    "AddressCalculationFailure",
    "InvalidAddressType",
    "IpAddressAlreadyAllocated",
    "InvalidIpForSubnet",
    "InvalidAddressRequest",
    "InvalidSubnetRequest",
    "IPAddressChangeNotAllowed",
    "AllocationOnAutoAddressSubnet",
    "IpAddressGenerationFailure",
    "IpAddressGenerationFailureAllSubnets",
    "IpAddressGenerationFailureNoMatchingSubnet",
    "IPAllocationFailed",
    "IpamValueInvalid",
    "DeferIpam",
    "SegmentNotFound",
    "NoUpdateSubnetWhenMultipleSegmentsOnNetwork",
    "SubnetsNotAllAssociatedWithSegments",
    "SubnetCantAssociateToDynamicSegment",
    "SubnetSegmentAssociationChangeNotAllowed",
    "NetworkIdsDontMatch",
    "HostNotConnectedToAnySegment",
    "HostNotCompatibleWithFixedIps",
    "SegmentInUse",
    "FixedIpsSubnetsNotOnSameSegment",
    "AutoAllocationFailure",
    "DefaultExternalNetworkExists",
    "UnknownProvisioningError",
    "ConntrackHelperNotFound",
    "ConntrackHelperNotAllowed",
    "InvalidProtocolForHelper",
    "RouterGatewayInUseByNDPProxy",
    "RouterInterfaceInUseByNDPProxy",
    "AddressScopeConflict",
    "RouterGatewayNotValid",
    "RouterNDPProxyNotEnable",
    "PortUnreachableRouter",
    "InvalidAddress",
    "RouterIPv6GatewayInUse",
    "NDPProxyNotFound",
    "LogResourceNotFound",
    "InvalidLogResourceType",
    "LoggingTypeNotSupported",
    "TargetResourceNotFound",
    "ResourceNotFound",
    "InvalidResourceConstraint",
    "LogapiDriverException",
    "CookieNotFound",
    "ValidatedMethodNotFound",
    "ResourceIdNotSpecified",
    "RouterNotEnabledSnat",
    "EventsDisabled",
    "RouterGatewayNotSet",
    "PortForwardingNotFound",
    "PortForwardingNotSupportFilterField",
    "PortHasPortForwarding",
    "FipInUseByPortForwarding",
    "PortHasBindingFloatingIP",
    "MechanismDriverNotFound",
    "TrunkBridgeNotFound",
    "ParentPortNotFound",
    "TrunkPortInUse",
    "TrunkNotFound",
    "SubPortNotFound",
    "DuplicateSubPort",
    "ParentPortInUse",
    "SubPortMtuGreaterThanTrunkPortMtu",
    "PortInUseAsTrunkParent",
    "PortInUseAsSubPort",
    "TrunkInUse",
    "TrunkDisabled",
    "TrunkInErrorState",
    "IncompatibleTrunkPluginConfiguration",
    "IncompatibleDriverSegmentationTypes",
    "SegmentationTypeValidatorNotFound",
    "TrunkPluginDriverConflict",
    "SubPortBindingError",
    "CallbackWrongResourceType",
    "CallbackNotFound",
    "CallbacksMaxLimitReached",
    "NoAgentDbMixinImplemented",
    # repo: neutron (extras)
    "NetworkNamespaceNotFound",
    "NetworkInterfaceNotFound",
    "InterfaceOperationNotSupported",
    "InvalidArgument",
    "IpAddressAlreadyExists",
    "InterfaceAlreadyExists",
    # repo:neutron-lib
    "AddressGroupNotFound",
    "AddressGroupInUse",
    "AddressesNotFound",
    "AddressesAlreadyExist",
    "AddressScopeNotFound",
    "AddressScopeInUse",
    "AddressScopeUpdateError",
    "NetworkAddressScopeAffinityError",
    "AgentNotFound",
    "AgentNotFoundByTypeHost",
    "MultipleAgentFoundByTypeHost",
    "AllowedAddressPairsMissingIP",
    "AddressPairAndPortSecurityRequired",
    "DuplicateAddressPairInRequest",
    "AllowedAddressPairExhausted",
    "AvailabilityZoneNotFound",
    "InvalidDHCPAgent",
    "NetworkHostedByDHCPAgent",
    "NetworkNotHostedByDhcpAgent",
    "DNSDomainNotFound",
    "DuplicateRecordSet",
    "ExternalDNSDriverNotFound",
    "InvalidPTRZoneConfiguration",
    "DVRMacAddressNotFound",
    "ExternalNetworkInUse",
    "InvalidRoutes",
    "RouterInterfaceInUseByRoute",
    "RoutesExhausted",
    "FirewallGroupNotFound",
    "FirewallGroupInUse",
    "FirewallGroupInPendingState",
    "FirewallGroupPortInvalid",
    "FirewallGroupPortInvalidProject",
    "FirewallGroupPortInUse",
    "FirewallPolicyNotFound",
    "FirewallPolicyInUse",
    "FirewallPolicyConflict",
    "FirewallRuleSharingConflict",
    "FirewallPolicySharingConflict",
    "FirewallRuleNotFound",
    "FirewallRuleInUse",
    "FirewallRuleNotAssociatedWithPolicy",
    "FirewallRuleInvalidProtocol",
    "FirewallRuleInvalidAction",
    "FirewallRuleInvalidICMPParameter",
    "FirewallRuleWithPortWithoutProtocolInvalid",
    "FirewallRuleInvalidPortValue",
    "FirewallRuleInfoMissing",
    "FirewallIpAddressConflict",
    "FirewallInternalDriverError",
    "FirewallRuleConflict",
    "FirewallRuleAlreadyAssociated",
    "FirewallGroupCannotRemoveDefault",
    "FirewallGroupCannotUpdateDefault",
    "FirewallGroupDefaultAlreadyExists",
    "FlavorNotFound",
    "FlavorInUse",
    "ServiceProfileNotFound",
    "ServiceProfileInUse",
    "FlavorServiceProfileBindingExists",
    "FlavorServiceProfileBindingNotFound",
    "ServiceProfileDriverNotFound",
    "ServiceProfileEmpty",
    "FlavorDisabled",
    "ServiceProfileDisabled",
    "NeutronException",
    "BadRequest",
    "NotFound",
    "Conflict",
    "NotAuthorized",
    "ServiceUnavailable",
    "AdminRequired",
    "ObjectNotFound",
    "NetworkNotFound",
    "SubnetNotFound",
    "PortNotFound",
    "PortNotFoundOnNetwork",
    "DeviceNotFoundError",
    "InUse",
    "NetworkInUse",
    "SubnetInUse",
    "SubnetPoolInUse",
    "PortInUse",
    "ServicePortInUse",
    "PortBound",
    "PortBoundNUMAAffinityPolicy",
    "MacAddressInUse",
    "InvalidIpForNetwork",
    "InvalidIpForSubnet",
    "IpAddressInUse",
    "VlanIdInUse",
    "TunnelIdInUse",
    "ResourceExhausted",
    "NoNetworkAvailable",
    "SubnetMismatchForPort",
    "Invalid",
    "InvalidInput",
    "IpAddressGenerationFailure",
    "PreexistingDeviceFailure",
    "OverQuota",
    "InvalidContentType",
    "ExternalIpAddressExhausted",
    "InvalidConfigurationOption",
    "NetworkTunnelRangeError",
    "PolicyInitError",
    "PolicyCheckError",
    "MultipleExceptions",
    "HostMacAddressGenerationFailure",
    "NetworkMacAddressGenerationFailure",
    "InvalidServiceType",
    "NetworkVlanRangeError",
    "PhysicalNetworkNameError",
    "TenantIdProjectIdFilterConflict",
    "SubnetPoolNotFound",
    "StateInvalid",
    "DhcpPortInUse",
    "HostRoutesExhausted",
    "DNSNameServersExhausted",
    "FlatNetworkInUse",
    "NoNetworkFoundInMaximumAllowedAttempts",
    "MalformedRequestBody",
    "InvalidAllocationPool",
    "UnsupportedPortDeviceOwner",
    "OverlappingAllocationPools",
    "OutOfBoundsAllocationPool",
    "BridgeDoesNotExist",
    "QuotaResourceUnknown",
    "QuotaMissingTenant",
    "InvalidQuotaValue",
    "InvalidSharedSetting",
    "ExtensionsNotFound",
    "GatewayConflictWithAllocationPools",
    "GatewayIpInUse",
    "NetworkVxlanPortRangeError",
    "VxlanNetworkUnsupported",
    "DuplicatedExtension",
    "DriverCallError",
    "DeviceIDNotOwnedByTenant",
    "InvalidCIDR",
    "FailToDropPrivilegesExit",
    "NetworkIdOrRouterIdRequiredError",
    "EmptySubnetPoolPrefixList",
    "PrefixVersionMismatch",
    "UnsupportedMinSubnetPoolPrefix",
    "IllegalSubnetPoolPrefixBounds",
    "IllegalSubnetPoolPrefixUpdate",
    "SubnetAllocationError",
    "AddressScopePrefixConflict",
    "IllegalSubnetPoolAssociationToAddressScope",
    "IllegalSubnetPoolIpVersionAssociationToAddressScope",
    "IllegalSubnetPoolUpdate",
    "MinPrefixSubnetAllocationError",
    "MaxPrefixSubnetAllocationError",
    "SubnetPoolDeleteError",
    "SubnetPoolQuotaExceeded",
    "NetworkSubnetPoolAffinityError",
    "ObjectActionError",
    "CTZoneExhaustedError",
    "TenantQuotaNotFound",
    "MultipleFilterIDForIPFound",
    "FilterIDForIPNotFound",
    "FailedToAddQdiscToDevice",
    "PortBindingNotFound",
    "PortBindingAlreadyActive",
    "PortBindingAlreadyExists",
    "PortBindingError",
    "ProcessExecutionError",
    "InvalidSubnetServiceType",
    "InvalidInputSubnetServiceType",
    "MaxVRIDAllocationTriesReached",
    "NoVRIDAvailable",
    "HANetworkConcurrentDeletion",
    "HANetworkCIDRNotValid",
    "HAMaximumAgentsNumberNotValid",
    "RouterNotFound",
    "RouterInUse",
    "RouterInterfaceNotFound",
    "RouterInterfaceNotFoundForSubnet",
    "RouterInterfaceInUseByFloatingIP",
    "FloatingIPNotFound",
    "ExternalGatewayForFloatingIPNotFound",
    "FloatingIPPortAlreadyAssociated",
    "RouterExternalGatewayInUseByFloatingIp",
    "RouterInterfaceAttachmentConflict",
    "RouterNotCompatibleWithAgent",
    "RouterNotFoundInRouterFactory",
    "FloatingIpSetupException",
    "AbortSyncRouters",
    "IpTablesApplyException",
    "MeteringLabelNotFound",
    "DuplicateMeteringRuleInPost",
    "MeteringLabelRuleNotFound",
    "MeteringLabelRuleOverlaps",
    "SegmentsSetInConjunctionWithProviders",
    "SegmentsContainDuplicateEntry",
    "NetworkSegmentRangeNetTypeNotSupported",
    "NetworkSegmentRangeNotFound",
    "NetworkSegmentRangeReferencedByProject",
    "NetworkSegmentRangeDefaultReadOnly",
    "NetworkSegmentRangeOverlaps",
    "PlacementEndpointNotFound",
    "PlacementResourceNotFound",
    "PlacementResourceProviderNotFound",
    "PlacementResourceProviderGenerationConflict",
    "PlacementInventoryNotFound",
    "PlacementInventoryUpdateConflict",
    "PlacementAggregateNotFound",
    "PlacementTraitNotFound",
    "PlacementResourceClassNotFound",
    "PlacementAPIVersionIncorrect",
    "PlacementResourceProviderNameNotUnique",
    "PlacementClientError",
    "UnknownResourceProvider",
    "AmbiguousResponsibilityForResourceProvider",
    "PlacementAllocationGenerationConflict",
    "PlacementAllocationRemoved",
    "PlacementAllocationRpNotExists",
    "PortSecurityPortHasSecurityGroup",
    "PortSecurityAndIPRequiredForSecurityGroups",
    "QosPolicyNotFound",
    "QosRuleNotFound",
    "QoSPolicyDefaultAlreadyExists",
    "PortQosBindingNotFound",
    "PortQosBindingError",
    "NetworkQosBindingNotFound",
    "FloatingIPQosBindingNotFound",
    "QosPolicyInUse",
    "FloatingIPQosBindingError",
    "NetworkQosBindingError",
    "QosRuleNotSupported",
    "QoSRuleParameterConflict",
    "QoSRulesConflict",
    "PolicyRemoveAuthorizationError",
    "TcLibQdiscTypeError",
    "TcLibQdiscNeededArguments",
    "RouterQosBindingNotFound",
    "RouterQosBindingError",
    "QosPlacementAllocationConflict",
    "VlanTransparencyDriverError",
    "VPNServiceNotFound",
    "IPsecSiteConnectionNotFound",
    "IPsecSiteConnectionDpdIntervalValueError",
    "IPsecSiteConnectionMtuError",
    "IPsecSiteConnectionPeerCidrError",
    "IKEPolicyNotFound",
    "IPsecPolicyNotFound",
    "IKEPolicyInUse",
    "VPNServiceInUse",
    "SubnetInUseByVPNService",
    "SubnetInUseByEndpointGroup",
    "SubnetInUseByIPsecSiteConnection",
    "VPNStateInvalidToUpdate",
    "IPsecPolicyInUse",
    "DeviceDriverImportError",
    "SubnetIsNotConnectedToRouter",
    "RouterIsNotExternal",
    "VPNPeerAddressNotResolved",
    "ExternalNetworkHasNoSubnet",
    "VPNEndpointGroupNotFound",
    "InvalidEndpointInEndpointGroup",
    "MissingEndpointForEndpointGroup",
    "NonExistingSubnetInEndpointGroup",
    "MixedIPVersionsForIPSecEndpoints",
    "MixedIPVersionsForPeerCidrs",
    "MixedIPVersionsForIPSecConnection",
    "InvalidEndpointGroup",
    "WrongEndpointGroupType",
    "PeerCidrsInvalid",
    "MissingPeerCidrs",
    "MissingRequiredEndpointGroup",
    "EndpointGroupInUse",
    "FlavorsPluginNotLoaded",
    "NoProviderFoundForFlavor",
    "IpsecValidationFailure",
    "IkeValidationFailure",
    "CsrInternalError",
    "CsrValidationFailure",
]

# sed -rn 's/^class\s+(\S+)\(.+/    "\1",/p' ./neutronclient/common/exceptions.py
_NEUTRONCLIENT_EXCEPTIONS = [
    "NeutronException",
    "NeutronClientException",
    "BadRequest",
    "Unauthorized",
    "Forbidden",
    "NotFound",
    "Conflict",
    "InternalServerError",
    "ServiceUnavailable",
    "NetworkNotFoundClient",
    "PortNotFoundClient",
    "StateInvalidClient",
    "NetworkInUseClient",
    "PortInUseClient",
    "IpAddressInUseClient",
    "IpAddressAlreadyAllocatedClient",
    "InvalidIpForNetworkClient",
    "InvalidIpForSubnetClient",
    "OverQuotaClient",
    "IpAddressGenerationFailureClient",
    "MacAddressInUseClient",
    "HostNotCompatibleWithFixedIpsClient",
    "ExternalIpAddressExhaustedClient",
    "NoAuthURLProvided",
    "EndpointNotFound",
    "EndpointTypeNotFound",
    "AmbiguousEndpoints",
    "RequestURITooLong",
    "ConnectionFailed",
    "SslCertificateValidationError",
    "MalformedResponseBody",
    "InvalidContentType",
    "NeutronCLIError",
    "CommandError",
    "UnsupportedVersion",
    "NeutronClientNoUniqueMatch",
]
NEUTRONCLIENT_EXCEPTIONS = [f"neutronclient.common.exceptions.{exc}"
                            for exc in _NEUTRONCLIENT_EXCEPTIONS]

# Including this as a dep of (at least) Neutron
# sed -rn 's/^class\s+(\S+)\(.+/    "\1",/p' ovsdbapp/exceptions.py
OVSDBAPP_EXCEPTIONS = [
    "OvsdbAppException",
    "TimeoutException",
    "OvsdbConnectionUnavailable",
]

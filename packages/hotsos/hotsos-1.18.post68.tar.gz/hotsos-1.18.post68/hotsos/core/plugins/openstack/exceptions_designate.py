
# sed -rn 's/^class\s+(\S+)\(.+/    "\1",/p' designate/exceptions.py
DESIGNATE_EXCEPTIONS = [
    "DesignateException",
    "Backend",
    "RelationNotLoaded",
    "AdapterNotFound",
    "NSD4SlaveBackendError",
    "NotImplemented",
    "XFRFailure",
    "ConfigurationError",
    "UnknownFailure",
    "CommunicationFailure",
    "KeystoneCommunicationFailure",
    "NeutronCommunicationFailure",
    "NoFiltersConfigured",
    "NoServersConfigured",
    "MultiplePoolsFound",
    "NoPoolTargetsConfigured",
    "OverQuota",
    "QuotaResourceUnknown",
    "InvalidObject",
    "BadAction",
    "BadRequest",
    "EmptyRequestBody",
    "InvalidProject",
    "InvalidUUID",
    "NetworkEndpointNotFound",
    "MarkerNotFound",
    "ValueError",
    "InvalidMarker",
    "InvalidSortDir",
    "InvalidLimit",
    "InvalidSortKey",
    "InvalidJson",
    "InvalidOperation",
    "UnsupportedAccept",
    "UnsupportedContentType",
    "InvalidZoneName",
    "InvalidRecordSetName",
    "InvalidRecordSetLocation",
    "InvaildZoneTransfer",
    "InvalidTTL",
    "ZoneHasSubZone",
    "Forbidden",
    "IllegalChildZone",
    "IllegalParentZone",
    "IncorrectZoneTransferKey",
    "InvalidTokenScope",
    "Duplicate",
    "DuplicateServiceStatus",
    "DuplicateQuota",
    "DuplicateServer",
    "DuplicateTsigKey",
    "DuplicateZone",
    "DuplicateTld",
    "DuplicateRecordSet",
    "DuplicateRecord",
    "DuplicateBlacklist",
    "DuplicatePool",
    "DuplicatePoolAttribute",
    "DuplicatePoolNsRecord",
    "DuplicatePoolNameserver",
    "DuplicatePoolTarget",
    "DuplicatePoolTargetOption",
    "DuplicatePoolTargetMaster",
    "DuplicatePoolAlsoNotify",
    "DuplicateZoneImport",
    "DuplicateZoneExport",
    "MethodNotAllowed",
    "DuplicateZoneTransferRequest",
    "DuplicateZoneTransferAccept",
    "DuplicateZoneAttribute",
    "DuplicateZoneMaster",
    "NotFound",
    "ServiceStatusNotFound",
    "QuotaNotFound",
    "ServerNotFound",
    "TsigKeyNotFound",
    "BlacklistNotFound",
    "ZoneNotFound",
    "ZoneMasterNotFound",
    "ZoneAttributeNotFound",
    "TldNotFound",
    "RecordSetNotFound",
    "RecordNotFound",
    "ReportNotFound",
    "PoolNotFound",
    "NoValidPoolFound",
    "PoolAttributeNotFound",
    "PoolNsRecordNotFound",
    "PoolNameserverNotFound",
    "PoolTargetNotFound",
    "PoolTargetOptionNotFound",
    "PoolTargetMasterNotFound",
    "PoolAlsoNotifyNotFound",
    "ZoneTransferRequestNotFound",
    "ZoneTransferAcceptNotFound",
    "ZoneImportNotFound",
    "ZoneExportNotFound",
    "LastServerDeleteNotAllowed",
    "ResourceNotFound",
    "MissingProjectID",
]

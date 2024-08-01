# sed -rn 's/^class\s+(\S+)\(.+/    "\1",/p' glance_store/exceptions.py
GLANCE_STORE_EXCEPTIONS = [
    "BackendException",
    "UnsupportedBackend",
    "RedirectException",
    "GlanceStoreException",
    "MissingCredentialError",
    "BadAuthStrategy",
    "AuthorizationRedirect",
    "NotFound",
    "UnknownHashingAlgo",
    "UnknownScheme",
    "BadStoreUri",
    "Duplicate",
    "StorageFull",
    "StorageWriteDenied",
    "AuthBadRequest",
    "AuthUrlNotFound",
    "AuthorizationFailure",
    "NotAuthenticated",
    "Forbidden",
    "Invalid",
    "BadStoreConfiguration",
    "DriverLoadFailure",
    "StoreDeleteNotSupported",
    "StoreGetNotSupported",
    "StoreRandomGetNotSupported",
    "StoreAddDisabled",
    "MaxRedirectsExceeded",
    "NoServiceEndpoint",
    "RegionAmbiguity",
    "RemoteServiceUnavailable",
    "HasSnapshot",
    "InUseByStore",
    "HostNotInitialized",
]

# sed -rn 's/^class\s+(\S+)\(.+/    "\1",/p' glance/common/exception.py
GLANCE_EXCEPTIONS = [
    "RedirectException",
    "GlanceException",
    "MissingCredentialError",
    "BadAuthStrategy",
    "NotFound",
    "BadStoreUri",
    "Duplicate",
    "Conflict",
    "StorageQuotaFull",
    "AuthBadRequest",
    "AuthUrlNotFound",
    "AuthorizationFailure",
    "NotAuthenticated",
    "UploadException",
    "Forbidden",
    "ForbiddenPublicImage",
    "ProtectedImageDelete",
    "ProtectedMetadefNamespaceDelete",
    "ProtectedMetadefNamespacePropDelete",
    "ProtectedMetadefObjectDelete",
    "ProtectedMetadefResourceTypeAssociationDelete",
    "ProtectedMetadefResourceTypeSystemDelete",
    "ProtectedMetadefTagDelete",
    "Invalid",
    "InvalidSortKey",
    "InvalidSortDir",
    "InvalidPropertyProtectionConfiguration",
    "InvalidSwiftStoreConfiguration",
    "InvalidFilterOperatorValue",
    "InvalidFilterRangeValue",
    "InvalidOptionValue",
    "ReadonlyProperty",
    "ReservedProperty",
    "AuthorizationRedirect",
    "ClientConnectionError",
    "ClientConfigurationError",
    "MultipleChoices",
    "LimitExceeded",
    "ServiceUnavailable",
    "ServerError",
    "UnexpectedStatus",
    "InvalidContentType",
    "BadRegistryConnectionConfiguration",
    "BadDriverConfiguration",
    "MaxRedirectsExceeded",
    "InvalidRedirect",
    "NoServiceEndpoint",
    "RegionAmbiguity",
    "WorkerCreationFailure",
    "SchemaLoadError",
    "InvalidObject",
    "ImageSizeLimitExceeded",
    "FailedToGetScrubberJobs",
    "ImageMemberLimitExceeded",
    "ImagePropertyLimitExceeded",
    "ImageTagLimitExceeded",
    "ImageLocationLimitExceeded",
    "SIGHUPInterrupt",
    "RPCError",
    "TaskException",
    "BadTaskConfiguration",
    "ImageNotFound",
    "TaskNotFound",
    "InvalidTaskStatus",
    "InvalidTaskType",
    "InvalidTaskStatusTransition",
    "ImportTaskError",
    "TaskAbortedError",
    "DuplicateLocation",
    "InvalidParameterValue",
    "InvalidImageStatusTransition",
    "MetadefDuplicateNamespace",
    "MetadefDuplicateObject",
    "MetadefDuplicateProperty",
    "MetadefDuplicateResourceType",
    "MetadefDuplicateResourceTypeAssociation",
    "MetadefDuplicateTag",
    "MetadefForbidden",
    "MetadefIntegrityError",
    "MetadefNamespaceNotFound",
    "MetadefObjectNotFound",
    "MetadefPropertyNotFound",
    "MetadefResourceTypeNotFound",
    "MetadefResourceTypeAssociationNotFound",
    "MetadefTagNotFound",
    "InvalidDataMigrationScript",
]

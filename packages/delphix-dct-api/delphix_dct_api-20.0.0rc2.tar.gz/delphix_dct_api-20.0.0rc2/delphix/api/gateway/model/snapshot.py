"""
    Delphix DCT API

    Delphix DCT API  # noqa: E501

    The version of the OpenAPI document: 3.15.0
    Contact: support@delphix.com
    Generated by: https://openapi-generator.tech
"""


import re  # noqa: F401
import sys  # noqa: F401

from delphix.api.gateway.model_utils import (  # noqa: F401
    ApiTypeError,
    ModelComposed,
    ModelNormal,
    ModelSimple,
    cached_property,
    change_keys_js_to_python,
    convert_js_args_to_python_args,
    date,
    datetime,
    file_type,
    none_type,
    validate_get_composed_info,
)
from ..model_utils import OpenApiModel
from delphix.api.gateway.exceptions import ApiAttributeError


def lazy_import():
    from delphix.api.gateway.model.tag import Tag
    globals()['Tag'] = Tag


class Snapshot(ModelNormal):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.

    Attributes:
      allowed_values (dict): The key is the tuple path to the attribute
          and the for var_name this is (var_name,). The value is a dict
          with a capitalized key describing the allowed value and an allowed
          value. These dicts store the allowed enum values.
      attribute_map (dict): The key is attribute name
          and the value is json key in definition.
      discriminator_value_class_map (dict): A dict to go from the discriminator
          variable value to the discriminator class name.
      validations (dict): The key is the tuple path to the attribute
          and the for var_name this is (var_name,). The value is a dict
          that stores validations for max_length, min_length, max_items,
          min_items, exclusive_maximum, inclusive_maximum, exclusive_minimum,
          inclusive_minimum, and regex.
      additional_properties_type (tuple): A tuple of classes accepted
          as additional properties values.
    """

    allowed_values = {
        ('consistency',): {
            'CONSISTENT': "CONSISTENT",
            'INCONSISTENT': "INCONSISTENT",
            'CRASH_CONSISTENT': "CRASH_CONSISTENT",
            'PLUGGABLE': "PLUGGABLE",
        },
        ('mssql_backup_software_type',): {
            'AZURE_NATIVE': "AZURE_NATIVE",
            'NATIVE': "NATIVE",
            'LITESPEED': "LITESPEED",
            'REDGATE': "REDGATE",
            'NETBACKUP': "NETBACKUP",
            'COMMVAULT': "COMMVAULT",
        },
        ('mssql_backup_location_type',): {
            'DISK': "DISK",
            'AZURE': "AZURE",
            'BACKUP_SERVER': "BACKUP_SERVER",
        },
    }

    validations = {
    }

    @cached_property
    def additional_properties_type():
        """
        This must be a method because a model may have properties that are
        of type self, this must run after the class is loaded
        """
        lazy_import()
        return (bool, date, datetime, dict, float, int, list, str, none_type,)  # noqa: E501

    _nullable = False

    @cached_property
    def openapi_types():
        """
        This must be a method because a model may have properties that are
        of type self, this must run after the class is loaded

        Returns
            openapi_types (dict): The key is attribute name
                and the value is attribute type.
        """
        lazy_import()
        return {
            'id': (str,),  # noqa: E501
            'engine_id': (str,),  # noqa: E501
            'namespace': (str, none_type,),  # noqa: E501
            'name': (str,),  # noqa: E501
            'namespace_id': (str,),  # noqa: E501
            'namespace_name': (str,),  # noqa: E501
            'is_replica': (bool,),  # noqa: E501
            'consistency': (str,),  # noqa: E501
            'missing_non_logged_data': (bool,),  # noqa: E501
            'dataset_id': (str,),  # noqa: E501
            'creation_time': (datetime,),  # noqa: E501
            'start_timestamp': (datetime,),  # noqa: E501
            'start_location': (str,),  # noqa: E501
            'timestamp': (datetime,),  # noqa: E501
            'location': (str,),  # noqa: E501
            'retention': (int,),  # noqa: E501
            'expiration': (date,),  # noqa: E501
            'retain_forever': (bool,),  # noqa: E501
            'effective_expiration': (date,),  # noqa: E501
            'effective_retain_forever': (bool,),  # noqa: E501
            'timeflow_id': (str,),  # noqa: E501
            'timezone': (str,),  # noqa: E501
            'version': (str, none_type,),  # noqa: E501
            'temporary': (bool,),  # noqa: E501
            'appdata_toolkit': (str,),  # noqa: E501
            'appdata_metadata': (str,),  # noqa: E501
            'ase_db_encryption_key': (str,),  # noqa: E501
            'mssql_internal_version': (int,),  # noqa: E501
            'mssql_backup_set_uuid': (str,),  # noqa: E501
            'mssql_backup_software_type': (str,),  # noqa: E501
            'mssql_backup_location_type': (str,),  # noqa: E501
            'mssql_empty_snapshot': (bool,),  # noqa: E501
            'oracle_from_physical_standby_vdb': (bool,),  # noqa: E501
            'oracle_redo_log_size_in_bytes': (int,),  # noqa: E501
            'tags': ([Tag],),  # noqa: E501
        }

    @cached_property
    def discriminator():
        return None


    attribute_map = {
        'id': 'id',  # noqa: E501
        'engine_id': 'engine_id',  # noqa: E501
        'namespace': 'namespace',  # noqa: E501
        'name': 'name',  # noqa: E501
        'namespace_id': 'namespace_id',  # noqa: E501
        'namespace_name': 'namespace_name',  # noqa: E501
        'is_replica': 'is_replica',  # noqa: E501
        'consistency': 'consistency',  # noqa: E501
        'missing_non_logged_data': 'missing_non_logged_data',  # noqa: E501
        'dataset_id': 'dataset_id',  # noqa: E501
        'creation_time': 'creation_time',  # noqa: E501
        'start_timestamp': 'start_timestamp',  # noqa: E501
        'start_location': 'start_location',  # noqa: E501
        'timestamp': 'timestamp',  # noqa: E501
        'location': 'location',  # noqa: E501
        'retention': 'retention',  # noqa: E501
        'expiration': 'expiration',  # noqa: E501
        'retain_forever': 'retain_forever',  # noqa: E501
        'effective_expiration': 'effective_expiration',  # noqa: E501
        'effective_retain_forever': 'effective_retain_forever',  # noqa: E501
        'timeflow_id': 'timeflow_id',  # noqa: E501
        'timezone': 'timezone',  # noqa: E501
        'version': 'version',  # noqa: E501
        'temporary': 'temporary',  # noqa: E501
        'appdata_toolkit': 'appdata_toolkit',  # noqa: E501
        'appdata_metadata': 'appdata_metadata',  # noqa: E501
        'ase_db_encryption_key': 'ase_db_encryption_key',  # noqa: E501
        'mssql_internal_version': 'mssql_internal_version',  # noqa: E501
        'mssql_backup_set_uuid': 'mssql_backup_set_uuid',  # noqa: E501
        'mssql_backup_software_type': 'mssql_backup_software_type',  # noqa: E501
        'mssql_backup_location_type': 'mssql_backup_location_type',  # noqa: E501
        'mssql_empty_snapshot': 'mssql_empty_snapshot',  # noqa: E501
        'oracle_from_physical_standby_vdb': 'oracle_from_physical_standby_vdb',  # noqa: E501
        'oracle_redo_log_size_in_bytes': 'oracle_redo_log_size_in_bytes',  # noqa: E501
        'tags': 'tags',  # noqa: E501
    }

    read_only_vars = {
    }

    _composed_schemas = {}

    @classmethod
    @convert_js_args_to_python_args
    def _from_openapi_data(cls, *args, **kwargs):  # noqa: E501
        """Snapshot - a model defined in OpenAPI

        Keyword Args:
            _check_type (bool): if True, values for parameters in openapi_types
                                will be type checked and a TypeError will be
                                raised if the wrong type is input.
                                Defaults to True
            _path_to_item (tuple/list): This is a list of keys or values to
                                drill down to the model in received_data
                                when deserializing a response
            _spec_property_naming (bool): True if the variable names in the input data
                                are serialized names, as specified in the OpenAPI document.
                                False if the variable names in the input data
                                are pythonic names, e.g. snake case (default)
            _configuration (Configuration): the instance to use when
                                deserializing a file_type parameter.
                                If passed, type conversion is attempted
                                If omitted no type conversion is done.
            _visited_composed_classes (tuple): This stores a tuple of
                                classes that we have traveled through so that
                                if we see that class again we will not use its
                                discriminator again.
                                When traveling through a discriminator, the
                                composed schema that is
                                is traveled through is added to this set.
                                For example if Animal has a discriminator
                                petType and we pass in "Dog", and the class Dog
                                allOf includes Animal, we move through Animal
                                once using the discriminator, and pick Dog.
                                Then in Dog, we will make an instance of the
                                Animal class but this time we won't travel
                                through its discriminator because we passed in
                                _visited_composed_classes = (Animal,)
            id (str): The Snapshot ID.. [optional]  # noqa: E501
            engine_id (str): The id of the engine the snapshot belongs to.. [optional]  # noqa: E501
            namespace (str, none_type): Alternate namespace for this object, for replicated and restored snapshots.. [optional]  # noqa: E501
            name (str): The snapshot's name.. [optional]  # noqa: E501
            namespace_id (str): The namespace id of this snapshot.. [optional]  # noqa: E501
            namespace_name (str): The namespace name of this snapshot.. [optional]  # noqa: E501
            is_replica (bool): Is this a replicated object.. [optional]  # noqa: E501
            consistency (str): Indicates what type of recovery strategies must be invoked when provisioning from this snapshot.. [optional]  # noqa: E501
            missing_non_logged_data (bool): Indicates if a virtual database provisioned from this snapshot will be missing nologging changes.. [optional]  # noqa: E501
            dataset_id (str): The ID of the Snapshot's dSource or VDB.. [optional]  # noqa: E501
            creation_time (datetime): The time when the snapshot was created.. [optional]  # noqa: E501
            start_timestamp (datetime): The timestamp within the parent TimeFlow at which this snapshot was initiated. \\ No recovery earlier than this point needs to be applied in order to provision a database from \\ this snapshot. If start_timestamp equals timestamp, then no recovery needs to be \\ applied in order to provision a database. . [optional]  # noqa: E501
            start_location (str): The database specific indentifier within the parent TimeFlow at which this snapshot was initiated. \\ No recovery earlier than this point needs to be applied in order to provision a database from \\ this snapshot. If start_location equals location, then no recovery needs to be \\ applied in order to provision a database. . [optional]  # noqa: E501
            timestamp (datetime): The logical time of the data contained in this Snapshot.. [optional]  # noqa: E501
            location (str): Database specific identifier for the data contained in this Snapshot, such as the Log Sequence Number (LSN) for MSsql databases, System Change Number (SCN) for Oracle databases.. [optional]  # noqa: E501
            retention (int): Retention policy, in days. A value of -1 indicates the snapshot should be kept forever. Deprecated in favor of expiration and retain_forever.. [optional]  # noqa: E501
            expiration (date): The expiration date of this snapshot. If this is unset and retain_forever is false, and the snapshot is not included in a Bookmark, the snapshot is subject to the retention policy of its dataset.. [optional]  # noqa: E501
            retain_forever (bool): Indicates that the snapshot is protected from retention, i.e it will be kept forever. If false, see expiration.. [optional]  # noqa: E501
            effective_expiration (date): The effective expiration is that max of the snapshot expiration and the expiration of any Bookmark which includes this snapshot.. [optional]  # noqa: E501
            effective_retain_forever (bool): True if retain_forever is set or a Bookmark retains this snapshot forever.. [optional]  # noqa: E501
            timeflow_id (str): The TimeFlow this snapshot was taken on.. [optional]  # noqa: E501
            timezone (str): Time zone of the source database at the time the snapshot was taken.. [optional]  # noqa: E501
            version (str, none_type): Version of database source repository at the time the snapshot was taken.. [optional]  # noqa: E501
            temporary (bool): Indicates that this snapshot is in a transient state and should not be user visible.. [optional]  # noqa: E501
            appdata_toolkit (str): The toolkit associated with this snapshot.. [optional]  # noqa: E501
            appdata_metadata (str): The JSON payload conforming to the DraftV4 schema based on the type of application data being manipulated.. [optional]  # noqa: E501
            ase_db_encryption_key (str): Database encryption key present for this snapshot.. [optional]  # noqa: E501
            mssql_internal_version (int): Internal version of the source database at the time the snapshot was taken.. [optional]  # noqa: E501
            mssql_backup_set_uuid (str): UUID of the source database backup that was restored for this snapshot.. [optional]  # noqa: E501
            mssql_backup_software_type (str): Backup software used to restore the source database backup for this snapshot. [optional]  # noqa: E501
            mssql_backup_location_type (str): Backup software used to restore the source database backup for this snapshot. [optional]  # noqa: E501
            mssql_empty_snapshot (bool): True if the staging push dSource snapshot is empty.. [optional]  # noqa: E501
            oracle_from_physical_standby_vdb (bool): True if this snapshot was taken of a standby database.. [optional]  # noqa: E501
            oracle_redo_log_size_in_bytes (int): Online redo log size in bytes when this snapshot was taken.. [optional]  # noqa: E501
            tags ([Tag]): [optional]  # noqa: E501
        """

        _check_type = kwargs.pop('_check_type', True)
        _spec_property_naming = kwargs.pop('_spec_property_naming', False)
        _path_to_item = kwargs.pop('_path_to_item', ())
        _configuration = kwargs.pop('_configuration', None)
        _visited_composed_classes = kwargs.pop('_visited_composed_classes', ())

        self = super(OpenApiModel, cls).__new__(cls)

        if args:
            raise ApiTypeError(
                "Invalid positional arguments=%s passed to %s. Remove those invalid positional arguments." % (
                    args,
                    self.__class__.__name__,
                ),
                path_to_item=_path_to_item,
                valid_classes=(self.__class__,),
            )

        self._data_store = {}
        self._check_type = _check_type
        self._spec_property_naming = _spec_property_naming
        self._path_to_item = _path_to_item
        self._configuration = _configuration
        self._visited_composed_classes = _visited_composed_classes + (self.__class__,)

        for var_name, var_value in kwargs.items():
            if var_name not in self.attribute_map and \
                        self._configuration is not None and \
                        self._configuration.discard_unknown_keys and \
                        self.additional_properties_type is None:
                # discard variable.
                continue
            setattr(self, var_name, var_value)
        return self

    required_properties = set([
        '_data_store',
        '_check_type',
        '_spec_property_naming',
        '_path_to_item',
        '_configuration',
        '_visited_composed_classes',
    ])

    @convert_js_args_to_python_args
    def __init__(self, *args, **kwargs):  # noqa: E501
        """Snapshot - a model defined in OpenAPI

        Keyword Args:
            _check_type (bool): if True, values for parameters in openapi_types
                                will be type checked and a TypeError will be
                                raised if the wrong type is input.
                                Defaults to True
            _path_to_item (tuple/list): This is a list of keys or values to
                                drill down to the model in received_data
                                when deserializing a response
            _spec_property_naming (bool): True if the variable names in the input data
                                are serialized names, as specified in the OpenAPI document.
                                False if the variable names in the input data
                                are pythonic names, e.g. snake case (default)
            _configuration (Configuration): the instance to use when
                                deserializing a file_type parameter.
                                If passed, type conversion is attempted
                                If omitted no type conversion is done.
            _visited_composed_classes (tuple): This stores a tuple of
                                classes that we have traveled through so that
                                if we see that class again we will not use its
                                discriminator again.
                                When traveling through a discriminator, the
                                composed schema that is
                                is traveled through is added to this set.
                                For example if Animal has a discriminator
                                petType and we pass in "Dog", and the class Dog
                                allOf includes Animal, we move through Animal
                                once using the discriminator, and pick Dog.
                                Then in Dog, we will make an instance of the
                                Animal class but this time we won't travel
                                through its discriminator because we passed in
                                _visited_composed_classes = (Animal,)
            id (str): The Snapshot ID.. [optional]  # noqa: E501
            engine_id (str): The id of the engine the snapshot belongs to.. [optional]  # noqa: E501
            namespace (str, none_type): Alternate namespace for this object, for replicated and restored snapshots.. [optional]  # noqa: E501
            name (str): The snapshot's name.. [optional]  # noqa: E501
            namespace_id (str): The namespace id of this snapshot.. [optional]  # noqa: E501
            namespace_name (str): The namespace name of this snapshot.. [optional]  # noqa: E501
            is_replica (bool): Is this a replicated object.. [optional]  # noqa: E501
            consistency (str): Indicates what type of recovery strategies must be invoked when provisioning from this snapshot.. [optional]  # noqa: E501
            missing_non_logged_data (bool): Indicates if a virtual database provisioned from this snapshot will be missing nologging changes.. [optional]  # noqa: E501
            dataset_id (str): The ID of the Snapshot's dSource or VDB.. [optional]  # noqa: E501
            creation_time (datetime): The time when the snapshot was created.. [optional]  # noqa: E501
            start_timestamp (datetime): The timestamp within the parent TimeFlow at which this snapshot was initiated. \\ No recovery earlier than this point needs to be applied in order to provision a database from \\ this snapshot. If start_timestamp equals timestamp, then no recovery needs to be \\ applied in order to provision a database. . [optional]  # noqa: E501
            start_location (str): The database specific indentifier within the parent TimeFlow at which this snapshot was initiated. \\ No recovery earlier than this point needs to be applied in order to provision a database from \\ this snapshot. If start_location equals location, then no recovery needs to be \\ applied in order to provision a database. . [optional]  # noqa: E501
            timestamp (datetime): The logical time of the data contained in this Snapshot.. [optional]  # noqa: E501
            location (str): Database specific identifier for the data contained in this Snapshot, such as the Log Sequence Number (LSN) for MSsql databases, System Change Number (SCN) for Oracle databases.. [optional]  # noqa: E501
            retention (int): Retention policy, in days. A value of -1 indicates the snapshot should be kept forever. Deprecated in favor of expiration and retain_forever.. [optional]  # noqa: E501
            expiration (date): The expiration date of this snapshot. If this is unset and retain_forever is false, and the snapshot is not included in a Bookmark, the snapshot is subject to the retention policy of its dataset.. [optional]  # noqa: E501
            retain_forever (bool): Indicates that the snapshot is protected from retention, i.e it will be kept forever. If false, see expiration.. [optional]  # noqa: E501
            effective_expiration (date): The effective expiration is that max of the snapshot expiration and the expiration of any Bookmark which includes this snapshot.. [optional]  # noqa: E501
            effective_retain_forever (bool): True if retain_forever is set or a Bookmark retains this snapshot forever.. [optional]  # noqa: E501
            timeflow_id (str): The TimeFlow this snapshot was taken on.. [optional]  # noqa: E501
            timezone (str): Time zone of the source database at the time the snapshot was taken.. [optional]  # noqa: E501
            version (str, none_type): Version of database source repository at the time the snapshot was taken.. [optional]  # noqa: E501
            temporary (bool): Indicates that this snapshot is in a transient state and should not be user visible.. [optional]  # noqa: E501
            appdata_toolkit (str): The toolkit associated with this snapshot.. [optional]  # noqa: E501
            appdata_metadata (str): The JSON payload conforming to the DraftV4 schema based on the type of application data being manipulated.. [optional]  # noqa: E501
            ase_db_encryption_key (str): Database encryption key present for this snapshot.. [optional]  # noqa: E501
            mssql_internal_version (int): Internal version of the source database at the time the snapshot was taken.. [optional]  # noqa: E501
            mssql_backup_set_uuid (str): UUID of the source database backup that was restored for this snapshot.. [optional]  # noqa: E501
            mssql_backup_software_type (str): Backup software used to restore the source database backup for this snapshot. [optional]  # noqa: E501
            mssql_backup_location_type (str): Backup software used to restore the source database backup for this snapshot. [optional]  # noqa: E501
            mssql_empty_snapshot (bool): True if the staging push dSource snapshot is empty.. [optional]  # noqa: E501
            oracle_from_physical_standby_vdb (bool): True if this snapshot was taken of a standby database.. [optional]  # noqa: E501
            oracle_redo_log_size_in_bytes (int): Online redo log size in bytes when this snapshot was taken.. [optional]  # noqa: E501
            tags ([Tag]): [optional]  # noqa: E501
        """

        _check_type = kwargs.pop('_check_type', True)
        _spec_property_naming = kwargs.pop('_spec_property_naming', False)
        _path_to_item = kwargs.pop('_path_to_item', ())
        _configuration = kwargs.pop('_configuration', None)
        _visited_composed_classes = kwargs.pop('_visited_composed_classes', ())

        if args:
            raise ApiTypeError(
                "Invalid positional arguments=%s passed to %s. Remove those invalid positional arguments." % (
                    args,
                    self.__class__.__name__,
                ),
                path_to_item=_path_to_item,
                valid_classes=(self.__class__,),
            )

        self._data_store = {}
        self._check_type = _check_type
        self._spec_property_naming = _spec_property_naming
        self._path_to_item = _path_to_item
        self._configuration = _configuration
        self._visited_composed_classes = _visited_composed_classes + (self.__class__,)

        for var_name, var_value in kwargs.items():
            if var_name not in self.attribute_map and \
                        self._configuration is not None and \
                        self._configuration.discard_unknown_keys and \
                        self.additional_properties_type is None:
                # discard variable.
                continue
            setattr(self, var_name, var_value)
            if var_name in self.read_only_vars:
                raise ApiAttributeError(f"`{var_name}` is a read-only attribute. Use `from_openapi_data` to instantiate "
                                     f"class with read only attributes.")

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
    from delphix.api.gateway.model.virtualization_schedule import VirtualizationSchedule
    globals()['VirtualizationSchedule'] = VirtualizationSchedule


class VirtualizationPolicy(ModelNormal):
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
        ('policy_type',): {
            'REFRESH_POLICY': "REFRESH_POLICY",
            'SNAPSHOT_POLICY': "SNAPSHOT_POLICY",
            'SYNC_POLICY': "SYNC_POLICY",
            'RETENTION_POLICY': "RETENTION_POLICY",
            'QUOTA_POLICY': "QUOTA_POLICY",
        },
        ('effective_type',): {
            'DIRECT_APPLIED': "DIRECT_APPLIED",
            'INHERITED': "INHERITED",
        },
        ('data_unit',): {
            'DAY': "DAY",
            'WEEK': "WEEK",
            'MONTH': "MONTH",
            'QUARTER': "QUARTER",
            'YEAR': "YEAR",
        },
        ('log_unit',): {
            'DAY': "DAY",
            'WEEK': "WEEK",
            'MONTH': "MONTH",
            'QUARTER': "QUARTER",
            'YEAR': "YEAR",
        },
        ('day_of_week',): {
            'MONDAY': "MONDAY",
            'TUESDAY': "TUESDAY",
            'WEDNESDAY': "WEDNESDAY",
            'THURSDAY': "THURSDAY",
            'FRIDAY': "FRIDAY",
            'SATURDAY': "SATURDAY",
            'SUNDAY': "SUNDAY",
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
            'name': (str,),  # noqa: E501
            'namespace': (str,),  # noqa: E501
            'namespace_id': (str,),  # noqa: E501
            'namespace_name': (str,),  # noqa: E501
            'is_replica': (bool,),  # noqa: E501
            'engine_id': (str,),  # noqa: E501
            'policy_type': (str,),  # noqa: E501
            'timezone_id': (str,),  # noqa: E501
            'default_policy': (bool,),  # noqa: E501
            'effective_type': (str,),  # noqa: E501
            'data_duration': (int,),  # noqa: E501
            'data_unit': (str,),  # noqa: E501
            'log_duration': (int,),  # noqa: E501
            'log_unit': (str,),  # noqa: E501
            'num_of_daily': (int,),  # noqa: E501
            'num_of_weekly': (int,),  # noqa: E501
            'day_of_week': (str,),  # noqa: E501
            'num_of_monthly': (int,),  # noqa: E501
            'day_of_month': (int,),  # noqa: E501
            'num_of_yearly': (int,),  # noqa: E501
            'day_of_year': (str,),  # noqa: E501
            'schedules': ([VirtualizationSchedule],),  # noqa: E501
            'size': (int, none_type,),  # noqa: E501
        }

    @cached_property
    def discriminator():
        return None


    attribute_map = {
        'id': 'id',  # noqa: E501
        'name': 'name',  # noqa: E501
        'namespace': 'namespace',  # noqa: E501
        'namespace_id': 'namespace_id',  # noqa: E501
        'namespace_name': 'namespace_name',  # noqa: E501
        'is_replica': 'is_replica',  # noqa: E501
        'engine_id': 'engine_id',  # noqa: E501
        'policy_type': 'policy_type',  # noqa: E501
        'timezone_id': 'timezone_id',  # noqa: E501
        'default_policy': 'default_policy',  # noqa: E501
        'effective_type': 'effective_type',  # noqa: E501
        'data_duration': 'data_duration',  # noqa: E501
        'data_unit': 'data_unit',  # noqa: E501
        'log_duration': 'log_duration',  # noqa: E501
        'log_unit': 'log_unit',  # noqa: E501
        'num_of_daily': 'num_of_daily',  # noqa: E501
        'num_of_weekly': 'num_of_weekly',  # noqa: E501
        'day_of_week': 'day_of_week',  # noqa: E501
        'num_of_monthly': 'num_of_monthly',  # noqa: E501
        'day_of_month': 'day_of_month',  # noqa: E501
        'num_of_yearly': 'num_of_yearly',  # noqa: E501
        'day_of_year': 'day_of_year',  # noqa: E501
        'schedules': 'schedules',  # noqa: E501
        'size': 'size',  # noqa: E501
    }

    read_only_vars = {
    }

    _composed_schemas = {}

    @classmethod
    @convert_js_args_to_python_args
    def _from_openapi_data(cls, *args, **kwargs):  # noqa: E501
        """VirtualizationPolicy - a model defined in OpenAPI

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
            id (str): [optional]  # noqa: E501
            name (str): [optional]  # noqa: E501
            namespace (str): [optional]  # noqa: E501
            namespace_id (str): The namespace id of this virtualization policy.. [optional]  # noqa: E501
            namespace_name (str): The namespace name of this virtualization policy... [optional]  # noqa: E501
            is_replica (bool): Is this a replicated object.. [optional]  # noqa: E501
            engine_id (str): [optional]  # noqa: E501
            policy_type (str): [optional]  # noqa: E501
            timezone_id (str): [optional]  # noqa: E501
            default_policy (bool): True if this is the default policy created when the system is setup.. [optional]  # noqa: E501
            effective_type (str): Whether this policy has been directly applied or inherited. See the effectivePolicies parameter of the list call for details.. [optional]  # noqa: E501
            data_duration (int): Amount of time to keep source data [Retention Policy].. [optional]  # noqa: E501
            data_unit (str): Time unit for data_duration [Retention Policy].. [optional]  # noqa: E501
            log_duration (int): Amount of time to keep log data [Retention Policy].. [optional]  # noqa: E501
            log_unit (str): Time unit for log_duration [Retention Policy].. [optional]  # noqa: E501
            num_of_daily (int): Number of daily snapshots to keep [Retention Policy].. [optional]  # noqa: E501
            num_of_weekly (int): Number of weekly snapshots to keep [Retention Policy].. [optional]  # noqa: E501
            day_of_week (str): Day of week upon which to enforce weekly snapshot retention [Retention Policy].. [optional]  # noqa: E501
            num_of_monthly (int): Number of monthly snapshots to keep [Retention Policy].. [optional]  # noqa: E501
            day_of_month (int): Day of month upon which to enforce monthly snapshot retention [Retention Policy].. [optional]  # noqa: E501
            num_of_yearly (int): Number of yearly snapshots to keep [Retention Policy].. [optional]  # noqa: E501
            day_of_year (str): Day of year upon which to enforce yearly snapshot retention, expressed a month / day string (e.g., \"Jan 1\") [Retention Policy].. [optional]  # noqa: E501
            schedules ([VirtualizationSchedule]): [optional]  # noqa: E501
            size (int, none_type): Size of the quota, in bytes. (QUOTA_POLICY only).. [optional]  # noqa: E501
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
        """VirtualizationPolicy - a model defined in OpenAPI

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
            id (str): [optional]  # noqa: E501
            name (str): [optional]  # noqa: E501
            namespace (str): [optional]  # noqa: E501
            namespace_id (str): The namespace id of this virtualization policy.. [optional]  # noqa: E501
            namespace_name (str): The namespace name of this virtualization policy... [optional]  # noqa: E501
            is_replica (bool): Is this a replicated object.. [optional]  # noqa: E501
            engine_id (str): [optional]  # noqa: E501
            policy_type (str): [optional]  # noqa: E501
            timezone_id (str): [optional]  # noqa: E501
            default_policy (bool): True if this is the default policy created when the system is setup.. [optional]  # noqa: E501
            effective_type (str): Whether this policy has been directly applied or inherited. See the effectivePolicies parameter of the list call for details.. [optional]  # noqa: E501
            data_duration (int): Amount of time to keep source data [Retention Policy].. [optional]  # noqa: E501
            data_unit (str): Time unit for data_duration [Retention Policy].. [optional]  # noqa: E501
            log_duration (int): Amount of time to keep log data [Retention Policy].. [optional]  # noqa: E501
            log_unit (str): Time unit for log_duration [Retention Policy].. [optional]  # noqa: E501
            num_of_daily (int): Number of daily snapshots to keep [Retention Policy].. [optional]  # noqa: E501
            num_of_weekly (int): Number of weekly snapshots to keep [Retention Policy].. [optional]  # noqa: E501
            day_of_week (str): Day of week upon which to enforce weekly snapshot retention [Retention Policy].. [optional]  # noqa: E501
            num_of_monthly (int): Number of monthly snapshots to keep [Retention Policy].. [optional]  # noqa: E501
            day_of_month (int): Day of month upon which to enforce monthly snapshot retention [Retention Policy].. [optional]  # noqa: E501
            num_of_yearly (int): Number of yearly snapshots to keep [Retention Policy].. [optional]  # noqa: E501
            day_of_year (str): Day of year upon which to enforce yearly snapshot retention, expressed a month / day string (e.g., \"Jan 1\") [Retention Policy].. [optional]  # noqa: E501
            schedules ([VirtualizationSchedule]): [optional]  # noqa: E501
            size (int, none_type): Size of the quota, in bytes. (QUOTA_POLICY only).. [optional]  # noqa: E501
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

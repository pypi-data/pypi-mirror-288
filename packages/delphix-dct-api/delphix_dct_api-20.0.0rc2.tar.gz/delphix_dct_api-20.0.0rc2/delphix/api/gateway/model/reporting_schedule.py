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


class ReportingSchedule(ModelNormal):
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
        ('report_type',): {
            'VIRTUALIZATION_STORAGE_SUMMARY': "VIRTUALIZATION_STORAGE_SUMMARY",
            'ENGINE_PERFORMANCE_ANALYTIC': "ENGINE_PERFORMANCE_ANALYTIC",
            'VDB_INVENTORY_DATA': "VDB_INVENTORY_DATA",
            'DSOURCE_USAGE_DATA': "DSOURCE_USAGE_DATA",
            'DSOURCE_CONSUMPTION_DATA': "DSOURCE_CONSUMPTION_DATA",
            'MASKING_EXECUTION_METRICS': "MASKING_EXECUTION_METRICS",
            'AUDIT_LOGS_SUMMARY': "AUDIT_LOGS_SUMMARY",
            'STORAGE_SAVINGS_SUMMARY': "STORAGE_SAVINGS_SUMMARY",
            'DATA_RISK_SUMMARY': "DATA_RISK_SUMMARY",
        },
        ('file_format',): {
            'CSV': "CSV",
        },
        ('sort_column',): {
            'ENGINE_ID': "engine_id",
            'ENGINE_NAME': "engine_name",
            'ENGINE_HOSTNAME': "engine_hostname",
            'TOTAL_CAPACITY': "total_capacity",
            'FREE_STORAGE': "free_storage",
            'USED_STORAGE': "used_storage",
            'USED_PERCENTAGE': "used_percentage",
            'DSOURCE_COUNT': "dsource_count",
            'VDB_COUNT': "vdb_count",
            'TOTAL_OBJECT_COUNT': "total_object_count",
            'NAME': "name",
            'UNVIRTUALIZED_SPACE': "unvirtualized_space",
            'ACTUAL_SPACE': "actual_space",
            'DEPENDANT_VDBS': "dependant_vdbs",
            'TYPE': "type",
            'VERSION': "version",
            'PARENT_ID': "parent_id",
            'PARENT_NAME': "parent_name",
            'CREATION_DATE': "creation_date",
            'PARENT_TIMEFLOW_LOCATION': "parent_timeflow_location",
            'PARENT_TIMEFLOW_TIMESTAMP': "parent_timeflow_timestamp",
            'PARENT_TIMEFLOW_TIMEZONE': "parent_timeflow_timezone",
            'ENABLED': "enabled",
            'STATUS': "status",
            'CONNECTOR_ID': "connector_id",
            'CONNECTOR_NAME': "connector_name",
            'CONNECTOR_TYPE': "connector_type",
            'LAST_PROFILED_DATE': "last_profiled_date",
            'LAST_MASKED_DATE': "last_masked_date",
            'IS_PROFILED': "is_profiled",
            'IS_SENSITIVE_DATA': "is_sensitive_data",
            'IS_MASKED': "is_masked",
            'IS_AT_RISK': "is_at_risk",
            'DATA_ELEMENTS_TOTAL': "data_elements_total",
            'DATA_ELEMENTS_NOT_SENSITIVE': "data_elements_not_sensitive",
            'DATA_ELEMENTS_SENSITIVE_MASKED': "data_elements_sensitive_masked",
            'DATA_ELEMENTS_SENSITIVE_UNMASKED': "data_elements_sensitive_unmasked",
            'RECORDS_TOTAL': "records_total",
            'RECORDS_NOT_SENSITIVE': "records_not_sensitive",
            'RECORDS_SENSITIVE_MASKED': "records_sensitive_masked",
            'RECORDS_SENSITIVE_UNMASKED': "records_sensitive_unmasked",
            '-ENGINE_ID': "-engine_id",
            '-ENGINE_NAME': "-engine_name",
            '-ENGINE_HOSTNAME': "-engine_hostname",
            '-TOTAL_CAPACITY': "-total_capacity",
            '-FREE_STORAGE': "-free_storage",
            '-USED_STORAGE': "-used_storage",
            '-USED_PERCENTAGE': "-used_percentage",
            '-DSOURCE_COUNT': "-dsource_count",
            '-VDB_COUNT': "-vdb_count",
            '-TOTAL_OBJECT_COUNT': "-total_object_count",
            '-UNVIRTUALIZED_SPACE': "-unvirtualized_space",
            '-ACTUAL_SPACE': "-actual_space",
            '-DEPENDANT_VDBS': "-dependant_vdbs",
            '-NAME': "-name",
            '-TYPE': "-type",
            '-VERSION': "-version",
            '-PARENT_ID': "-parent_id",
            '-PARENT_NAME': "-parent_name",
            '-CREATION_DATE': "-creation_date",
            '-PARENT_TIMEFLOW_LOCATION': "-parent_timeflow_location",
            '-PARENT_TIMEFLOW_TIMESTAMP': "-parent_timeflow_timestamp",
            '-PARENT_TIMEFLOW_TIMEZONE': "-parent_timeflow_timezone",
            '-ENABLED': "-enabled",
            '-STATUS': "-status",
            '-CONNECTOR_ID': "-connector_id",
            '-CONNECTOR_NAME': "-connector_name",
            '-CONNECTOR_TYPE': "-connector_type",
            '-LAST_PROFILED_DATE': "-last_profiled_date",
            '-LAST_MASKED_DATE': "-last_masked_date",
            '-IS_PROFILED': "-is_profiled",
            '-IS_SENSITIVE_DATA': "-is_sensitive_data",
            '-IS_MASKED': "-is_masked",
            '-IS_AT_RISK': "-is_at_risk",
            '-DATA_ELEMENTS_TOTAL': "-data_elements_total",
            '-DATA_ELEMENTS_NOT_SENSITIVE': "-data_elements_not_sensitive",
            '-DATA_ELEMENTS_SENSITIVE_MASKED': "-data_elements_sensitive_masked",
            '-DATA_ELEMENTS_SENSITIVE_UNMASKED': "-data_elements_sensitive_unmasked",
            '-RECORDS_TOTAL': "-records_total",
            '-RECORDS_NOT_SENSITIVE': "-records_not_sensitive",
            '-RECORDS_SENSITIVE_MASKED': "-records_sensitive_masked",
            '-RECORDS_SENSITIVE_UNMASKED': "-records_sensitive_unmasked",
        },
    }

    validations = {
        ('recipients',): {
            'min_items': 1,
        },
        ('row_count',): {
            'inclusive_minimum': 1,
        },
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
            'report_type': (str,),  # noqa: E501
            'cron_expression': (str,),  # noqa: E501
            'message': (str,),  # noqa: E501
            'file_format': (str,),  # noqa: E501
            'enabled': (bool,),  # noqa: E501
            'recipients': ([str],),  # noqa: E501
            'report_id': (int,),  # noqa: E501
            'time_zone': (str,),  # noqa: E501
            'tags': ([Tag],),  # noqa: E501
            'sort_column': (str,),  # noqa: E501
            'row_count': (int,),  # noqa: E501
        }

    @cached_property
    def discriminator():
        return None


    attribute_map = {
        'report_type': 'report_type',  # noqa: E501
        'cron_expression': 'cron_expression',  # noqa: E501
        'message': 'message',  # noqa: E501
        'file_format': 'file_format',  # noqa: E501
        'enabled': 'enabled',  # noqa: E501
        'recipients': 'recipients',  # noqa: E501
        'report_id': 'report_id',  # noqa: E501
        'time_zone': 'time_zone',  # noqa: E501
        'tags': 'tags',  # noqa: E501
        'sort_column': 'sort_column',  # noqa: E501
        'row_count': 'row_count',  # noqa: E501
    }

    read_only_vars = {
        'report_id',  # noqa: E501
    }

    _composed_schemas = {}

    @classmethod
    @convert_js_args_to_python_args
    def _from_openapi_data(cls, report_type, cron_expression, message, recipients, *args, **kwargs):  # noqa: E501
        """ReportingSchedule - a model defined in OpenAPI

        Args:
            report_type (str):
            cron_expression (str): Standard cron expressions are supported e.g. 0 15 10 L * ?  - Schedule at 10:15 AM on the last day of every month, 0 0 2 ? * Mon-Fri - Schedule at 2:00 AM every Monday, Tuesday, Wednesday, Thursday and Friday. For more details kindly refer- \"http://www.quartz-scheduler.org/documentation/\"
            message (str):
            recipients ([str]):

        Keyword Args:
            file_format (str): defaults to "CSV", must be one of ["CSV", ]  # noqa: E501
            enabled (bool): defaults to True  # noqa: E501
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
            report_id (int): [optional]  # noqa: E501
            time_zone (str): Timezones are specified according to the Olson tzinfo database - \"https://en.wikipedia.org/wiki/List_of_tz_database_time_zones\".. [optional]  # noqa: E501
            tags ([Tag]): [optional]  # noqa: E501
            sort_column (str): [optional]  # noqa: E501
            row_count (int): [optional]  # noqa: E501
        """

        file_format = kwargs.get('file_format', "CSV")
        enabled = kwargs.get('enabled', True)
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

        self.report_type = report_type
        self.cron_expression = cron_expression
        self.message = message
        self.file_format = file_format
        self.enabled = enabled
        self.recipients = recipients
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
    def __init__(self, report_type, cron_expression, message, recipients, *args, **kwargs):  # noqa: E501
        """ReportingSchedule - a model defined in OpenAPI

        Args:
            report_type (str):
            cron_expression (str): Standard cron expressions are supported e.g. 0 15 10 L * ?  - Schedule at 10:15 AM on the last day of every month, 0 0 2 ? * Mon-Fri - Schedule at 2:00 AM every Monday, Tuesday, Wednesday, Thursday and Friday. For more details kindly refer- \"http://www.quartz-scheduler.org/documentation/\"
            message (str):
            recipients ([str]):

        Keyword Args:
            file_format (str): defaults to "CSV", must be one of ["CSV", ]  # noqa: E501
            enabled (bool): defaults to True  # noqa: E501
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
            report_id (int): [optional]  # noqa: E501
            time_zone (str): Timezones are specified according to the Olson tzinfo database - \"https://en.wikipedia.org/wiki/List_of_tz_database_time_zones\".. [optional]  # noqa: E501
            tags ([Tag]): [optional]  # noqa: E501
            sort_column (str): [optional]  # noqa: E501
            row_count (int): [optional]  # noqa: E501
        """

        file_format = kwargs.get('file_format', "CSV")
        enabled = kwargs.get('enabled', True)
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

        self.report_type = report_type
        self.cron_expression = cron_expression
        self.message = message
        self.file_format = file_format
        self.enabled = enabled
        self.recipients = recipients
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

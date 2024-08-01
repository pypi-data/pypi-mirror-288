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


class BookmarkCreateParameters(ModelNormal):
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
        ('bookmark_type',): {
            'PUBLIC': "PUBLIC",
            'PRIVATE': "PRIVATE",
        },
    }

    validations = {
        ('name',): {
            'max_length': 256,
            'min_length': 1,
        },
        ('vdb_ids',): {
        },
        ('vdb_group_id',): {
            'max_length': 256,
            'min_length': 1,
        },
        ('snapshot_ids',): {
        },
        ('timeflow_ids',): {
        },
        ('timestamp_in_database_timezone',): {
            'regex': {
                'pattern': r'[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}(.[0-9]{0,3})?',  # noqa: E501
            },
        },
        ('location',): {
            'max_length': 256,
            'min_length': 1,
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
            'name': (str,),  # noqa: E501
            'vdb_ids': ([str],),  # noqa: E501
            'vdb_group_id': (str,),  # noqa: E501
            'snapshot_ids': ([str],),  # noqa: E501
            'timeflow_ids': ([str],),  # noqa: E501
            'timestamp': (datetime,),  # noqa: E501
            'timestamp_in_database_timezone': (str,),  # noqa: E501
            'location': (str,),  # noqa: E501
            'retention': (int,),  # noqa: E501
            'expiration': (date,),  # noqa: E501
            'retain_forever': (bool,),  # noqa: E501
            'tags': ([Tag],),  # noqa: E501
            'bookmark_type': (str,),  # noqa: E501
            'make_current_account_owner': (bool,),  # noqa: E501
            'inherit_parent_vdb_tags': (bool,),  # noqa: E501
            'inherit_parent_tags': (bool,),  # noqa: E501
        }

    @cached_property
    def discriminator():
        return None


    attribute_map = {
        'name': 'name',  # noqa: E501
        'vdb_ids': 'vdb_ids',  # noqa: E501
        'vdb_group_id': 'vdb_group_id',  # noqa: E501
        'snapshot_ids': 'snapshot_ids',  # noqa: E501
        'timeflow_ids': 'timeflow_ids',  # noqa: E501
        'timestamp': 'timestamp',  # noqa: E501
        'timestamp_in_database_timezone': 'timestamp_in_database_timezone',  # noqa: E501
        'location': 'location',  # noqa: E501
        'retention': 'retention',  # noqa: E501
        'expiration': 'expiration',  # noqa: E501
        'retain_forever': 'retain_forever',  # noqa: E501
        'tags': 'tags',  # noqa: E501
        'bookmark_type': 'bookmark_type',  # noqa: E501
        'make_current_account_owner': 'make_current_account_owner',  # noqa: E501
        'inherit_parent_vdb_tags': 'inherit_parent_vdb_tags',  # noqa: E501
        'inherit_parent_tags': 'inherit_parent_tags',  # noqa: E501
    }

    read_only_vars = {
    }

    _composed_schemas = {}

    @classmethod
    @convert_js_args_to_python_args
    def _from_openapi_data(cls, name, *args, **kwargs):  # noqa: E501
        """BookmarkCreateParameters - a model defined in OpenAPI

        Args:
            name (str): The user-defined name of this bookmark.

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
            vdb_ids ([str]): The IDs of the VDBs to create the Bookmark on. This parameter is mutually exclusive with snapshot_ids and timeflow_ids.. [optional]  # noqa: E501
            vdb_group_id (str): The ID of the VDB group to create the Bookmark on. This parameter is mutually exclusive with vdb_ids.. [optional]  # noqa: E501
            snapshot_ids ([str]): The IDs of the snapshots that will be part of the Bookmark. This parameter is mutually exclusive with vdb_ids, timestamp, timestamp_in_database_timezone, location and timeflow_ids. . [optional]  # noqa: E501
            timeflow_ids ([str]): The array of timeflow Id. Only allowed to set when timestamp, timestamp_in_database_timezone or location is provided.. [optional]  # noqa: E501
            timestamp (datetime): The point in time from which to execute the operation. Mutually exclusive with snapshot_ids, timestamp_in_database_timezone and location.. [optional]  # noqa: E501
            timestamp_in_database_timezone (str): The point in time from which to execute the operation, expressed as a date-time in the timezone of the source database. Mutually exclusive with snapshot_ids, timestamp and location.. [optional]  # noqa: E501
            location (str): The location to create bookmark from. Mutually exclusive with snapshot_ids, timestamp, and timestamp_in_database_timezone.. [optional]  # noqa: E501
            retention (int): The retention policy for this bookmark, in days. A value of -1 indicates the bookmark should be kept forever. Deprecated in favor of expiration and retain_forever.. [optional]  # noqa: E501
            expiration (date): The expiration for this bookmark. Mutually exclusive with retention and retain_forever.. [optional]  # noqa: E501
            retain_forever (bool): Indicates that the bookmark should be retained forever.. [optional]  # noqa: E501
            tags ([Tag]): The tags to be created for this Bookmark.. [optional]  # noqa: E501
            bookmark_type (str): Type of the bookmark, either PUBLIC or PRIVATE.. [optional] if omitted the server will use the default value of "PRIVATE"  # noqa: E501
            make_current_account_owner (bool): Whether the account creating this bookmark must be configured as owner of the bookmark.. [optional] if omitted the server will use the default value of True  # noqa: E501
            inherit_parent_vdb_tags (bool): This field has been deprecated in favour of new field 'inherit_parent_tags'.. [optional] if omitted the server will use the default value of False  # noqa: E501
            inherit_parent_tags (bool): Whether this bookmark should inherit tags from the parent dataset.. [optional] if omitted the server will use the default value of False  # noqa: E501
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

        self.name = name
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
    def __init__(self, name, *args, **kwargs):  # noqa: E501
        """BookmarkCreateParameters - a model defined in OpenAPI

        Args:
            name (str): The user-defined name of this bookmark.

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
            vdb_ids ([str]): The IDs of the VDBs to create the Bookmark on. This parameter is mutually exclusive with snapshot_ids and timeflow_ids.. [optional]  # noqa: E501
            vdb_group_id (str): The ID of the VDB group to create the Bookmark on. This parameter is mutually exclusive with vdb_ids.. [optional]  # noqa: E501
            snapshot_ids ([str]): The IDs of the snapshots that will be part of the Bookmark. This parameter is mutually exclusive with vdb_ids, timestamp, timestamp_in_database_timezone, location and timeflow_ids. . [optional]  # noqa: E501
            timeflow_ids ([str]): The array of timeflow Id. Only allowed to set when timestamp, timestamp_in_database_timezone or location is provided.. [optional]  # noqa: E501
            timestamp (datetime): The point in time from which to execute the operation. Mutually exclusive with snapshot_ids, timestamp_in_database_timezone and location.. [optional]  # noqa: E501
            timestamp_in_database_timezone (str): The point in time from which to execute the operation, expressed as a date-time in the timezone of the source database. Mutually exclusive with snapshot_ids, timestamp and location.. [optional]  # noqa: E501
            location (str): The location to create bookmark from. Mutually exclusive with snapshot_ids, timestamp, and timestamp_in_database_timezone.. [optional]  # noqa: E501
            retention (int): The retention policy for this bookmark, in days. A value of -1 indicates the bookmark should be kept forever. Deprecated in favor of expiration and retain_forever.. [optional]  # noqa: E501
            expiration (date): The expiration for this bookmark. Mutually exclusive with retention and retain_forever.. [optional]  # noqa: E501
            retain_forever (bool): Indicates that the bookmark should be retained forever.. [optional]  # noqa: E501
            tags ([Tag]): The tags to be created for this Bookmark.. [optional]  # noqa: E501
            bookmark_type (str): Type of the bookmark, either PUBLIC or PRIVATE.. [optional] if omitted the server will use the default value of "PRIVATE"  # noqa: E501
            make_current_account_owner (bool): Whether the account creating this bookmark must be configured as owner of the bookmark.. [optional] if omitted the server will use the default value of True  # noqa: E501
            inherit_parent_vdb_tags (bool): This field has been deprecated in favour of new field 'inherit_parent_tags'.. [optional] if omitted the server will use the default value of False  # noqa: E501
            inherit_parent_tags (bool): Whether this bookmark should inherit tags from the parent dataset.. [optional] if omitted the server will use the default value of False  # noqa: E501
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

        self.name = name
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

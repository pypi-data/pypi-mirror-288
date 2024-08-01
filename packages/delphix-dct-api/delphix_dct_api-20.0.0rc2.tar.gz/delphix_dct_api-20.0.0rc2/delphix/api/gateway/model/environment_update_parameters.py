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



class EnvironmentUpdateParameters(ModelNormal):
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
    }

    validations = {
        ('name',): {
            'max_length': 256,
            'min_length': 1,
        },
        ('staging_environment',): {
            'max_length': 256,
            'min_length': 1,
        },
        ('cluster_address',): {
            'max_length': 256,
            'min_length': 1,
        },
        ('cluster_home',): {
            'max_length': 256,
            'min_length': 1,
        },
        ('ase_db_username',): {
            'max_length': 256,
            'min_length': 1,
        },
        ('ase_db_password',): {
            'max_length': 256,
            'min_length': 1,
        },
        ('ase_db_vault',): {
            'max_length': 256,
            'min_length': 1,
        },
        ('ase_db_vault_username',): {
            'max_length': 256,
            'min_length': 1,
        },
        ('ase_db_hashicorp_vault_engine',): {
            'max_length': 256,
            'min_length': 1,
        },
        ('ase_db_hashicorp_vault_secret_path',): {
            'max_length': 256,
            'min_length': 1,
        },
        ('ase_db_hashicorp_vault_username_key',): {
            'max_length': 256,
            'min_length': 1,
        },
        ('ase_db_hashicorp_vault_secret_key',): {
            'max_length': 256,
            'min_length': 1,
        },
        ('ase_db_cyberark_vault_query_string',): {
            'max_length': 256,
            'min_length': 1,
        },
        ('ase_db_azure_vault_name',): {
            'max_length': 256,
            'min_length': 1,
        },
        ('ase_db_azure_vault_username_key',): {
            'max_length': 256,
            'min_length': 1,
        },
        ('ase_db_azure_vault_secret_key',): {
            'max_length': 256,
            'min_length': 1,
        },
        ('description',): {
            'max_length': 1024,
            'min_length': 1,
        },
    }

    @cached_property
    def additional_properties_type():
        """
        This must be a method because a model may have properties that are
        of type self, this must run after the class is loaded
        """
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
        return {
            'name': (str,),  # noqa: E501
            'staging_environment': (str,),  # noqa: E501
            'cluster_address': (str,),  # noqa: E501
            'cluster_home': (str,),  # noqa: E501
            'ase_db_username': (str,),  # noqa: E501
            'ase_db_password': (str,),  # noqa: E501
            'ase_db_vault': (str,),  # noqa: E501
            'ase_db_vault_username': (str,),  # noqa: E501
            'ase_db_hashicorp_vault_engine': (str,),  # noqa: E501
            'ase_db_hashicorp_vault_secret_path': (str,),  # noqa: E501
            'ase_db_hashicorp_vault_username_key': (str,),  # noqa: E501
            'ase_db_hashicorp_vault_secret_key': (str,),  # noqa: E501
            'ase_db_cyberark_vault_query_string': (str,),  # noqa: E501
            'ase_db_azure_vault_name': (str,),  # noqa: E501
            'ase_db_azure_vault_username_key': (str,),  # noqa: E501
            'ase_db_azure_vault_secret_key': (str,),  # noqa: E501
            'ase_db_use_kerberos_authentication': (bool,),  # noqa: E501
            'description': (str,),  # noqa: E501
        }

    @cached_property
    def discriminator():
        return None


    attribute_map = {
        'name': 'name',  # noqa: E501
        'staging_environment': 'staging_environment',  # noqa: E501
        'cluster_address': 'cluster_address',  # noqa: E501
        'cluster_home': 'cluster_home',  # noqa: E501
        'ase_db_username': 'ase_db_username',  # noqa: E501
        'ase_db_password': 'ase_db_password',  # noqa: E501
        'ase_db_vault': 'ase_db_vault',  # noqa: E501
        'ase_db_vault_username': 'ase_db_vault_username',  # noqa: E501
        'ase_db_hashicorp_vault_engine': 'ase_db_hashicorp_vault_engine',  # noqa: E501
        'ase_db_hashicorp_vault_secret_path': 'ase_db_hashicorp_vault_secret_path',  # noqa: E501
        'ase_db_hashicorp_vault_username_key': 'ase_db_hashicorp_vault_username_key',  # noqa: E501
        'ase_db_hashicorp_vault_secret_key': 'ase_db_hashicorp_vault_secret_key',  # noqa: E501
        'ase_db_cyberark_vault_query_string': 'ase_db_cyberark_vault_query_string',  # noqa: E501
        'ase_db_azure_vault_name': 'ase_db_azure_vault_name',  # noqa: E501
        'ase_db_azure_vault_username_key': 'ase_db_azure_vault_username_key',  # noqa: E501
        'ase_db_azure_vault_secret_key': 'ase_db_azure_vault_secret_key',  # noqa: E501
        'ase_db_use_kerberos_authentication': 'ase_db_use_kerberos_authentication',  # noqa: E501
        'description': 'description',  # noqa: E501
    }

    read_only_vars = {
    }

    _composed_schemas = {}

    @classmethod
    @convert_js_args_to_python_args
    def _from_openapi_data(cls, *args, **kwargs):  # noqa: E501
        """EnvironmentUpdateParameters - a model defined in OpenAPI

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
            name (str): The name of the environment.. [optional]  # noqa: E501
            staging_environment (str): Id of the connector environment which is used to connect to this source environment.. [optional]  # noqa: E501
            cluster_address (str): Address of the cluster. This property can be modified for Windows cluster only.. [optional]  # noqa: E501
            cluster_home (str): Absolute path to cluster home directory. This parameter is for UNIX cluster environments.. [optional]  # noqa: E501
            ase_db_username (str): username of the SAP ASE database.. [optional]  # noqa: E501
            ase_db_password (str): password of the SAP ASE database.. [optional]  # noqa: E501
            ase_db_vault (str): The name or reference of the vault from which to read the ASE database credentials.. [optional]  # noqa: E501
            ase_db_vault_username (str): Delphix display name for the vault user. [optional]  # noqa: E501
            ase_db_hashicorp_vault_engine (str): Vault engine name where the credential is stored.. [optional]  # noqa: E501
            ase_db_hashicorp_vault_secret_path (str): Path in the vault engine where the credential is stored.. [optional]  # noqa: E501
            ase_db_hashicorp_vault_username_key (str): Key for the username in the key-value store.. [optional]  # noqa: E501
            ase_db_hashicorp_vault_secret_key (str): Key for the password in the key-value store.. [optional]  # noqa: E501
            ase_db_cyberark_vault_query_string (str): Query to find a credential in the CyberArk vault.. [optional]  # noqa: E501
            ase_db_azure_vault_name (str): Azure key vault name.. [optional]  # noqa: E501
            ase_db_azure_vault_username_key (str): Azure vault key for the username in the key-value store.. [optional]  # noqa: E501
            ase_db_azure_vault_secret_key (str): Azure vault key for the password in the key-value store.. [optional]  # noqa: E501
            ase_db_use_kerberos_authentication (bool): Whether to use kerberos authentication for ASE DB discovery.. [optional]  # noqa: E501
            description (str): The environment description.. [optional]  # noqa: E501
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
        """EnvironmentUpdateParameters - a model defined in OpenAPI

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
            name (str): The name of the environment.. [optional]  # noqa: E501
            staging_environment (str): Id of the connector environment which is used to connect to this source environment.. [optional]  # noqa: E501
            cluster_address (str): Address of the cluster. This property can be modified for Windows cluster only.. [optional]  # noqa: E501
            cluster_home (str): Absolute path to cluster home directory. This parameter is for UNIX cluster environments.. [optional]  # noqa: E501
            ase_db_username (str): username of the SAP ASE database.. [optional]  # noqa: E501
            ase_db_password (str): password of the SAP ASE database.. [optional]  # noqa: E501
            ase_db_vault (str): The name or reference of the vault from which to read the ASE database credentials.. [optional]  # noqa: E501
            ase_db_vault_username (str): Delphix display name for the vault user. [optional]  # noqa: E501
            ase_db_hashicorp_vault_engine (str): Vault engine name where the credential is stored.. [optional]  # noqa: E501
            ase_db_hashicorp_vault_secret_path (str): Path in the vault engine where the credential is stored.. [optional]  # noqa: E501
            ase_db_hashicorp_vault_username_key (str): Key for the username in the key-value store.. [optional]  # noqa: E501
            ase_db_hashicorp_vault_secret_key (str): Key for the password in the key-value store.. [optional]  # noqa: E501
            ase_db_cyberark_vault_query_string (str): Query to find a credential in the CyberArk vault.. [optional]  # noqa: E501
            ase_db_azure_vault_name (str): Azure key vault name.. [optional]  # noqa: E501
            ase_db_azure_vault_username_key (str): Azure vault key for the username in the key-value store.. [optional]  # noqa: E501
            ase_db_azure_vault_secret_key (str): Azure vault key for the password in the key-value store.. [optional]  # noqa: E501
            ase_db_use_kerberos_authentication (bool): Whether to use kerberos authentication for ASE DB discovery.. [optional]  # noqa: E501
            description (str): The environment description.. [optional]  # noqa: E501
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

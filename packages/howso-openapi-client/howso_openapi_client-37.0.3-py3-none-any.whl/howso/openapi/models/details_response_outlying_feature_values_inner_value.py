# coding: utf-8

"""
Howso API

OpenAPI implementation for interacting with the Howso API. 
"""

try:
    from inspect import getfullargspec
except ImportError:
    from inspect import getargspec as getfullargspec
import pprint
import re  # noqa: F401
import six

from howso.openapi.configuration import Configuration


class DetailsResponseOutlyingFeatureValuesInnerValue(object):
    """
    Auto-generated OpenAPI type.

    Feature values from the reaction case that are below the min or above the max value of similar cases that were identified during a prediction. 
    """

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    openapi_types = {
        'input_case_value': 'float',
        'local_max': 'float'
    }

    attribute_map = {
        'input_case_value': 'input_case_value',
        'local_max': 'local_max'
    }

    nullable_attributes = [
    ]

    discriminator = None

    def __init__(self, input_case_value=None, local_max=None, local_vars_configuration=None):  # noqa: E501
        """DetailsResponseOutlyingFeatureValuesInnerValue - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default_copy()
        self.local_vars_configuration = local_vars_configuration

        self._input_case_value = None
        self._local_max = None

        if input_case_value is not None:
            self.input_case_value = input_case_value
        if local_max is not None:
            self.local_max = local_max

    @property
    def input_case_value(self):
        """Get the input_case_value of this DetailsResponseOutlyingFeatureValuesInnerValue.


        :return: The input_case_value of this DetailsResponseOutlyingFeatureValuesInnerValue.
        :rtype: float
        """
        return self._input_case_value

    @input_case_value.setter
    def input_case_value(self, input_case_value):
        """Set the input_case_value of this DetailsResponseOutlyingFeatureValuesInnerValue.


        :param input_case_value: The input_case_value of this DetailsResponseOutlyingFeatureValuesInnerValue.
        :type input_case_value: float
        """

        self._input_case_value = input_case_value

    @property
    def local_max(self):
        """Get the local_max of this DetailsResponseOutlyingFeatureValuesInnerValue.


        :return: The local_max of this DetailsResponseOutlyingFeatureValuesInnerValue.
        :rtype: float
        """
        return self._local_max

    @local_max.setter
    def local_max(self, local_max):
        """Set the local_max of this DetailsResponseOutlyingFeatureValuesInnerValue.


        :param local_max: The local_max of this DetailsResponseOutlyingFeatureValuesInnerValue.
        :type local_max: float
        """

        self._local_max = local_max

    def to_dict(self, serialize=False, exclude_null=False):
        """Returns the model properties as a dict"""
        result = {}

        def convert(x):
            if hasattr(x, "to_dict"):
                args = getfullargspec(x.to_dict).args
                if len(args) == 1:
                    return x.to_dict()
                elif 'exclude_null' in args:
                    return x.to_dict(serialize, exclude_null)
                else:
                    return x.to_dict(serialize)
            else:
                return x

        for attr, _ in six.iteritems(self.openapi_types):
            value = getattr(self, attr)
            attr = self.attribute_map.get(attr, attr) if serialize else attr
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: convert(x),
                    value
                ))
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], convert(item[1])),
                    value.items()
                ))
            elif value is None and (exclude_null or attr not in self.nullable_attributes):
                continue
            else:
                result[attr] = convert(value)

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, DetailsResponseOutlyingFeatureValuesInnerValue):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, DetailsResponseOutlyingFeatureValuesInnerValue):
            return True

        return self.to_dict() != other.to_dict()

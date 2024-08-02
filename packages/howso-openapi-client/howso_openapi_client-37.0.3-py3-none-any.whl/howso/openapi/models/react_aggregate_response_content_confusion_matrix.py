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


class ReactAggregateResponseContentConfusionMatrix(object):
    """
    Auto-generated OpenAPI type.

    """

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    openapi_types = {
        'matrix': 'dict[str, dict[str, float]]',
        'leftover_correct': 'int',
        'leftover_incorrect': 'int',
        'other_counts': 'int'
    }

    attribute_map = {
        'matrix': 'matrix',
        'leftover_correct': 'leftover_correct',
        'leftover_incorrect': 'leftover_incorrect',
        'other_counts': 'other_counts'
    }

    nullable_attributes = [
    ]

    discriminator = None

    def __init__(self, matrix=None, leftover_correct=None, leftover_incorrect=None, other_counts=None, local_vars_configuration=None):  # noqa: E501
        """ReactAggregateResponseContentConfusionMatrix - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default_copy()
        self.local_vars_configuration = local_vars_configuration

        self._matrix = None
        self._leftover_correct = None
        self._leftover_incorrect = None
        self._other_counts = None

        if matrix is not None:
            self.matrix = matrix
        if leftover_correct is not None:
            self.leftover_correct = leftover_correct
        if leftover_incorrect is not None:
            self.leftover_incorrect = leftover_incorrect
        if other_counts is not None:
            self.other_counts = other_counts

    @property
    def matrix(self):
        """Get the matrix of this ReactAggregateResponseContentConfusionMatrix.

        The sparse confusion matrix for the predicted values of an action feature. 

        :return: The matrix of this ReactAggregateResponseContentConfusionMatrix.
        :rtype: dict[str, dict[str, float]]
        """
        return self._matrix

    @matrix.setter
    def matrix(self, matrix):
        """Set the matrix of this ReactAggregateResponseContentConfusionMatrix.

        The sparse confusion matrix for the predicted values of an action feature. 

        :param matrix: The matrix of this ReactAggregateResponseContentConfusionMatrix.
        :type matrix: dict[str, dict[str, float]]
        """

        self._matrix = matrix

    @property
    def leftover_correct(self):
        """Get the leftover_correct of this ReactAggregateResponseContentConfusionMatrix.

        Total count of all correct predictions for classes that did not have a statistically significant amount. 

        :return: The leftover_correct of this ReactAggregateResponseContentConfusionMatrix.
        :rtype: int
        """
        return self._leftover_correct

    @leftover_correct.setter
    def leftover_correct(self, leftover_correct):
        """Set the leftover_correct of this ReactAggregateResponseContentConfusionMatrix.

        Total count of all correct predictions for classes that did not have a statistically significant amount. 

        :param leftover_correct: The leftover_correct of this ReactAggregateResponseContentConfusionMatrix.
        :type leftover_correct: int
        """

        self._leftover_correct = leftover_correct

    @property
    def leftover_incorrect(self):
        """Get the leftover_incorrect of this ReactAggregateResponseContentConfusionMatrix.

        Total count of all incorrect predictions for classes that did not have a statistically significant amount. 

        :return: The leftover_incorrect of this ReactAggregateResponseContentConfusionMatrix.
        :rtype: int
        """
        return self._leftover_incorrect

    @leftover_incorrect.setter
    def leftover_incorrect(self, leftover_incorrect):
        """Set the leftover_incorrect of this ReactAggregateResponseContentConfusionMatrix.

        Total count of all incorrect predictions for classes that did not have a statistically significant amount. 

        :param leftover_incorrect: The leftover_incorrect of this ReactAggregateResponseContentConfusionMatrix.
        :type leftover_incorrect: int
        """

        self._leftover_incorrect = leftover_incorrect

    @property
    def other_counts(self):
        """Get the other_counts of this ReactAggregateResponseContentConfusionMatrix.

        Total count of all other statistically insignificant predictions for classes that were predicted correctly with significance. 

        :return: The other_counts of this ReactAggregateResponseContentConfusionMatrix.
        :rtype: int
        """
        return self._other_counts

    @other_counts.setter
    def other_counts(self, other_counts):
        """Set the other_counts of this ReactAggregateResponseContentConfusionMatrix.

        Total count of all other statistically insignificant predictions for classes that were predicted correctly with significance. 

        :param other_counts: The other_counts of this ReactAggregateResponseContentConfusionMatrix.
        :type other_counts: int
        """

        self._other_counts = other_counts

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
        if not isinstance(other, ReactAggregateResponseContentConfusionMatrix):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, ReactAggregateResponseContentConfusionMatrix):
            return True

        return self.to_dict() != other.to_dict()

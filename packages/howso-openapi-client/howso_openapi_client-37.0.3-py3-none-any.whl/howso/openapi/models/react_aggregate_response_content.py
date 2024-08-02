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


class ReactAggregateResponseContent(object):
    """
    Auto-generated OpenAPI type.

    Prediction feature statistics and details.
    """

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    openapi_types = {
        'accuracy': 'float',
        'confusion_matrix': 'ReactAggregateResponseContentConfusionMatrix',
        'feature_contributions_full': 'float',
        'feature_contributions_robust': 'float',
        'mae': 'float',
        'feature_residuals_full': 'float',
        'feature_residuals_robust': 'float',
        'feature_mda_full': 'float',
        'feature_mda_robust': 'float',
        'feature_mda_permutation_full': 'float',
        'feature_mda_permutation_robust': 'float',
        'precision': 'float',
        'r2': 'float',
        'recall': 'float',
        'missing_value_accuracy': 'float',
        'rmse': 'float',
        'spearman_coeff': 'float',
        'mcc': 'float'
    }

    attribute_map = {
        'accuracy': 'accuracy',
        'confusion_matrix': 'confusion_matrix',
        'feature_contributions_full': 'feature_contributions_full',
        'feature_contributions_robust': 'feature_contributions_robust',
        'mae': 'mae',
        'feature_residuals_full': 'feature_residuals_full',
        'feature_residuals_robust': 'feature_residuals_robust',
        'feature_mda_full': 'feature_mda_full',
        'feature_mda_robust': 'feature_mda_robust',
        'feature_mda_permutation_full': 'feature_mda_permutation_full',
        'feature_mda_permutation_robust': 'feature_mda_permutation_robust',
        'precision': 'precision',
        'r2': 'r2',
        'recall': 'recall',
        'missing_value_accuracy': 'missing_value_accuracy',
        'rmse': 'rmse',
        'spearman_coeff': 'spearman_coeff',
        'mcc': 'mcc'
    }

    nullable_attributes = [
        'accuracy', 
        'confusion_matrix', 
        'feature_contributions_full', 
        'feature_contributions_robust', 
        'mae', 
        'feature_residuals_full', 
        'feature_residuals_robust', 
        'feature_mda_full', 
        'feature_mda_robust', 
        'feature_mda_permutation_full', 
        'feature_mda_permutation_robust', 
        'precision', 
        'r2', 
        'recall', 
        'missing_value_accuracy', 
        'rmse', 
        'spearman_coeff', 
        'mcc', 
    ]

    discriminator = None

    def __init__(self, accuracy=None, confusion_matrix=None, feature_contributions_full=None, feature_contributions_robust=None, mae=None, feature_residuals_full=None, feature_residuals_robust=None, feature_mda_full=None, feature_mda_robust=None, feature_mda_permutation_full=None, feature_mda_permutation_robust=None, precision=None, r2=None, recall=None, missing_value_accuracy=None, rmse=None, spearman_coeff=None, mcc=None, local_vars_configuration=None):  # noqa: E501
        """ReactAggregateResponseContent - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default_copy()
        self.local_vars_configuration = local_vars_configuration

        self._accuracy = None
        self._confusion_matrix = None
        self._feature_contributions_full = None
        self._feature_contributions_robust = None
        self._mae = None
        self._feature_residuals_full = None
        self._feature_residuals_robust = None
        self._feature_mda_full = None
        self._feature_mda_robust = None
        self._feature_mda_permutation_full = None
        self._feature_mda_permutation_robust = None
        self._precision = None
        self._r2 = None
        self._recall = None
        self._missing_value_accuracy = None
        self._rmse = None
        self._spearman_coeff = None
        self._mcc = None

        self.accuracy = accuracy
        self.confusion_matrix = confusion_matrix
        self.feature_contributions_full = feature_contributions_full
        self.feature_contributions_robust = feature_contributions_robust
        self.mae = mae
        self.feature_residuals_full = feature_residuals_full
        self.feature_residuals_robust = feature_residuals_robust
        self.feature_mda_full = feature_mda_full
        self.feature_mda_robust = feature_mda_robust
        self.feature_mda_permutation_full = feature_mda_permutation_full
        self.feature_mda_permutation_robust = feature_mda_permutation_robust
        self.precision = precision
        self.r2 = r2
        self.recall = recall
        self.missing_value_accuracy = missing_value_accuracy
        self.rmse = rmse
        self.spearman_coeff = spearman_coeff
        self.mcc = mcc

    @property
    def accuracy(self):
        """Get the accuracy of this ReactAggregateResponseContent.

        The accuracy (1 - mean absolute error) value. Applicable only for nominal features, computed by computing residuals. 

        :return: The accuracy of this ReactAggregateResponseContent.
        :rtype: float
        """
        return self._accuracy

    @accuracy.setter
    def accuracy(self, accuracy):
        """Set the accuracy of this ReactAggregateResponseContent.

        The accuracy (1 - mean absolute error) value. Applicable only for nominal features, computed by computing residuals. 

        :param accuracy: The accuracy of this ReactAggregateResponseContent.
        :type accuracy: float
        """

        self._accuracy = accuracy

    @property
    def confusion_matrix(self):
        """Get the confusion_matrix of this ReactAggregateResponseContent.


        :return: The confusion_matrix of this ReactAggregateResponseContent.
        :rtype: ReactAggregateResponseContentConfusionMatrix
        """
        return self._confusion_matrix

    @confusion_matrix.setter
    def confusion_matrix(self, confusion_matrix):
        """Set the confusion_matrix of this ReactAggregateResponseContent.


        :param confusion_matrix: The confusion_matrix of this ReactAggregateResponseContent.
        :type confusion_matrix: ReactAggregateResponseContentConfusionMatrix
        """

        self._confusion_matrix = confusion_matrix

    @property
    def feature_contributions_full(self):
        """Get the feature_contributions_full of this ReactAggregateResponseContent.

        The full contribution to the predicted value of an action feature. 

        :return: The feature_contributions_full of this ReactAggregateResponseContent.
        :rtype: float
        """
        return self._feature_contributions_full

    @feature_contributions_full.setter
    def feature_contributions_full(self, feature_contributions_full):
        """Set the feature_contributions_full of this ReactAggregateResponseContent.

        The full contribution to the predicted value of an action feature. 

        :param feature_contributions_full: The feature_contributions_full of this ReactAggregateResponseContent.
        :type feature_contributions_full: float
        """

        self._feature_contributions_full = feature_contributions_full

    @property
    def feature_contributions_robust(self):
        """Get the feature_contributions_robust of this ReactAggregateResponseContent.

        The robust contribution to the predicted value of an action feature. 

        :return: The feature_contributions_robust of this ReactAggregateResponseContent.
        :rtype: float
        """
        return self._feature_contributions_robust

    @feature_contributions_robust.setter
    def feature_contributions_robust(self, feature_contributions_robust):
        """Set the feature_contributions_robust of this ReactAggregateResponseContent.

        The robust contribution to the predicted value of an action feature. 

        :param feature_contributions_robust: The feature_contributions_robust of this ReactAggregateResponseContent.
        :type feature_contributions_robust: float
        """

        self._feature_contributions_robust = feature_contributions_robust

    @property
    def mae(self):
        """Get the mae of this ReactAggregateResponseContent.

        The mean absolute error value. 

        :return: The mae of this ReactAggregateResponseContent.
        :rtype: float
        """
        return self._mae

    @mae.setter
    def mae(self, mae):
        """Set the mae of this ReactAggregateResponseContent.

        The mean absolute error value. 

        :param mae: The mae of this ReactAggregateResponseContent.
        :type mae: float
        """

        self._mae = mae

    @property
    def feature_residuals_full(self):
        """Get the feature_residuals_full of this ReactAggregateResponseContent.

        The full feature residuals. 

        :return: The feature_residuals_full of this ReactAggregateResponseContent.
        :rtype: float
        """
        return self._feature_residuals_full

    @feature_residuals_full.setter
    def feature_residuals_full(self, feature_residuals_full):
        """Set the feature_residuals_full of this ReactAggregateResponseContent.

        The full feature residuals. 

        :param feature_residuals_full: The feature_residuals_full of this ReactAggregateResponseContent.
        :type feature_residuals_full: float
        """

        self._feature_residuals_full = feature_residuals_full

    @property
    def feature_residuals_robust(self):
        """Get the feature_residuals_robust of this ReactAggregateResponseContent.

        The robust feature residuals. 

        :return: The feature_residuals_robust of this ReactAggregateResponseContent.
        :rtype: float
        """
        return self._feature_residuals_robust

    @feature_residuals_robust.setter
    def feature_residuals_robust(self, feature_residuals_robust):
        """Set the feature_residuals_robust of this ReactAggregateResponseContent.

        The robust feature residuals. 

        :param feature_residuals_robust: The feature_residuals_robust of this ReactAggregateResponseContent.
        :type feature_residuals_robust: float
        """

        self._feature_residuals_robust = feature_residuals_robust

    @property
    def feature_mda_full(self):
        """Get the feature_mda_full of this ReactAggregateResponseContent.

        The full mean decrease in accuracy value. Computed by dropping each feature and use the full set of remaining context features for each prediction. 

        :return: The feature_mda_full of this ReactAggregateResponseContent.
        :rtype: float
        """
        return self._feature_mda_full

    @feature_mda_full.setter
    def feature_mda_full(self, feature_mda_full):
        """Set the feature_mda_full of this ReactAggregateResponseContent.

        The full mean decrease in accuracy value. Computed by dropping each feature and use the full set of remaining context features for each prediction. 

        :param feature_mda_full: The feature_mda_full of this ReactAggregateResponseContent.
        :type feature_mda_full: float
        """

        self._feature_mda_full = feature_mda_full

    @property
    def feature_mda_robust(self):
        """Get the feature_mda_robust of this ReactAggregateResponseContent.

        The robust mean decrease in accuracy value. Computed by dropping each feature and use the full set of remaining context features for each prediction. 

        :return: The feature_mda_robust of this ReactAggregateResponseContent.
        :rtype: float
        """
        return self._feature_mda_robust

    @feature_mda_robust.setter
    def feature_mda_robust(self, feature_mda_robust):
        """Set the feature_mda_robust of this ReactAggregateResponseContent.

        The robust mean decrease in accuracy value. Computed by dropping each feature and use the full set of remaining context features for each prediction. 

        :param feature_mda_robust: The feature_mda_robust of this ReactAggregateResponseContent.
        :type feature_mda_robust: float
        """

        self._feature_mda_robust = feature_mda_robust

    @property
    def feature_mda_permutation_full(self):
        """Get the feature_mda_permutation_full of this ReactAggregateResponseContent.

        The full mean decrease in accuracy permutation value. Computed by scrambling each feature and using the full set of remaining context features for each prediction. 

        :return: The feature_mda_permutation_full of this ReactAggregateResponseContent.
        :rtype: float
        """
        return self._feature_mda_permutation_full

    @feature_mda_permutation_full.setter
    def feature_mda_permutation_full(self, feature_mda_permutation_full):
        """Set the feature_mda_permutation_full of this ReactAggregateResponseContent.

        The full mean decrease in accuracy permutation value. Computed by scrambling each feature and using the full set of remaining context features for each prediction. 

        :param feature_mda_permutation_full: The feature_mda_permutation_full of this ReactAggregateResponseContent.
        :type feature_mda_permutation_full: float
        """

        self._feature_mda_permutation_full = feature_mda_permutation_full

    @property
    def feature_mda_permutation_robust(self):
        """Get the feature_mda_permutation_robust of this ReactAggregateResponseContent.

        The robust mean decrease in accuracy permutation value. Computed by scrambling each feature and using the full set of remaining context features for each prediction. 

        :return: The feature_mda_permutation_robust of this ReactAggregateResponseContent.
        :rtype: float
        """
        return self._feature_mda_permutation_robust

    @feature_mda_permutation_robust.setter
    def feature_mda_permutation_robust(self, feature_mda_permutation_robust):
        """Set the feature_mda_permutation_robust of this ReactAggregateResponseContent.

        The robust mean decrease in accuracy permutation value. Computed by scrambling each feature and using the full set of remaining context features for each prediction. 

        :param feature_mda_permutation_robust: The feature_mda_permutation_robust of this ReactAggregateResponseContent.
        :type feature_mda_permutation_robust: float
        """

        self._feature_mda_permutation_robust = feature_mda_permutation_robust

    @property
    def precision(self):
        """Get the precision of this ReactAggregateResponseContent.

        The precision (positive predictive) value. Applicable only for nominal features, computed by computing residuals. 

        :return: The precision of this ReactAggregateResponseContent.
        :rtype: float
        """
        return self._precision

    @precision.setter
    def precision(self, precision):
        """Set the precision of this ReactAggregateResponseContent.

        The precision (positive predictive) value. Applicable only for nominal features, computed by computing residuals. 

        :param precision: The precision of this ReactAggregateResponseContent.
        :type precision: float
        """

        self._precision = precision

    @property
    def r2(self):
        """Get the r2 of this ReactAggregateResponseContent.

        The R-squared (coefficient of determination) value. Applicable only for continuous features, computed by computing residuals. 

        :return: The r2 of this ReactAggregateResponseContent.
        :rtype: float
        """
        return self._r2

    @r2.setter
    def r2(self, r2):
        """Set the r2 of this ReactAggregateResponseContent.

        The R-squared (coefficient of determination) value. Applicable only for continuous features, computed by computing residuals. 

        :param r2: The r2 of this ReactAggregateResponseContent.
        :type r2: float
        """

        self._r2 = r2

    @property
    def recall(self):
        """Get the recall of this ReactAggregateResponseContent.

        The recall (sensitivity) value. Applicable only for nominal features, computed by computing residuals. 

        :return: The recall of this ReactAggregateResponseContent.
        :rtype: float
        """
        return self._recall

    @recall.setter
    def recall(self, recall):
        """Set the recall of this ReactAggregateResponseContent.

        The recall (sensitivity) value. Applicable only for nominal features, computed by computing residuals. 

        :param recall: The recall of this ReactAggregateResponseContent.
        :type recall: float
        """

        self._recall = recall

    @property
    def missing_value_accuracy(self):
        """Get the missing_value_accuracy of this ReactAggregateResponseContent.

        The missing value accuracy. 

        :return: The missing_value_accuracy of this ReactAggregateResponseContent.
        :rtype: float
        """
        return self._missing_value_accuracy

    @missing_value_accuracy.setter
    def missing_value_accuracy(self, missing_value_accuracy):
        """Set the missing_value_accuracy of this ReactAggregateResponseContent.

        The missing value accuracy. 

        :param missing_value_accuracy: The missing_value_accuracy of this ReactAggregateResponseContent.
        :type missing_value_accuracy: float
        """

        self._missing_value_accuracy = missing_value_accuracy

    @property
    def rmse(self):
        """Get the rmse of this ReactAggregateResponseContent.

        The root-mean-squared-error value. Applicable only for continuous features, computed by computing residuals. 

        :return: The rmse of this ReactAggregateResponseContent.
        :rtype: float
        """
        return self._rmse

    @rmse.setter
    def rmse(self, rmse):
        """Set the rmse of this ReactAggregateResponseContent.

        The root-mean-squared-error value. Applicable only for continuous features, computed by computing residuals. 

        :param rmse: The rmse of this ReactAggregateResponseContent.
        :type rmse: float
        """

        self._rmse = rmse

    @property
    def spearman_coeff(self):
        """Get the spearman_coeff of this ReactAggregateResponseContent.

        The Spearman's rank correlation coefficient value. Applicable only for continuous features, computed by computing residuals. 

        :return: The spearman_coeff of this ReactAggregateResponseContent.
        :rtype: float
        """
        return self._spearman_coeff

    @spearman_coeff.setter
    def spearman_coeff(self, spearman_coeff):
        """Set the spearman_coeff of this ReactAggregateResponseContent.

        The Spearman's rank correlation coefficient value. Applicable only for continuous features, computed by computing residuals. 

        :param spearman_coeff: The spearman_coeff of this ReactAggregateResponseContent.
        :type spearman_coeff: float
        """

        self._spearman_coeff = spearman_coeff

    @property
    def mcc(self):
        """Get the mcc of this ReactAggregateResponseContent.

        The Matthews correlation coefficient value. Applicable only for nominal features, computed by computing residuals. 

        :return: The mcc of this ReactAggregateResponseContent.
        :rtype: float
        """
        return self._mcc

    @mcc.setter
    def mcc(self, mcc):
        """Set the mcc of this ReactAggregateResponseContent.

        The Matthews correlation coefficient value. Applicable only for nominal features, computed by computing residuals. 

        :param mcc: The mcc of this ReactAggregateResponseContent.
        :type mcc: float
        """

        self._mcc = mcc

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
        if not isinstance(other, ReactAggregateResponseContent):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, ReactAggregateResponseContent):
            return True

        return self.to_dict() != other.to_dict()

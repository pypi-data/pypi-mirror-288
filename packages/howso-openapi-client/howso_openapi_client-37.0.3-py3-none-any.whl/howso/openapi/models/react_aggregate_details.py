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


class ReactAggregateDetails(object):
    """
    Auto-generated OpenAPI type.

    Returns details and prediction stats data for a given reaction for the specified flags. 
    """

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    openapi_types = {
        'prediction_stats': 'bool',
        'feature_residuals_full': 'bool',
        'feature_residuals_robust': 'bool',
        'feature_contributions_full': 'bool',
        'feature_contributions_robust': 'bool',
        'feature_mda_full': 'bool',
        'feature_mda_robust': 'bool',
        'feature_mda_permutation_full': 'bool',
        'feature_mda_permutation_robust': 'bool',
        'action_condition': 'dict[str, object]',
        'action_condition_precision': 'str',
        'action_num_cases': 'float',
        'context_condition': 'dict[str, object]',
        'context_condition_precision': 'str',
        'context_precision_num_cases': 'float',
        'prediction_stats_features': 'list[str]',
        'selected_prediction_stats': 'list[str]'
    }

    attribute_map = {
        'prediction_stats': 'prediction_stats',
        'feature_residuals_full': 'feature_residuals_full',
        'feature_residuals_robust': 'feature_residuals_robust',
        'feature_contributions_full': 'feature_contributions_full',
        'feature_contributions_robust': 'feature_contributions_robust',
        'feature_mda_full': 'feature_mda_full',
        'feature_mda_robust': 'feature_mda_robust',
        'feature_mda_permutation_full': 'feature_mda_permutation_full',
        'feature_mda_permutation_robust': 'feature_mda_permutation_robust',
        'action_condition': 'action_condition',
        'action_condition_precision': 'action_condition_precision',
        'action_num_cases': 'action_num_cases',
        'context_condition': 'context_condition',
        'context_condition_precision': 'context_condition_precision',
        'context_precision_num_cases': 'context_precision_num_cases',
        'prediction_stats_features': 'prediction_stats_features',
        'selected_prediction_stats': 'selected_prediction_stats'
    }

    nullable_attributes = [
    ]

    discriminator = None

    def __init__(self, prediction_stats=None, feature_residuals_full=None, feature_residuals_robust=None, feature_contributions_full=None, feature_contributions_robust=None, feature_mda_full=None, feature_mda_robust=None, feature_mda_permutation_full=None, feature_mda_permutation_robust=None, action_condition=None, action_condition_precision=None, action_num_cases=None, context_condition=None, context_condition_precision=None, context_precision_num_cases=None, prediction_stats_features=None, selected_prediction_stats=None, local_vars_configuration=None):  # noqa: E501
        """ReactAggregateDetails - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default_copy()
        self.local_vars_configuration = local_vars_configuration

        self._prediction_stats = None
        self._feature_residuals_full = None
        self._feature_residuals_robust = None
        self._feature_contributions_full = None
        self._feature_contributions_robust = None
        self._feature_mda_full = None
        self._feature_mda_robust = None
        self._feature_mda_permutation_full = None
        self._feature_mda_permutation_robust = None
        self._action_condition = None
        self._action_condition_precision = None
        self._action_num_cases = None
        self._context_condition = None
        self._context_condition_precision = None
        self._context_precision_num_cases = None
        self._prediction_stats_features = None
        self._selected_prediction_stats = None

        if prediction_stats is not None:
            self.prediction_stats = prediction_stats
        if feature_residuals_full is not None:
            self.feature_residuals_full = feature_residuals_full
        if feature_residuals_robust is not None:
            self.feature_residuals_robust = feature_residuals_robust
        if feature_contributions_full is not None:
            self.feature_contributions_full = feature_contributions_full
        if feature_contributions_robust is not None:
            self.feature_contributions_robust = feature_contributions_robust
        if feature_mda_full is not None:
            self.feature_mda_full = feature_mda_full
        if feature_mda_robust is not None:
            self.feature_mda_robust = feature_mda_robust
        if feature_mda_permutation_full is not None:
            self.feature_mda_permutation_full = feature_mda_permutation_full
        if feature_mda_permutation_robust is not None:
            self.feature_mda_permutation_robust = feature_mda_permutation_robust
        if action_condition is not None:
            self.action_condition = action_condition
        if action_condition_precision is not None:
            self.action_condition_precision = action_condition_precision
        if action_num_cases is not None:
            self.action_num_cases = action_num_cases
        if context_condition is not None:
            self.context_condition = context_condition
        if context_condition_precision is not None:
            self.context_condition_precision = context_condition_precision
        if context_precision_num_cases is not None:
            self.context_precision_num_cases = context_precision_num_cases
        if prediction_stats_features is not None:
            self.prediction_stats_features = prediction_stats_features
        if selected_prediction_stats is not None:
            self.selected_prediction_stats = selected_prediction_stats

    @property
    def prediction_stats(self):
        """Get the prediction_stats of this ReactAggregateDetails.

        If true outputs full feature prediction stats for all (context and action) features. The prediction stats returned are set by the \"selected_prediction_stats\" parameter in the 'details' parameter. Uses full calculations, which uses leave-one-out for features for computations. False removes cached values. 

        :return: The prediction_stats of this ReactAggregateDetails.
        :rtype: bool
        """
        return self._prediction_stats

    @prediction_stats.setter
    def prediction_stats(self, prediction_stats):
        """Set the prediction_stats of this ReactAggregateDetails.

        If true outputs full feature prediction stats for all (context and action) features. The prediction stats returned are set by the \"selected_prediction_stats\" parameter in the 'details' parameter. Uses full calculations, which uses leave-one-out for features for computations. False removes cached values. 

        :param prediction_stats: The prediction_stats of this ReactAggregateDetails.
        :type prediction_stats: bool
        """

        self._prediction_stats = prediction_stats

    @property
    def feature_residuals_full(self):
        """Get the feature_residuals_full of this ReactAggregateDetails.

        For each context_feature, use the full set of all other context_features to predict the feature. False removes cached values. When \"prediction_stats\" in the \"details\" parameter is true, the Trainee will also calculate and cache the full feature residuals. 

        :return: The feature_residuals_full of this ReactAggregateDetails.
        :rtype: bool
        """
        return self._feature_residuals_full

    @feature_residuals_full.setter
    def feature_residuals_full(self, feature_residuals_full):
        """Set the feature_residuals_full of this ReactAggregateDetails.

        For each context_feature, use the full set of all other context_features to predict the feature. False removes cached values. When \"prediction_stats\" in the \"details\" parameter is true, the Trainee will also calculate and cache the full feature residuals. 

        :param feature_residuals_full: The feature_residuals_full of this ReactAggregateDetails.
        :type feature_residuals_full: bool
        """

        self._feature_residuals_full = feature_residuals_full

    @property
    def feature_residuals_robust(self):
        """Get the feature_residuals_robust of this ReactAggregateDetails.

        For each context_feature, use the robust (power set/permutations) set of all other context_features to predict the feature. False removes cached values. 

        :return: The feature_residuals_robust of this ReactAggregateDetails.
        :rtype: bool
        """
        return self._feature_residuals_robust

    @feature_residuals_robust.setter
    def feature_residuals_robust(self, feature_residuals_robust):
        """Set the feature_residuals_robust of this ReactAggregateDetails.

        For each context_feature, use the robust (power set/permutations) set of all other context_features to predict the feature. False removes cached values. 

        :param feature_residuals_robust: The feature_residuals_robust of this ReactAggregateDetails.
        :type feature_residuals_robust: bool
        """

        self._feature_residuals_robust = feature_residuals_robust

    @property
    def feature_contributions_full(self):
        """Get the feature_contributions_full of this ReactAggregateDetails.

        For each context_feature, use the full set of all other context_features to compute the mean absolute delta between prediction of the action feature with and without the context features in the model. False removes cached values. 

        :return: The feature_contributions_full of this ReactAggregateDetails.
        :rtype: bool
        """
        return self._feature_contributions_full

    @feature_contributions_full.setter
    def feature_contributions_full(self, feature_contributions_full):
        """Set the feature_contributions_full of this ReactAggregateDetails.

        For each context_feature, use the full set of all other context_features to compute the mean absolute delta between prediction of the action feature with and without the context features in the model. False removes cached values. 

        :param feature_contributions_full: The feature_contributions_full of this ReactAggregateDetails.
        :type feature_contributions_full: bool
        """

        self._feature_contributions_full = feature_contributions_full

    @property
    def feature_contributions_robust(self):
        """Get the feature_contributions_robust of this ReactAggregateDetails.

        For each context_feature, use the robust (power set/permutation) set of all other context features to compute the mean absolute delta between prediction of the action feature with and without the context features in the model. False removes cached values. 

        :return: The feature_contributions_robust of this ReactAggregateDetails.
        :rtype: bool
        """
        return self._feature_contributions_robust

    @feature_contributions_robust.setter
    def feature_contributions_robust(self, feature_contributions_robust):
        """Set the feature_contributions_robust of this ReactAggregateDetails.

        For each context_feature, use the robust (power set/permutation) set of all other context features to compute the mean absolute delta between prediction of the action feature with and without the context features in the model. False removes cached values. 

        :param feature_contributions_robust: The feature_contributions_robust of this ReactAggregateDetails.
        :type feature_contributions_robust: bool
        """

        self._feature_contributions_robust = feature_contributions_robust

    @property
    def feature_mda_full(self):
        """Get the feature_mda_full of this ReactAggregateDetails.

        When True will compute Mean Decrease in Accuracy (MDA) for each context feature at predicting the action feature. Drop each feature and use the full set of remaining context features for each prediction. False removes cached values. 

        :return: The feature_mda_full of this ReactAggregateDetails.
        :rtype: bool
        """
        return self._feature_mda_full

    @feature_mda_full.setter
    def feature_mda_full(self, feature_mda_full):
        """Set the feature_mda_full of this ReactAggregateDetails.

        When True will compute Mean Decrease in Accuracy (MDA) for each context feature at predicting the action feature. Drop each feature and use the full set of remaining context features for each prediction. False removes cached values. 

        :param feature_mda_full: The feature_mda_full of this ReactAggregateDetails.
        :type feature_mda_full: bool
        """

        self._feature_mda_full = feature_mda_full

    @property
    def feature_mda_robust(self):
        """Get the feature_mda_robust of this ReactAggregateDetails.

        Compute Mean Decrease in Accuracy (MDA) by dropping each feature and using the robust (power set/permutations) set of remaining context features for each prediction. False removes cached values. 

        :return: The feature_mda_robust of this ReactAggregateDetails.
        :rtype: bool
        """
        return self._feature_mda_robust

    @feature_mda_robust.setter
    def feature_mda_robust(self, feature_mda_robust):
        """Set the feature_mda_robust of this ReactAggregateDetails.

        Compute Mean Decrease in Accuracy (MDA) by dropping each feature and using the robust (power set/permutations) set of remaining context features for each prediction. False removes cached values. 

        :param feature_mda_robust: The feature_mda_robust of this ReactAggregateDetails.
        :type feature_mda_robust: bool
        """

        self._feature_mda_robust = feature_mda_robust

    @property
    def feature_mda_permutation_full(self):
        """Get the feature_mda_permutation_full of this ReactAggregateDetails.

        Compute Mean Decrease in Accuracy (MDA) by scrambling each feature and using the full set of remaining context features for each prediction. False removes cached values. 

        :return: The feature_mda_permutation_full of this ReactAggregateDetails.
        :rtype: bool
        """
        return self._feature_mda_permutation_full

    @feature_mda_permutation_full.setter
    def feature_mda_permutation_full(self, feature_mda_permutation_full):
        """Set the feature_mda_permutation_full of this ReactAggregateDetails.

        Compute Mean Decrease in Accuracy (MDA) by scrambling each feature and using the full set of remaining context features for each prediction. False removes cached values. 

        :param feature_mda_permutation_full: The feature_mda_permutation_full of this ReactAggregateDetails.
        :type feature_mda_permutation_full: bool
        """

        self._feature_mda_permutation_full = feature_mda_permutation_full

    @property
    def feature_mda_permutation_robust(self):
        """Get the feature_mda_permutation_robust of this ReactAggregateDetails.

        Compute MDA by scrambling each feature and using the robust (power set/permutations) set of remaining context features for each prediction. False removes cached values. 

        :return: The feature_mda_permutation_robust of this ReactAggregateDetails.
        :rtype: bool
        """
        return self._feature_mda_permutation_robust

    @feature_mda_permutation_robust.setter
    def feature_mda_permutation_robust(self, feature_mda_permutation_robust):
        """Set the feature_mda_permutation_robust of this ReactAggregateDetails.

        Compute MDA by scrambling each feature and using the robust (power set/permutations) set of remaining context features for each prediction. False removes cached values. 

        :param feature_mda_permutation_robust: The feature_mda_permutation_robust of this ReactAggregateDetails.
        :type feature_mda_permutation_robust: bool
        """

        self._feature_mda_permutation_robust = feature_mda_permutation_robust

    @property
    def action_condition(self):
        """Get the action_condition of this ReactAggregateDetails.

        A condition map to select the action set, which is the dataset for which the prediction stats are for. If both action_condition and context_condition are provided, then all of the action cases selected by the action_condition will be excluded from the context set, which is the set being queried to make predictions on the action set, effectively holding them out. If only action_condition is specified, then only the single predicted case will be left out.  The dictionary keys are the feature name and values are one of: - None - A value, must match exactly. - An array of two numeric values, specifying an inclusive range. Only applicable to continuous and numeric ordinal features. - An array of string values, must match any of these values exactly. Only applicable to nominal and string ordinal features. 

        :return: The action_condition of this ReactAggregateDetails.
        :rtype: dict[str, object]
        """
        return self._action_condition

    @action_condition.setter
    def action_condition(self, action_condition):
        """Set the action_condition of this ReactAggregateDetails.

        A condition map to select the action set, which is the dataset for which the prediction stats are for. If both action_condition and context_condition are provided, then all of the action cases selected by the action_condition will be excluded from the context set, which is the set being queried to make predictions on the action set, effectively holding them out. If only action_condition is specified, then only the single predicted case will be left out.  The dictionary keys are the feature name and values are one of: - None - A value, must match exactly. - An array of two numeric values, specifying an inclusive range. Only applicable to continuous and numeric ordinal features. - An array of string values, must match any of these values exactly. Only applicable to nominal and string ordinal features. 

        :param action_condition: The action_condition of this ReactAggregateDetails.
        :type action_condition: dict[str, object]
        """

        self._action_condition = action_condition

    @property
    def action_condition_precision(self):
        """Get the action_condition_precision of this ReactAggregateDetails.

        Exact matching or fuzzy matching. Only used if action_condition is not not null.

        :return: The action_condition_precision of this ReactAggregateDetails.
        :rtype: str
        """
        return self._action_condition_precision

    @action_condition_precision.setter
    def action_condition_precision(self, action_condition_precision):
        """Set the action_condition_precision of this ReactAggregateDetails.

        Exact matching or fuzzy matching. Only used if action_condition is not not null.

        :param action_condition_precision: The action_condition_precision of this ReactAggregateDetails.
        :type action_condition_precision: str
        """
        allowed_values = ["exact", "similar"]  # noqa: E501
        if self.local_vars_configuration.client_side_validation and action_condition_precision not in allowed_values:  # noqa: E501
            raise ValueError(
                "Invalid value for `action_condition_precision` ({0}), must be one of {1}"  # noqa: E501
                .format(action_condition_precision, allowed_values)
            )

        self._action_condition_precision = action_condition_precision

    @property
    def action_num_cases(self):
        """Get the action_num_cases of this ReactAggregateDetails.

        The maximum amount of cases to use to calculate prediction stats. If not specified, the limit will be k cases if precision is \"similar\", or 1000 cases if precision is \"exact\". Works with or without action_condition. If action_condition is set: - If None, will be set to k if precision is \"similar\" or no limit if precision is \"exact\". If action_condition is not set: - If None, will be set to the Howso default limit of 2000. 

        :return: The action_num_cases of this ReactAggregateDetails.
        :rtype: float
        """
        return self._action_num_cases

    @action_num_cases.setter
    def action_num_cases(self, action_num_cases):
        """Set the action_num_cases of this ReactAggregateDetails.

        The maximum amount of cases to use to calculate prediction stats. If not specified, the limit will be k cases if precision is \"similar\", or 1000 cases if precision is \"exact\". Works with or without action_condition. If action_condition is set: - If None, will be set to k if precision is \"similar\" or no limit if precision is \"exact\". If action_condition is not set: - If None, will be set to the Howso default limit of 2000. 

        :param action_num_cases: The action_num_cases of this ReactAggregateDetails.
        :type action_num_cases: float
        """

        self._action_num_cases = action_num_cases

    @property
    def context_condition(self):
        """Get the context_condition of this ReactAggregateDetails.

        A condition map to select the context set, which is the set being queried to make predictions on the action set. If both action_condition and context_condition are provided, then all of the cases from the action set, which is the dataset for which the prediction stats are for, will be excluded from the context set, effectively holding them out. If only action_condition is specified, then only the single predicted case will be left out.  The dictionary keys are the feature name and values are one of: - None - A value, must match exactly. - An array of two numeric values, specifying an inclusive range. Only applicable to continuous and numeric ordinal features. - An array of string values, must match any of these values exactly. Only applicable to nominal and string ordinal features. 

        :return: The context_condition of this ReactAggregateDetails.
        :rtype: dict[str, object]
        """
        return self._context_condition

    @context_condition.setter
    def context_condition(self, context_condition):
        """Set the context_condition of this ReactAggregateDetails.

        A condition map to select the context set, which is the set being queried to make predictions on the action set. If both action_condition and context_condition are provided, then all of the cases from the action set, which is the dataset for which the prediction stats are for, will be excluded from the context set, effectively holding them out. If only action_condition is specified, then only the single predicted case will be left out.  The dictionary keys are the feature name and values are one of: - None - A value, must match exactly. - An array of two numeric values, specifying an inclusive range. Only applicable to continuous and numeric ordinal features. - An array of string values, must match any of these values exactly. Only applicable to nominal and string ordinal features. 

        :param context_condition: The context_condition of this ReactAggregateDetails.
        :type context_condition: dict[str, object]
        """

        self._context_condition = context_condition

    @property
    def context_condition_precision(self):
        """Get the context_condition_precision of this ReactAggregateDetails.

        Exact matching or fuzzy matching. Only used if context_condition is not not null.

        :return: The context_condition_precision of this ReactAggregateDetails.
        :rtype: str
        """
        return self._context_condition_precision

    @context_condition_precision.setter
    def context_condition_precision(self, context_condition_precision):
        """Set the context_condition_precision of this ReactAggregateDetails.

        Exact matching or fuzzy matching. Only used if context_condition is not not null.

        :param context_condition_precision: The context_condition_precision of this ReactAggregateDetails.
        :type context_condition_precision: str
        """
        allowed_values = ["exact", "similar"]  # noqa: E501
        if self.local_vars_configuration.client_side_validation and context_condition_precision not in allowed_values:  # noqa: E501
            raise ValueError(
                "Invalid value for `context_condition_precision` ({0}), must be one of {1}"  # noqa: E501
                .format(context_condition_precision, allowed_values)
            )

        self._context_condition_precision = context_condition_precision

    @property
    def context_precision_num_cases(self):
        """Get the context_precision_num_cases of this ReactAggregateDetails.

        Limit on the number of context cases when context_condition_precision is set to \"similar\". If None, will be set to k. 

        :return: The context_precision_num_cases of this ReactAggregateDetails.
        :rtype: float
        """
        return self._context_precision_num_cases

    @context_precision_num_cases.setter
    def context_precision_num_cases(self, context_precision_num_cases):
        """Set the context_precision_num_cases of this ReactAggregateDetails.

        Limit on the number of context cases when context_condition_precision is set to \"similar\". If None, will be set to k. 

        :param context_precision_num_cases: The context_precision_num_cases of this ReactAggregateDetails.
        :type context_precision_num_cases: float
        """

        self._context_precision_num_cases = context_precision_num_cases

    @property
    def prediction_stats_features(self):
        """Get the prediction_stats_features of this ReactAggregateDetails.

        List of features to use when calculating conditional prediction stats. Should contain all action and context features desired. If ``action_feature`` is also provided, that feature will automatically be appended to this list if it is not already in the list. 

        :return: The prediction_stats_features of this ReactAggregateDetails.
        :rtype: list[str]
        """
        return self._prediction_stats_features

    @prediction_stats_features.setter
    def prediction_stats_features(self, prediction_stats_features):
        """Set the prediction_stats_features of this ReactAggregateDetails.

        List of features to use when calculating conditional prediction stats. Should contain all action and context features desired. If ``action_feature`` is also provided, that feature will automatically be appended to this list if it is not already in the list. 

        :param prediction_stats_features: The prediction_stats_features of this ReactAggregateDetails.
        :type prediction_stats_features: list[str]
        """

        self._prediction_stats_features = prediction_stats_features

    @property
    def selected_prediction_stats(self):
        """Get the selected_prediction_stats of this ReactAggregateDetails.

        Types of stats to output. When unspecified, returns all except the confusion_matrix. If all, then returns all including the confusion_matrix.

        :return: The selected_prediction_stats of this ReactAggregateDetails.
        :rtype: list[str]
        """
        return self._selected_prediction_stats

    @selected_prediction_stats.setter
    def selected_prediction_stats(self, selected_prediction_stats):
        """Set the selected_prediction_stats of this ReactAggregateDetails.

        Types of stats to output. When unspecified, returns all except the confusion_matrix. If all, then returns all including the confusion_matrix.

        :param selected_prediction_stats: The selected_prediction_stats of this ReactAggregateDetails.
        :type selected_prediction_stats: list[str]
        """
        allowed_values = ["all", "accuracy", "confusion_matrix", "mae", "precision", "r2", "recall", "rmse", "spearman_coeff", "mcc", "missing_value_accuracy"]  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                not set(selected_prediction_stats).issubset(set(allowed_values))):  # noqa: E501
            raise ValueError(
                "Invalid values for `selected_prediction_stats` [{0}], must be a subset of [{1}]"  # noqa: E501
                .format(", ".join(map(str, set(selected_prediction_stats) - set(allowed_values))),  # noqa: E501
                        ", ".join(map(str, allowed_values)))
            )

        self._selected_prediction_stats = selected_prediction_stats

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
        if not isinstance(other, ReactAggregateDetails):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, ReactAggregateDetails):
            return True

        return self.to_dict() != other.to_dict()

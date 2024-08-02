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


class ReactAggregateRequest(object):
    """
    Auto-generated OpenAPI type.

    Request body for react aggregate.
    """

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    openapi_types = {
        'details': 'ReactAggregateDetails',
        'action_feature': 'str',
        'feature_influences_action_feature': 'str',
        'prediction_stats_action_feature': 'str',
        'context_features': 'list[str]',
        'hyperparameter_param_path': 'list[str]',
        'num_robust_influence_samples': 'int',
        'num_robust_influence_samples_per_case': 'int',
        'num_robust_residual_samples': 'int',
        'num_samples': 'int',
        'robust_hyperparameters': 'bool',
        'sample_model_fraction': 'float',
        'sub_model_size': 'int',
        'confusion_matrix_min_count': 'int',
        'residuals_hyperparameter_feature': 'str',
        'use_case_weights': 'bool',
        'weight_feature': 'str'
    }

    attribute_map = {
        'details': 'details',
        'action_feature': 'action_feature',
        'feature_influences_action_feature': 'feature_influences_action_feature',
        'prediction_stats_action_feature': 'prediction_stats_action_feature',
        'context_features': 'context_features',
        'hyperparameter_param_path': 'hyperparameter_param_path',
        'num_robust_influence_samples': 'num_robust_influence_samples',
        'num_robust_influence_samples_per_case': 'num_robust_influence_samples_per_case',
        'num_robust_residual_samples': 'num_robust_residual_samples',
        'num_samples': 'num_samples',
        'robust_hyperparameters': 'robust_hyperparameters',
        'sample_model_fraction': 'sample_model_fraction',
        'sub_model_size': 'sub_model_size',
        'confusion_matrix_min_count': 'confusion_matrix_min_count',
        'residuals_hyperparameter_feature': 'residuals_hyperparameter_feature',
        'use_case_weights': 'use_case_weights',
        'weight_feature': 'weight_feature'
    }

    nullable_attributes = [
    ]

    discriminator = None

    def __init__(self, details=None, action_feature=None, feature_influences_action_feature=None, prediction_stats_action_feature=None, context_features=None, hyperparameter_param_path=None, num_robust_influence_samples=None, num_robust_influence_samples_per_case=None, num_robust_residual_samples=None, num_samples=None, robust_hyperparameters=None, sample_model_fraction=None, sub_model_size=None, confusion_matrix_min_count=None, residuals_hyperparameter_feature=None, use_case_weights=None, weight_feature=None, local_vars_configuration=None):  # noqa: E501
        """ReactAggregateRequest - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default_copy()
        self.local_vars_configuration = local_vars_configuration

        self._details = None
        self._action_feature = None
        self._feature_influences_action_feature = None
        self._prediction_stats_action_feature = None
        self._context_features = None
        self._hyperparameter_param_path = None
        self._num_robust_influence_samples = None
        self._num_robust_influence_samples_per_case = None
        self._num_robust_residual_samples = None
        self._num_samples = None
        self._robust_hyperparameters = None
        self._sample_model_fraction = None
        self._sub_model_size = None
        self._confusion_matrix_min_count = None
        self._residuals_hyperparameter_feature = None
        self._use_case_weights = None
        self._weight_feature = None

        if details is not None:
            self.details = details
        if action_feature is not None:
            self.action_feature = action_feature
        if feature_influences_action_feature is not None:
            self.feature_influences_action_feature = feature_influences_action_feature
        if prediction_stats_action_feature is not None:
            self.prediction_stats_action_feature = prediction_stats_action_feature
        if context_features is not None:
            self.context_features = context_features
        if hyperparameter_param_path is not None:
            self.hyperparameter_param_path = hyperparameter_param_path
        if num_robust_influence_samples is not None:
            self.num_robust_influence_samples = num_robust_influence_samples
        if num_robust_influence_samples_per_case is not None:
            self.num_robust_influence_samples_per_case = num_robust_influence_samples_per_case
        if num_robust_residual_samples is not None:
            self.num_robust_residual_samples = num_robust_residual_samples
        if num_samples is not None:
            self.num_samples = num_samples
        if robust_hyperparameters is not None:
            self.robust_hyperparameters = robust_hyperparameters
        if sample_model_fraction is not None:
            self.sample_model_fraction = sample_model_fraction
        if sub_model_size is not None:
            self.sub_model_size = sub_model_size
        if confusion_matrix_min_count is not None:
            self.confusion_matrix_min_count = confusion_matrix_min_count
        if residuals_hyperparameter_feature is not None:
            self.residuals_hyperparameter_feature = residuals_hyperparameter_feature
        if use_case_weights is not None:
            self.use_case_weights = use_case_weights
        if weight_feature is not None:
            self.weight_feature = weight_feature

    @property
    def details(self):
        """Get the details of this ReactAggregateRequest.


        :return: The details of this ReactAggregateRequest.
        :rtype: ReactAggregateDetails
        """
        return self._details

    @details.setter
    def details(self, details):
        """Set the details of this ReactAggregateRequest.


        :param details: The details of this ReactAggregateRequest.
        :type details: ReactAggregateDetails
        """

        self._details = details

    @property
    def action_feature(self):
        """Get the action_feature of this ReactAggregateRequest.

        Name of target feature for which to do computations. If \"prediction_stats_action_feature\" and \"feature_influences_action_feature\" are not provided, they will default to this value. If \"feature_influences_action_feature\" is not provided and feature influences \"details\" are selected, this feature must be provided. 

        :return: The action_feature of this ReactAggregateRequest.
        :rtype: str
        """
        return self._action_feature

    @action_feature.setter
    def action_feature(self, action_feature):
        """Set the action_feature of this ReactAggregateRequest.

        Name of target feature for which to do computations. If \"prediction_stats_action_feature\" and \"feature_influences_action_feature\" are not provided, they will default to this value. If \"feature_influences_action_feature\" is not provided and feature influences \"details\" are selected, this feature must be provided. 

        :param action_feature: The action_feature of this ReactAggregateRequest.
        :type action_feature: str
        """

        self._action_feature = action_feature

    @property
    def feature_influences_action_feature(self):
        """Get the feature_influences_action_feature of this ReactAggregateRequest.

        When feature influences such as contributions and mda, use this feature as the action feature.  If not provided, will default to the \"action_feature\" if provided. If \"action_feature\" is not provided and feature influences \"details\" are selected, this feature must be provided. 

        :return: The feature_influences_action_feature of this ReactAggregateRequest.
        :rtype: str
        """
        return self._feature_influences_action_feature

    @feature_influences_action_feature.setter
    def feature_influences_action_feature(self, feature_influences_action_feature):
        """Set the feature_influences_action_feature of this ReactAggregateRequest.

        When feature influences such as contributions and mda, use this feature as the action feature.  If not provided, will default to the \"action_feature\" if provided. If \"action_feature\" is not provided and feature influences \"details\" are selected, this feature must be provided. 

        :param feature_influences_action_feature: The feature_influences_action_feature of this ReactAggregateRequest.
        :type feature_influences_action_feature: str
        """

        self._feature_influences_action_feature = feature_influences_action_feature

    @property
    def prediction_stats_action_feature(self):
        """Get the prediction_stats_action_feature of this ReactAggregateRequest.

        When calculating residuals and prediction stats, uses this target features's hyperparameters. The trainee must have been analyzed with this feature as the action feature first. If both \"prediction_stats_action_feature\" and \"action_feature\" are not provided, by default residuals and prediction stats uses \".targetless\" hyperparameters. If \"action_feature\" is provided, and this value is not provided, will default to \"action_feature\". 

        :return: The prediction_stats_action_feature of this ReactAggregateRequest.
        :rtype: str
        """
        return self._prediction_stats_action_feature

    @prediction_stats_action_feature.setter
    def prediction_stats_action_feature(self, prediction_stats_action_feature):
        """Set the prediction_stats_action_feature of this ReactAggregateRequest.

        When calculating residuals and prediction stats, uses this target features's hyperparameters. The trainee must have been analyzed with this feature as the action feature first. If both \"prediction_stats_action_feature\" and \"action_feature\" are not provided, by default residuals and prediction stats uses \".targetless\" hyperparameters. If \"action_feature\" is provided, and this value is not provided, will default to \"action_feature\". 

        :param prediction_stats_action_feature: The prediction_stats_action_feature of this ReactAggregateRequest.
        :type prediction_stats_action_feature: str
        """

        self._prediction_stats_action_feature = prediction_stats_action_feature

    @property
    def context_features(self):
        """Get the context_features of this ReactAggregateRequest.

        List of features names to use as contexts for computations. Defaults to all non-unique features if not specified. 

        :return: The context_features of this ReactAggregateRequest.
        :rtype: list[str]
        """
        return self._context_features

    @context_features.setter
    def context_features(self, context_features):
        """Set the context_features of this ReactAggregateRequest.

        List of features names to use as contexts for computations. Defaults to all non-unique features if not specified. 

        :param context_features: The context_features of this ReactAggregateRequest.
        :type context_features: list[str]
        """

        self._context_features = context_features

    @property
    def hyperparameter_param_path(self):
        """Get the hyperparameter_param_path of this ReactAggregateRequest.

        Full path for hyperparameters to use for computation. If specified for any residual computations, takes precedence over action_feature parameter. 

        :return: The hyperparameter_param_path of this ReactAggregateRequest.
        :rtype: list[str]
        """
        return self._hyperparameter_param_path

    @hyperparameter_param_path.setter
    def hyperparameter_param_path(self, hyperparameter_param_path):
        """Set the hyperparameter_param_path of this ReactAggregateRequest.

        Full path for hyperparameters to use for computation. If specified for any residual computations, takes precedence over action_feature parameter. 

        :param hyperparameter_param_path: The hyperparameter_param_path of this ReactAggregateRequest.
        :type hyperparameter_param_path: list[str]
        """

        self._hyperparameter_param_path = hyperparameter_param_path

    @property
    def num_robust_influence_samples(self):
        """Get the num_robust_influence_samples of this ReactAggregateRequest.

        Total sample size of model to use (using sampling with replacement) for robust contribution computation. Defaults to 300. 

        :return: The num_robust_influence_samples of this ReactAggregateRequest.
        :rtype: int
        """
        return self._num_robust_influence_samples

    @num_robust_influence_samples.setter
    def num_robust_influence_samples(self, num_robust_influence_samples):
        """Set the num_robust_influence_samples of this ReactAggregateRequest.

        Total sample size of model to use (using sampling with replacement) for robust contribution computation. Defaults to 300. 

        :param num_robust_influence_samples: The num_robust_influence_samples of this ReactAggregateRequest.
        :type num_robust_influence_samples: int
        """

        self._num_robust_influence_samples = num_robust_influence_samples

    @property
    def num_robust_influence_samples_per_case(self):
        """Get the num_robust_influence_samples_per_case of this ReactAggregateRequest.

        Specifies the number of robust samples to use for each case for robust contribution computations. Defaults to 300 + 2 * (number of features). 

        :return: The num_robust_influence_samples_per_case of this ReactAggregateRequest.
        :rtype: int
        """
        return self._num_robust_influence_samples_per_case

    @num_robust_influence_samples_per_case.setter
    def num_robust_influence_samples_per_case(self, num_robust_influence_samples_per_case):
        """Set the num_robust_influence_samples_per_case of this ReactAggregateRequest.

        Specifies the number of robust samples to use for each case for robust contribution computations. Defaults to 300 + 2 * (number of features). 

        :param num_robust_influence_samples_per_case: The num_robust_influence_samples_per_case of this ReactAggregateRequest.
        :type num_robust_influence_samples_per_case: int
        """

        self._num_robust_influence_samples_per_case = num_robust_influence_samples_per_case

    @property
    def num_robust_residual_samples(self):
        """Get the num_robust_residual_samples of this ReactAggregateRequest.

        Total sample size of model to use (using sampling with replacement) for robust mda and residual computation. Defaults to 1000 * (1 + log(number of features)).  Note: robust mda will be updated to use num_robust_influence_samples in a future release. 

        :return: The num_robust_residual_samples of this ReactAggregateRequest.
        :rtype: int
        """
        return self._num_robust_residual_samples

    @num_robust_residual_samples.setter
    def num_robust_residual_samples(self, num_robust_residual_samples):
        """Set the num_robust_residual_samples of this ReactAggregateRequest.

        Total sample size of model to use (using sampling with replacement) for robust mda and residual computation. Defaults to 1000 * (1 + log(number of features)).  Note: robust mda will be updated to use num_robust_influence_samples in a future release. 

        :param num_robust_residual_samples: The num_robust_residual_samples of this ReactAggregateRequest.
        :type num_robust_residual_samples: int
        """

        self._num_robust_residual_samples = num_robust_residual_samples

    @property
    def num_samples(self):
        """Get the num_samples of this ReactAggregateRequest.

        Total sample size of model to use (using sampling with replacement) for all non-robust computation. Defaults to 1000. If specified overrides sample_model_fraction. 

        :return: The num_samples of this ReactAggregateRequest.
        :rtype: int
        """
        return self._num_samples

    @num_samples.setter
    def num_samples(self, num_samples):
        """Set the num_samples of this ReactAggregateRequest.

        Total sample size of model to use (using sampling with replacement) for all non-robust computation. Defaults to 1000. If specified overrides sample_model_fraction. 

        :param num_samples: The num_samples of this ReactAggregateRequest.
        :type num_samples: int
        """

        self._num_samples = num_samples

    @property
    def robust_hyperparameters(self):
        """Get the robust_hyperparameters of this ReactAggregateRequest.

        When specified, will attempt to return residuals that were computed using hyperparameters with the specified robust or non-robust type. 

        :return: The robust_hyperparameters of this ReactAggregateRequest.
        :rtype: bool
        """
        return self._robust_hyperparameters

    @robust_hyperparameters.setter
    def robust_hyperparameters(self, robust_hyperparameters):
        """Set the robust_hyperparameters of this ReactAggregateRequest.

        When specified, will attempt to return residuals that were computed using hyperparameters with the specified robust or non-robust type. 

        :param robust_hyperparameters: The robust_hyperparameters of this ReactAggregateRequest.
        :type robust_hyperparameters: bool
        """

        self._robust_hyperparameters = robust_hyperparameters

    @property
    def sample_model_fraction(self):
        """Get the sample_model_fraction of this ReactAggregateRequest.

        A value between 0.0 - 1.0, percent of model to use in sampling (using sampling without replacement). Applicable only to non-robust computation. Ignored if num_samples is specified. Higher values provide better accuracy at the cost of compute time. 

        :return: The sample_model_fraction of this ReactAggregateRequest.
        :rtype: float
        """
        return self._sample_model_fraction

    @sample_model_fraction.setter
    def sample_model_fraction(self, sample_model_fraction):
        """Set the sample_model_fraction of this ReactAggregateRequest.

        A value between 0.0 - 1.0, percent of model to use in sampling (using sampling without replacement). Applicable only to non-robust computation. Ignored if num_samples is specified. Higher values provide better accuracy at the cost of compute time. 

        :param sample_model_fraction: The sample_model_fraction of this ReactAggregateRequest.
        :type sample_model_fraction: float
        """
        if (self.local_vars_configuration.client_side_validation and
                sample_model_fraction is not None and sample_model_fraction > 1):  # noqa: E501
            raise ValueError("Invalid value for `sample_model_fraction`, must be a value less than or equal to `1`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                sample_model_fraction is not None and sample_model_fraction < 0):  # noqa: E501
            raise ValueError("Invalid value for `sample_model_fraction`, must be a value greater than or equal to `0`")  # noqa: E501

        self._sample_model_fraction = sample_model_fraction

    @property
    def sub_model_size(self):
        """Get the sub_model_size of this ReactAggregateRequest.

        If specified will calculate residuals only on a sub model of the specified size from the full model. Applicable only to models > 1000 cases. 

        :return: The sub_model_size of this ReactAggregateRequest.
        :rtype: int
        """
        return self._sub_model_size

    @sub_model_size.setter
    def sub_model_size(self, sub_model_size):
        """Set the sub_model_size of this ReactAggregateRequest.

        If specified will calculate residuals only on a sub model of the specified size from the full model. Applicable only to models > 1000 cases. 

        :param sub_model_size: The sub_model_size of this ReactAggregateRequest.
        :type sub_model_size: int
        """

        self._sub_model_size = sub_model_size

    @property
    def confusion_matrix_min_count(self):
        """Get the confusion_matrix_min_count of this ReactAggregateRequest.

        The number of predictions a class should have (value of a cell in the matrix) for it to remain in the confusion matrix. If the count is less than this value, it will be accumulated into a single value of all insignificant predictions for the class and removed from the confusion matrix. Defaults to 10, applicable only to confusion matrices when computing residuals. 

        :return: The confusion_matrix_min_count of this ReactAggregateRequest.
        :rtype: int
        """
        return self._confusion_matrix_min_count

    @confusion_matrix_min_count.setter
    def confusion_matrix_min_count(self, confusion_matrix_min_count):
        """Set the confusion_matrix_min_count of this ReactAggregateRequest.

        The number of predictions a class should have (value of a cell in the matrix) for it to remain in the confusion matrix. If the count is less than this value, it will be accumulated into a single value of all insignificant predictions for the class and removed from the confusion matrix. Defaults to 10, applicable only to confusion matrices when computing residuals. 

        :param confusion_matrix_min_count: The confusion_matrix_min_count of this ReactAggregateRequest.
        :type confusion_matrix_min_count: int
        """

        self._confusion_matrix_min_count = confusion_matrix_min_count

    @property
    def residuals_hyperparameter_feature(self):
        """Get the residuals_hyperparameter_feature of this ReactAggregateRequest.

        When calculating residuals and prediction stats, uses this target features's hyperparameters. The trainee must have been analyzed with this feature as the action feature first. If not provided, by default residuals and prediction stats uses .targetless hyperparameters. 

        :return: The residuals_hyperparameter_feature of this ReactAggregateRequest.
        :rtype: str
        """
        return self._residuals_hyperparameter_feature

    @residuals_hyperparameter_feature.setter
    def residuals_hyperparameter_feature(self, residuals_hyperparameter_feature):
        """Set the residuals_hyperparameter_feature of this ReactAggregateRequest.

        When calculating residuals and prediction stats, uses this target features's hyperparameters. The trainee must have been analyzed with this feature as the action feature first. If not provided, by default residuals and prediction stats uses .targetless hyperparameters. 

        :param residuals_hyperparameter_feature: The residuals_hyperparameter_feature of this ReactAggregateRequest.
        :type residuals_hyperparameter_feature: str
        """

        self._residuals_hyperparameter_feature = residuals_hyperparameter_feature

    @property
    def use_case_weights(self):
        """Get the use_case_weights of this ReactAggregateRequest.

        When True, will scale influence weights by each case's weight_feature weight. If unspecified, case weights will be used if the Trainee has them. 

        :return: The use_case_weights of this ReactAggregateRequest.
        :rtype: bool
        """
        return self._use_case_weights

    @use_case_weights.setter
    def use_case_weights(self, use_case_weights):
        """Set the use_case_weights of this ReactAggregateRequest.

        When True, will scale influence weights by each case's weight_feature weight. If unspecified, case weights will be used if the Trainee has them. 

        :param use_case_weights: The use_case_weights of this ReactAggregateRequest.
        :type use_case_weights: bool
        """

        self._use_case_weights = use_case_weights

    @property
    def weight_feature(self):
        """Get the weight_feature of this ReactAggregateRequest.

        The name of the feature whose values to use as case weights. When left unspecified uses the internally managed case weight. 

        :return: The weight_feature of this ReactAggregateRequest.
        :rtype: str
        """
        return self._weight_feature

    @weight_feature.setter
    def weight_feature(self, weight_feature):
        """Set the weight_feature of this ReactAggregateRequest.

        The name of the feature whose values to use as case weights. When left unspecified uses the internally managed case weight. 

        :param weight_feature: The weight_feature of this ReactAggregateRequest.
        :type weight_feature: str
        """

        self._weight_feature = weight_feature

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
        if not isinstance(other, ReactAggregateRequest):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, ReactAggregateRequest):
            return True

        return self.to_dict() != other.to_dict()

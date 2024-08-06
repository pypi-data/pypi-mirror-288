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


class ReactDetails(object):
    """
    Auto-generated OpenAPI type.

    Returns details and audit data for a given reaction for the specified audit data flags. Local and regional models are used to determine details:     Local model -  only the most similar cases used to directly determine the prediction value, used to compute affects of cases directly                     responsible for the predicted output.     Regional model - the most similar cases to the prediction, represented by the maximum of either 30 or the local model size. Used in                     situations where relying on a small local model may produce noisy results. 
    """

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    openapi_types = {
        'influential_cases': 'bool',
        'derivation_parameters': 'bool',
        'influential_cases_familiarity_convictions': 'bool',
        'influential_cases_raw_weights': 'bool',
        'most_similar_cases': 'bool',
        'num_most_similar_cases': 'float',
        'num_most_similar_case_indices': 'float',
        'num_robust_influence_samples_per_case': 'float',
        'boundary_cases': 'bool',
        'num_boundary_cases': 'float',
        'boundary_cases_familiarity_convictions': 'bool',
        'features': 'list[str]',
        'feature_residuals_full': 'bool',
        'feature_residuals_robust': 'bool',
        'prediction_stats': 'bool',
        'feature_mda_full': 'bool',
        'feature_mda_robust': 'bool',
        'feature_mda_ex_post_full': 'bool',
        'feature_mda_ex_post_robust': 'bool',
        'feature_contributions_full': 'bool',
        'feature_contributions_robust': 'bool',
        'case_feature_contributions_full': 'bool',
        'case_feature_contributions_robust': 'bool',
        'case_feature_residuals_full': 'bool',
        'case_feature_residuals_robust': 'bool',
        'case_mda_full': 'bool',
        'case_mda_robust': 'bool',
        'case_contributions_full': 'bool',
        'case_contributions_robust': 'bool',
        'global_case_feature_residual_convictions_full': 'bool',
        'global_case_feature_residual_convictions_robust': 'bool',
        'local_case_feature_residual_convictions_full': 'bool',
        'local_case_feature_residual_convictions_robust': 'bool',
        'outlying_feature_values': 'bool',
        'categorical_action_probabilities': 'bool',
        'hypothetical_values': 'dict[str, object]',
        'distance_ratio': 'bool',
        'distance_contribution': 'bool',
        'similarity_conviction': 'bool',
        'observational_errors': 'bool',
        'generate_attempts': 'bool'
    }

    attribute_map = {
        'influential_cases': 'influential_cases',
        'derivation_parameters': 'derivation_parameters',
        'influential_cases_familiarity_convictions': 'influential_cases_familiarity_convictions',
        'influential_cases_raw_weights': 'influential_cases_raw_weights',
        'most_similar_cases': 'most_similar_cases',
        'num_most_similar_cases': 'num_most_similar_cases',
        'num_most_similar_case_indices': 'num_most_similar_case_indices',
        'num_robust_influence_samples_per_case': 'num_robust_influence_samples_per_case',
        'boundary_cases': 'boundary_cases',
        'num_boundary_cases': 'num_boundary_cases',
        'boundary_cases_familiarity_convictions': 'boundary_cases_familiarity_convictions',
        'features': 'features',
        'feature_residuals_full': 'feature_residuals_full',
        'feature_residuals_robust': 'feature_residuals_robust',
        'prediction_stats': 'prediction_stats',
        'feature_mda_full': 'feature_mda_full',
        'feature_mda_robust': 'feature_mda_robust',
        'feature_mda_ex_post_full': 'feature_mda_ex_post_full',
        'feature_mda_ex_post_robust': 'feature_mda_ex_post_robust',
        'feature_contributions_full': 'feature_contributions_full',
        'feature_contributions_robust': 'feature_contributions_robust',
        'case_feature_contributions_full': 'case_feature_contributions_full',
        'case_feature_contributions_robust': 'case_feature_contributions_robust',
        'case_feature_residuals_full': 'case_feature_residuals_full',
        'case_feature_residuals_robust': 'case_feature_residuals_robust',
        'case_mda_full': 'case_mda_full',
        'case_mda_robust': 'case_mda_robust',
        'case_contributions_full': 'case_contributions_full',
        'case_contributions_robust': 'case_contributions_robust',
        'global_case_feature_residual_convictions_full': 'global_case_feature_residual_convictions_full',
        'global_case_feature_residual_convictions_robust': 'global_case_feature_residual_convictions_robust',
        'local_case_feature_residual_convictions_full': 'local_case_feature_residual_convictions_full',
        'local_case_feature_residual_convictions_robust': 'local_case_feature_residual_convictions_robust',
        'outlying_feature_values': 'outlying_feature_values',
        'categorical_action_probabilities': 'categorical_action_probabilities',
        'hypothetical_values': 'hypothetical_values',
        'distance_ratio': 'distance_ratio',
        'distance_contribution': 'distance_contribution',
        'similarity_conviction': 'similarity_conviction',
        'observational_errors': 'observational_errors',
        'generate_attempts': 'generate_attempts'
    }

    nullable_attributes = [
    ]

    discriminator = None

    def __init__(self, influential_cases=None, derivation_parameters=None, influential_cases_familiarity_convictions=None, influential_cases_raw_weights=None, most_similar_cases=None, num_most_similar_cases=None, num_most_similar_case_indices=None, num_robust_influence_samples_per_case=None, boundary_cases=None, num_boundary_cases=None, boundary_cases_familiarity_convictions=None, features=None, feature_residuals_full=None, feature_residuals_robust=None, prediction_stats=None, feature_mda_full=None, feature_mda_robust=None, feature_mda_ex_post_full=None, feature_mda_ex_post_robust=None, feature_contributions_full=None, feature_contributions_robust=None, case_feature_contributions_full=None, case_feature_contributions_robust=None, case_feature_residuals_full=None, case_feature_residuals_robust=None, case_mda_full=None, case_mda_robust=None, case_contributions_full=None, case_contributions_robust=None, global_case_feature_residual_convictions_full=None, global_case_feature_residual_convictions_robust=None, local_case_feature_residual_convictions_full=None, local_case_feature_residual_convictions_robust=None, outlying_feature_values=None, categorical_action_probabilities=None, hypothetical_values=None, distance_ratio=None, distance_contribution=None, similarity_conviction=None, observational_errors=None, generate_attempts=None, local_vars_configuration=None):  # noqa: E501
        """ReactDetails - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default_copy()
        self.local_vars_configuration = local_vars_configuration

        self._influential_cases = None
        self._derivation_parameters = None
        self._influential_cases_familiarity_convictions = None
        self._influential_cases_raw_weights = None
        self._most_similar_cases = None
        self._num_most_similar_cases = None
        self._num_most_similar_case_indices = None
        self._num_robust_influence_samples_per_case = None
        self._boundary_cases = None
        self._num_boundary_cases = None
        self._boundary_cases_familiarity_convictions = None
        self._features = None
        self._feature_residuals_full = None
        self._feature_residuals_robust = None
        self._prediction_stats = None
        self._feature_mda_full = None
        self._feature_mda_robust = None
        self._feature_mda_ex_post_full = None
        self._feature_mda_ex_post_robust = None
        self._feature_contributions_full = None
        self._feature_contributions_robust = None
        self._case_feature_contributions_full = None
        self._case_feature_contributions_robust = None
        self._case_feature_residuals_full = None
        self._case_feature_residuals_robust = None
        self._case_mda_full = None
        self._case_mda_robust = None
        self._case_contributions_full = None
        self._case_contributions_robust = None
        self._global_case_feature_residual_convictions_full = None
        self._global_case_feature_residual_convictions_robust = None
        self._local_case_feature_residual_convictions_full = None
        self._local_case_feature_residual_convictions_robust = None
        self._outlying_feature_values = None
        self._categorical_action_probabilities = None
        self._hypothetical_values = None
        self._distance_ratio = None
        self._distance_contribution = None
        self._similarity_conviction = None
        self._observational_errors = None
        self._generate_attempts = None

        if influential_cases is not None:
            self.influential_cases = influential_cases
        if derivation_parameters is not None:
            self.derivation_parameters = derivation_parameters
        if influential_cases_familiarity_convictions is not None:
            self.influential_cases_familiarity_convictions = influential_cases_familiarity_convictions
        if influential_cases_raw_weights is not None:
            self.influential_cases_raw_weights = influential_cases_raw_weights
        if most_similar_cases is not None:
            self.most_similar_cases = most_similar_cases
        if num_most_similar_cases is not None:
            self.num_most_similar_cases = num_most_similar_cases
        if num_most_similar_case_indices is not None:
            self.num_most_similar_case_indices = num_most_similar_case_indices
        if num_robust_influence_samples_per_case is not None:
            self.num_robust_influence_samples_per_case = num_robust_influence_samples_per_case
        if boundary_cases is not None:
            self.boundary_cases = boundary_cases
        if num_boundary_cases is not None:
            self.num_boundary_cases = num_boundary_cases
        if boundary_cases_familiarity_convictions is not None:
            self.boundary_cases_familiarity_convictions = boundary_cases_familiarity_convictions
        if features is not None:
            self.features = features
        if feature_residuals_full is not None:
            self.feature_residuals_full = feature_residuals_full
        if feature_residuals_robust is not None:
            self.feature_residuals_robust = feature_residuals_robust
        if prediction_stats is not None:
            self.prediction_stats = prediction_stats
        if feature_mda_full is not None:
            self.feature_mda_full = feature_mda_full
        if feature_mda_robust is not None:
            self.feature_mda_robust = feature_mda_robust
        if feature_mda_ex_post_full is not None:
            self.feature_mda_ex_post_full = feature_mda_ex_post_full
        if feature_mda_ex_post_robust is not None:
            self.feature_mda_ex_post_robust = feature_mda_ex_post_robust
        if feature_contributions_full is not None:
            self.feature_contributions_full = feature_contributions_full
        if feature_contributions_robust is not None:
            self.feature_contributions_robust = feature_contributions_robust
        if case_feature_contributions_full is not None:
            self.case_feature_contributions_full = case_feature_contributions_full
        if case_feature_contributions_robust is not None:
            self.case_feature_contributions_robust = case_feature_contributions_robust
        if case_feature_residuals_full is not None:
            self.case_feature_residuals_full = case_feature_residuals_full
        if case_feature_residuals_robust is not None:
            self.case_feature_residuals_robust = case_feature_residuals_robust
        if case_mda_full is not None:
            self.case_mda_full = case_mda_full
        if case_mda_robust is not None:
            self.case_mda_robust = case_mda_robust
        if case_contributions_full is not None:
            self.case_contributions_full = case_contributions_full
        if case_contributions_robust is not None:
            self.case_contributions_robust = case_contributions_robust
        if global_case_feature_residual_convictions_full is not None:
            self.global_case_feature_residual_convictions_full = global_case_feature_residual_convictions_full
        if global_case_feature_residual_convictions_robust is not None:
            self.global_case_feature_residual_convictions_robust = global_case_feature_residual_convictions_robust
        if local_case_feature_residual_convictions_full is not None:
            self.local_case_feature_residual_convictions_full = local_case_feature_residual_convictions_full
        if local_case_feature_residual_convictions_robust is not None:
            self.local_case_feature_residual_convictions_robust = local_case_feature_residual_convictions_robust
        if outlying_feature_values is not None:
            self.outlying_feature_values = outlying_feature_values
        if categorical_action_probabilities is not None:
            self.categorical_action_probabilities = categorical_action_probabilities
        if hypothetical_values is not None:
            self.hypothetical_values = hypothetical_values
        if distance_ratio is not None:
            self.distance_ratio = distance_ratio
        if distance_contribution is not None:
            self.distance_contribution = distance_contribution
        if similarity_conviction is not None:
            self.similarity_conviction = similarity_conviction
        if observational_errors is not None:
            self.observational_errors = observational_errors
        if generate_attempts is not None:
            self.generate_attempts = generate_attempts

    @property
    def influential_cases(self):
        """Get the influential_cases of this ReactDetails.

        When true, outputs the most influential cases and their influence weights based on the surprisal of each case relative to the context being predicted among the cases. Uses only the context features of the reacted case. 

        :return: The influential_cases of this ReactDetails.
        :rtype: bool
        """
        return self._influential_cases

    @influential_cases.setter
    def influential_cases(self, influential_cases):
        """Set the influential_cases of this ReactDetails.

        When true, outputs the most influential cases and their influence weights based on the surprisal of each case relative to the context being predicted among the cases. Uses only the context features of the reacted case. 

        :param influential_cases: The influential_cases of this ReactDetails.
        :type influential_cases: bool
        """

        self._influential_cases = influential_cases

    @property
    def derivation_parameters(self):
        """Get the derivation_parameters of this ReactDetails.

        If True, outputs a dictionary of the parameters used in the react call. These include k, p, distance_transform, feature_weights, feature_deviations, nominal_class_counts, and use_irw. 

        :return: The derivation_parameters of this ReactDetails.
        :rtype: bool
        """
        return self._derivation_parameters

    @derivation_parameters.setter
    def derivation_parameters(self, derivation_parameters):
        """Set the derivation_parameters of this ReactDetails.

        If True, outputs a dictionary of the parameters used in the react call. These include k, p, distance_transform, feature_weights, feature_deviations, nominal_class_counts, and use_irw. 

        :param derivation_parameters: The derivation_parameters of this ReactDetails.
        :type derivation_parameters: bool
        """

        self._derivation_parameters = derivation_parameters

    @property
    def influential_cases_familiarity_convictions(self):
        """Get the influential_cases_familiarity_convictions of this ReactDetails.

        When true, outputs familiarity conviction of addition for each of the influential cases.

        :return: The influential_cases_familiarity_convictions of this ReactDetails.
        :rtype: bool
        """
        return self._influential_cases_familiarity_convictions

    @influential_cases_familiarity_convictions.setter
    def influential_cases_familiarity_convictions(self, influential_cases_familiarity_convictions):
        """Set the influential_cases_familiarity_convictions of this ReactDetails.

        When true, outputs familiarity conviction of addition for each of the influential cases.

        :param influential_cases_familiarity_convictions: The influential_cases_familiarity_convictions of this ReactDetails.
        :type influential_cases_familiarity_convictions: bool
        """

        self._influential_cases_familiarity_convictions = influential_cases_familiarity_convictions

    @property
    def influential_cases_raw_weights(self):
        """Get the influential_cases_raw_weights of this ReactDetails.

        When true, outputs the surprisal for each of the influential cases. 

        :return: The influential_cases_raw_weights of this ReactDetails.
        :rtype: bool
        """
        return self._influential_cases_raw_weights

    @influential_cases_raw_weights.setter
    def influential_cases_raw_weights(self, influential_cases_raw_weights):
        """Set the influential_cases_raw_weights of this ReactDetails.

        When true, outputs the surprisal for each of the influential cases. 

        :param influential_cases_raw_weights: The influential_cases_raw_weights of this ReactDetails.
        :type influential_cases_raw_weights: bool
        """

        self._influential_cases_raw_weights = influential_cases_raw_weights

    @property
    def most_similar_cases(self):
        """Get the most_similar_cases of this ReactDetails.

        When true, outputs an automatically determined (when 'num_most_similar_cases' is not specified) relevant number of similar cases, which will first include the influential cases. Uses only the context features of the reacted case. 

        :return: The most_similar_cases of this ReactDetails.
        :rtype: bool
        """
        return self._most_similar_cases

    @most_similar_cases.setter
    def most_similar_cases(self, most_similar_cases):
        """Set the most_similar_cases of this ReactDetails.

        When true, outputs an automatically determined (when 'num_most_similar_cases' is not specified) relevant number of similar cases, which will first include the influential cases. Uses only the context features of the reacted case. 

        :param most_similar_cases: The most_similar_cases of this ReactDetails.
        :type most_similar_cases: bool
        """

        self._most_similar_cases = most_similar_cases

    @property
    def num_most_similar_cases(self):
        """Get the num_most_similar_cases of this ReactDetails.

        When defined, outputs this manually specified number of most similar cases, which will first include the influential cases. Takes precedence over 'most_similar_cases' parameter. 

        :return: The num_most_similar_cases of this ReactDetails.
        :rtype: float
        """
        return self._num_most_similar_cases

    @num_most_similar_cases.setter
    def num_most_similar_cases(self, num_most_similar_cases):
        """Set the num_most_similar_cases of this ReactDetails.

        When defined, outputs this manually specified number of most similar cases, which will first include the influential cases. Takes precedence over 'most_similar_cases' parameter. 

        :param num_most_similar_cases: The num_most_similar_cases of this ReactDetails.
        :type num_most_similar_cases: float
        """
        if (self.local_vars_configuration.client_side_validation and
                num_most_similar_cases is not None and num_most_similar_cases > 1000):  # noqa: E501
            raise ValueError("Invalid value for `num_most_similar_cases`, must be a value less than or equal to `1000`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                num_most_similar_cases is not None and num_most_similar_cases < 1):  # noqa: E501
            raise ValueError("Invalid value for `num_most_similar_cases`, must be a value greater than or equal to `1`")  # noqa: E501

        self._num_most_similar_cases = num_most_similar_cases

    @property
    def num_most_similar_case_indices(self):
        """Get the num_most_similar_case_indices of this ReactDetails.

        When defined, outputs the specified number of most similar case indices when 'distance_ratio' is also set to true. 

        :return: The num_most_similar_case_indices of this ReactDetails.
        :rtype: float
        """
        return self._num_most_similar_case_indices

    @num_most_similar_case_indices.setter
    def num_most_similar_case_indices(self, num_most_similar_case_indices):
        """Set the num_most_similar_case_indices of this ReactDetails.

        When defined, outputs the specified number of most similar case indices when 'distance_ratio' is also set to true. 

        :param num_most_similar_case_indices: The num_most_similar_case_indices of this ReactDetails.
        :type num_most_similar_case_indices: float
        """
        if (self.local_vars_configuration.client_side_validation and
                num_most_similar_case_indices is not None and num_most_similar_case_indices > 1000):  # noqa: E501
            raise ValueError("Invalid value for `num_most_similar_case_indices`, must be a value less than or equal to `1000`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                num_most_similar_case_indices is not None and num_most_similar_case_indices < 1):  # noqa: E501
            raise ValueError("Invalid value for `num_most_similar_case_indices`, must be a value greater than or equal to `1`")  # noqa: E501

        self._num_most_similar_case_indices = num_most_similar_case_indices

    @property
    def num_robust_influence_samples_per_case(self):
        """Get the num_robust_influence_samples_per_case of this ReactDetails.

        Specifies the number of robust samples to use for each case. Applicable only for computing robust feature contributions or robust case feature contributions. Defaults to 2000 when unspecified. Higher values will take longer but provide more stable results. 

        :return: The num_robust_influence_samples_per_case of this ReactDetails.
        :rtype: float
        """
        return self._num_robust_influence_samples_per_case

    @num_robust_influence_samples_per_case.setter
    def num_robust_influence_samples_per_case(self, num_robust_influence_samples_per_case):
        """Set the num_robust_influence_samples_per_case of this ReactDetails.

        Specifies the number of robust samples to use for each case. Applicable only for computing robust feature contributions or robust case feature contributions. Defaults to 2000 when unspecified. Higher values will take longer but provide more stable results. 

        :param num_robust_influence_samples_per_case: The num_robust_influence_samples_per_case of this ReactDetails.
        :type num_robust_influence_samples_per_case: float
        """
        if (self.local_vars_configuration.client_side_validation and
                num_robust_influence_samples_per_case is not None and num_robust_influence_samples_per_case > 1000000):  # noqa: E501
            raise ValueError("Invalid value for `num_robust_influence_samples_per_case`, must be a value less than or equal to `1000000`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                num_robust_influence_samples_per_case is not None and num_robust_influence_samples_per_case < 1):  # noqa: E501
            raise ValueError("Invalid value for `num_robust_influence_samples_per_case`, must be a value greater than or equal to `1`")  # noqa: E501

        self._num_robust_influence_samples_per_case = num_robust_influence_samples_per_case

    @property
    def boundary_cases(self):
        """Get the boundary_cases of this ReactDetails.

        When true, outputs an automatically determined (when 'num_boundary_cases' is not specified) relevant number of boundary cases. Uses both context and action features of the reacted case to determine the counterfactual boundary based on action features, which maximize the dissimilarity of action features while maximizing the similarity of context features. If action features aren't specified, uses familiarity conviction to determine the boundary instead. 

        :return: The boundary_cases of this ReactDetails.
        :rtype: bool
        """
        return self._boundary_cases

    @boundary_cases.setter
    def boundary_cases(self, boundary_cases):
        """Set the boundary_cases of this ReactDetails.

        When true, outputs an automatically determined (when 'num_boundary_cases' is not specified) relevant number of boundary cases. Uses both context and action features of the reacted case to determine the counterfactual boundary based on action features, which maximize the dissimilarity of action features while maximizing the similarity of context features. If action features aren't specified, uses familiarity conviction to determine the boundary instead. 

        :param boundary_cases: The boundary_cases of this ReactDetails.
        :type boundary_cases: bool
        """

        self._boundary_cases = boundary_cases

    @property
    def num_boundary_cases(self):
        """Get the num_boundary_cases of this ReactDetails.

        When defined, outputs this manually specified number of boundary cases. Takes precedence over 'boundary_cases' parameter. 

        :return: The num_boundary_cases of this ReactDetails.
        :rtype: float
        """
        return self._num_boundary_cases

    @num_boundary_cases.setter
    def num_boundary_cases(self, num_boundary_cases):
        """Set the num_boundary_cases of this ReactDetails.

        When defined, outputs this manually specified number of boundary cases. Takes precedence over 'boundary_cases' parameter. 

        :param num_boundary_cases: The num_boundary_cases of this ReactDetails.
        :type num_boundary_cases: float
        """
        if (self.local_vars_configuration.client_side_validation and
                num_boundary_cases is not None and num_boundary_cases > 1000):  # noqa: E501
            raise ValueError("Invalid value for `num_boundary_cases`, must be a value less than or equal to `1000`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                num_boundary_cases is not None and num_boundary_cases < 1):  # noqa: E501
            raise ValueError("Invalid value for `num_boundary_cases`, must be a value greater than or equal to `1`")  # noqa: E501

        self._num_boundary_cases = num_boundary_cases

    @property
    def boundary_cases_familiarity_convictions(self):
        """Get the boundary_cases_familiarity_convictions of this ReactDetails.

        When true, outputs familiarity conviction of addition for each of the boundary cases.

        :return: The boundary_cases_familiarity_convictions of this ReactDetails.
        :rtype: bool
        """
        return self._boundary_cases_familiarity_convictions

    @boundary_cases_familiarity_convictions.setter
    def boundary_cases_familiarity_convictions(self, boundary_cases_familiarity_convictions):
        """Set the boundary_cases_familiarity_convictions of this ReactDetails.

        When true, outputs familiarity conviction of addition for each of the boundary cases.

        :param boundary_cases_familiarity_convictions: The boundary_cases_familiarity_convictions of this ReactDetails.
        :type boundary_cases_familiarity_convictions: bool
        """

        self._boundary_cases_familiarity_convictions = boundary_cases_familiarity_convictions

    @property
    def features(self):
        """Get the features of this ReactDetails.

        A list of feature names that specifies for what features will per-feature details be computed (residuals, contributions, mda, etc.). This should generally preserve compute, but will not when computing details robustly. Details will be computed for all context and action features if this is not specified. 

        :return: The features of this ReactDetails.
        :rtype: list[str]
        """
        return self._features

    @features.setter
    def features(self, features):
        """Set the features of this ReactDetails.

        A list of feature names that specifies for what features will per-feature details be computed (residuals, contributions, mda, etc.). This should generally preserve compute, but will not when computing details robustly. Details will be computed for all context and action features if this is not specified. 

        :param features: The features of this ReactDetails.
        :type features: list[str]
        """

        self._features = features

    @property
    def feature_residuals_full(self):
        """Get the feature_residuals_full of this ReactDetails.

        If True, outputs feature residuals for all (context and action) features locally around the prediction. Uses only the context features of the reacted case to determine that area. Uses full calculations, which uses leave-one-out for cases for computations. 

        :return: The feature_residuals_full of this ReactDetails.
        :rtype: bool
        """
        return self._feature_residuals_full

    @feature_residuals_full.setter
    def feature_residuals_full(self, feature_residuals_full):
        """Set the feature_residuals_full of this ReactDetails.

        If True, outputs feature residuals for all (context and action) features locally around the prediction. Uses only the context features of the reacted case to determine that area. Uses full calculations, which uses leave-one-out for cases for computations. 

        :param feature_residuals_full: The feature_residuals_full of this ReactDetails.
        :type feature_residuals_full: bool
        """

        self._feature_residuals_full = feature_residuals_full

    @property
    def feature_residuals_robust(self):
        """Get the feature_residuals_robust of this ReactDetails.

        If True, outputs feature residuals for all (context and action) features locally around the prediction. Uses only the context features of the reacted case to determine that area. Uses robust calculations, which uses uniform sampling from the power set of features as the contexts for predictions. 'selected_prediction_stats' controls the returned prediction stats. 

        :return: The feature_residuals_robust of this ReactDetails.
        :rtype: bool
        """
        return self._feature_residuals_robust

    @feature_residuals_robust.setter
    def feature_residuals_robust(self, feature_residuals_robust):
        """Set the feature_residuals_robust of this ReactDetails.

        If True, outputs feature residuals for all (context and action) features locally around the prediction. Uses only the context features of the reacted case to determine that area. Uses robust calculations, which uses uniform sampling from the power set of features as the contexts for predictions. 'selected_prediction_stats' controls the returned prediction stats. 

        :param feature_residuals_robust: The feature_residuals_robust of this ReactDetails.
        :type feature_residuals_robust: bool
        """

        self._feature_residuals_robust = feature_residuals_robust

    @property
    def prediction_stats(self):
        """Get the prediction_stats of this ReactDetails.

        When true outputs feature prediction stats for all (context and action) features locally around the prediction. The stats returned  are (\"r2\", \"rmse\", \"spearman_coeff\", \"precision\", \"recall\", \"accuracy\", \"mcc\", \"confusion_matrix\", \"missing_value_accuracy\"). Uses only the context features of the reacted case to determine that area. Uses full calculations, which uses leave-one-out context features for computations. 'selected_prediction_stats' controls the returned prediction stats. 

        :return: The prediction_stats of this ReactDetails.
        :rtype: bool
        """
        return self._prediction_stats

    @prediction_stats.setter
    def prediction_stats(self, prediction_stats):
        """Set the prediction_stats of this ReactDetails.

        When true outputs feature prediction stats for all (context and action) features locally around the prediction. The stats returned  are (\"r2\", \"rmse\", \"spearman_coeff\", \"precision\", \"recall\", \"accuracy\", \"mcc\", \"confusion_matrix\", \"missing_value_accuracy\"). Uses only the context features of the reacted case to determine that area. Uses full calculations, which uses leave-one-out context features for computations. 'selected_prediction_stats' controls the returned prediction stats. 

        :param prediction_stats: The prediction_stats of this ReactDetails.
        :type prediction_stats: bool
        """

        self._prediction_stats = prediction_stats

    @property
    def feature_mda_full(self):
        """Get the feature_mda_full of this ReactDetails.

        When True will compute Mean Decrease in Accuracy (MDA) for each context feature at predicting the action feature. Drop each feature and use the full set of remaining context features for each prediction. False removes cached values. 

        :return: The feature_mda_full of this ReactDetails.
        :rtype: bool
        """
        return self._feature_mda_full

    @feature_mda_full.setter
    def feature_mda_full(self, feature_mda_full):
        """Set the feature_mda_full of this ReactDetails.

        When True will compute Mean Decrease in Accuracy (MDA) for each context feature at predicting the action feature. Drop each feature and use the full set of remaining context features for each prediction. False removes cached values. 

        :param feature_mda_full: The feature_mda_full of this ReactDetails.
        :type feature_mda_full: bool
        """

        self._feature_mda_full = feature_mda_full

    @property
    def feature_mda_robust(self):
        """Get the feature_mda_robust of this ReactDetails.

        Compute Mean Decrease in Accuracy MDA by dropping each feature and using the robust (power set/permutations) set of remaining context features for each prediction. False removes cached values. 

        :return: The feature_mda_robust of this ReactDetails.
        :rtype: bool
        """
        return self._feature_mda_robust

    @feature_mda_robust.setter
    def feature_mda_robust(self, feature_mda_robust):
        """Set the feature_mda_robust of this ReactDetails.

        Compute Mean Decrease in Accuracy MDA by dropping each feature and using the robust (power set/permutations) set of remaining context features for each prediction. False removes cached values. 

        :param feature_mda_robust: The feature_mda_robust of this ReactDetails.
        :type feature_mda_robust: bool
        """

        self._feature_mda_robust = feature_mda_robust

    @property
    def feature_mda_ex_post_full(self):
        """Get the feature_mda_ex_post_full of this ReactDetails.

        If True, outputs each context feature's mean decrease in accuracy of predicting the action feature as an explanation detail given that the specified prediction was already made as specified by the action value. Uses both context and action features of the reacted case to determine that area. Uses full calculations, which uses leave-one-out for cases for computations. 

        :return: The feature_mda_ex_post_full of this ReactDetails.
        :rtype: bool
        """
        return self._feature_mda_ex_post_full

    @feature_mda_ex_post_full.setter
    def feature_mda_ex_post_full(self, feature_mda_ex_post_full):
        """Set the feature_mda_ex_post_full of this ReactDetails.

        If True, outputs each context feature's mean decrease in accuracy of predicting the action feature as an explanation detail given that the specified prediction was already made as specified by the action value. Uses both context and action features of the reacted case to determine that area. Uses full calculations, which uses leave-one-out for cases for computations. 

        :param feature_mda_ex_post_full: The feature_mda_ex_post_full of this ReactDetails.
        :type feature_mda_ex_post_full: bool
        """

        self._feature_mda_ex_post_full = feature_mda_ex_post_full

    @property
    def feature_mda_ex_post_robust(self):
        """Get the feature_mda_ex_post_robust of this ReactDetails.

        If True, outputs each context feature's mean decrease in accuracy of predicting the action feature as an explanation detail given that the specified prediction was already made as specified by the action value. Uses both context and action features of the reacted case to determine that area. Uses robust calculations, which uses uniform sampling from the power set of features as the contexts for predictions. 

        :return: The feature_mda_ex_post_robust of this ReactDetails.
        :rtype: bool
        """
        return self._feature_mda_ex_post_robust

    @feature_mda_ex_post_robust.setter
    def feature_mda_ex_post_robust(self, feature_mda_ex_post_robust):
        """Set the feature_mda_ex_post_robust of this ReactDetails.

        If True, outputs each context feature's mean decrease in accuracy of predicting the action feature as an explanation detail given that the specified prediction was already made as specified by the action value. Uses both context and action features of the reacted case to determine that area. Uses robust calculations, which uses uniform sampling from the power set of features as the contexts for predictions. 

        :param feature_mda_ex_post_robust: The feature_mda_ex_post_robust of this ReactDetails.
        :type feature_mda_ex_post_robust: bool
        """

        self._feature_mda_ex_post_robust = feature_mda_ex_post_robust

    @property
    def feature_contributions_full(self):
        """Get the feature_contributions_full of this ReactDetails.

        If True outputs each context feature's absolute and directional differences between the predicted action feature value and the predicted action feature value if each context were not in the model for all context features in the local model area. Uses full calculations, which uses leave-one-out for cases for computations. Directional feature contributions are returned under the key 'directional_feature_contributions_full'. 

        :return: The feature_contributions_full of this ReactDetails.
        :rtype: bool
        """
        return self._feature_contributions_full

    @feature_contributions_full.setter
    def feature_contributions_full(self, feature_contributions_full):
        """Set the feature_contributions_full of this ReactDetails.

        If True outputs each context feature's absolute and directional differences between the predicted action feature value and the predicted action feature value if each context were not in the model for all context features in the local model area. Uses full calculations, which uses leave-one-out for cases for computations. Directional feature contributions are returned under the key 'directional_feature_contributions_full'. 

        :param feature_contributions_full: The feature_contributions_full of this ReactDetails.
        :type feature_contributions_full: bool
        """

        self._feature_contributions_full = feature_contributions_full

    @property
    def feature_contributions_robust(self):
        """Get the feature_contributions_robust of this ReactDetails.

        If True outputs each context feature's absolute and directional differences between the predicted action feature value and the predicted action feature value if each context were not in the model for all context features in the local model area Uses robust calculations, which uses uniform sampling from the power set of features as the contexts for predictions. Directional feature contributions are returned under the key 'directional_feature_contributions_robust'. 

        :return: The feature_contributions_robust of this ReactDetails.
        :rtype: bool
        """
        return self._feature_contributions_robust

    @feature_contributions_robust.setter
    def feature_contributions_robust(self, feature_contributions_robust):
        """Set the feature_contributions_robust of this ReactDetails.

        If True outputs each context feature's absolute and directional differences between the predicted action feature value and the predicted action feature value if each context were not in the model for all context features in the local model area Uses robust calculations, which uses uniform sampling from the power set of features as the contexts for predictions. Directional feature contributions are returned under the key 'directional_feature_contributions_robust'. 

        :param feature_contributions_robust: The feature_contributions_robust of this ReactDetails.
        :type feature_contributions_robust: bool
        """

        self._feature_contributions_robust = feature_contributions_robust

    @property
    def case_feature_contributions_full(self):
        """Get the case_feature_contributions_full of this ReactDetails.

        If True outputs each context feature's absolute and directional differences between the predicted action feature value and the predicted action feature value if each context feature were not in the model for all context features in this case, using only the values from this specific case. Uses full calculations, which uses leave-one-out for cases for computations. Directional case feature contributions are returned under the 'case_directional_feature_contributions_full' key. 

        :return: The case_feature_contributions_full of this ReactDetails.
        :rtype: bool
        """
        return self._case_feature_contributions_full

    @case_feature_contributions_full.setter
    def case_feature_contributions_full(self, case_feature_contributions_full):
        """Set the case_feature_contributions_full of this ReactDetails.

        If True outputs each context feature's absolute and directional differences between the predicted action feature value and the predicted action feature value if each context feature were not in the model for all context features in this case, using only the values from this specific case. Uses full calculations, which uses leave-one-out for cases for computations. Directional case feature contributions are returned under the 'case_directional_feature_contributions_full' key. 

        :param case_feature_contributions_full: The case_feature_contributions_full of this ReactDetails.
        :type case_feature_contributions_full: bool
        """

        self._case_feature_contributions_full = case_feature_contributions_full

    @property
    def case_feature_contributions_robust(self):
        """Get the case_feature_contributions_robust of this ReactDetails.

        If True outputs each context feature's absolute and directional differences between the predicted action feature value and the predicted action feature value if each context feature were not in the model for all context features in this case, using only the values from this specific case. Uses robust calculations, which uses uniform sampling from the power set of features as the contexts for predictions. Directional case feature contributions are returned under the 'case_directional_feature_contributions_robust' key. 

        :return: The case_feature_contributions_robust of this ReactDetails.
        :rtype: bool
        """
        return self._case_feature_contributions_robust

    @case_feature_contributions_robust.setter
    def case_feature_contributions_robust(self, case_feature_contributions_robust):
        """Set the case_feature_contributions_robust of this ReactDetails.

        If True outputs each context feature's absolute and directional differences between the predicted action feature value and the predicted action feature value if each context feature were not in the model for all context features in this case, using only the values from this specific case. Uses robust calculations, which uses uniform sampling from the power set of features as the contexts for predictions. Directional case feature contributions are returned under the 'case_directional_feature_contributions_robust' key. 

        :param case_feature_contributions_robust: The case_feature_contributions_robust of this ReactDetails.
        :type case_feature_contributions_robust: bool
        """

        self._case_feature_contributions_robust = case_feature_contributions_robust

    @property
    def case_feature_residuals_full(self):
        """Get the case_feature_residuals_full of this ReactDetails.

        If True, outputs feature residuals for all (context and action) features for just the specified case. Uses leave-one-out for each feature, while using the others to predict the left out feature with their corresponding values from this case. Uses full calculations, which uses leave-one-out for cases for computations. 

        :return: The case_feature_residuals_full of this ReactDetails.
        :rtype: bool
        """
        return self._case_feature_residuals_full

    @case_feature_residuals_full.setter
    def case_feature_residuals_full(self, case_feature_residuals_full):
        """Set the case_feature_residuals_full of this ReactDetails.

        If True, outputs feature residuals for all (context and action) features for just the specified case. Uses leave-one-out for each feature, while using the others to predict the left out feature with their corresponding values from this case. Uses full calculations, which uses leave-one-out for cases for computations. 

        :param case_feature_residuals_full: The case_feature_residuals_full of this ReactDetails.
        :type case_feature_residuals_full: bool
        """

        self._case_feature_residuals_full = case_feature_residuals_full

    @property
    def case_feature_residuals_robust(self):
        """Get the case_feature_residuals_robust of this ReactDetails.

        If True, outputs feature residuals for all (context and action) features for just the specified case. Uses leave-one-out for each feature, while using the others to predict the left out feature with their corresponding values from this case. Uses robust calculations, which uses uniform sampling from the power set of features as the contexts for predictions. 

        :return: The case_feature_residuals_robust of this ReactDetails.
        :rtype: bool
        """
        return self._case_feature_residuals_robust

    @case_feature_residuals_robust.setter
    def case_feature_residuals_robust(self, case_feature_residuals_robust):
        """Set the case_feature_residuals_robust of this ReactDetails.

        If True, outputs feature residuals for all (context and action) features for just the specified case. Uses leave-one-out for each feature, while using the others to predict the left out feature with their corresponding values from this case. Uses robust calculations, which uses uniform sampling from the power set of features as the contexts for predictions. 

        :param case_feature_residuals_robust: The case_feature_residuals_robust of this ReactDetails.
        :type case_feature_residuals_robust: bool
        """

        self._case_feature_residuals_robust = case_feature_residuals_robust

    @property
    def case_mda_full(self):
        """Get the case_mda_full of this ReactDetails.

        If True, outputs each influential case's mean decrease in accuracy of predicting the action feature in the local model area, as if each individual case were included versus not included. Uses only the context features of the reacted case to determine that area. Uses full calculations, which uses leave-one-out for cases for computations. 

        :return: The case_mda_full of this ReactDetails.
        :rtype: bool
        """
        return self._case_mda_full

    @case_mda_full.setter
    def case_mda_full(self, case_mda_full):
        """Set the case_mda_full of this ReactDetails.

        If True, outputs each influential case's mean decrease in accuracy of predicting the action feature in the local model area, as if each individual case were included versus not included. Uses only the context features of the reacted case to determine that area. Uses full calculations, which uses leave-one-out for cases for computations. 

        :param case_mda_full: The case_mda_full of this ReactDetails.
        :type case_mda_full: bool
        """

        self._case_mda_full = case_mda_full

    @property
    def case_mda_robust(self):
        """Get the case_mda_robust of this ReactDetails.

        If True, outputs each influential case's mean decrease in accuracy of predicting the action feature in the local model area, as if each individual case were included versus not included. Uses only the context features of the reacted case to determine that area. Uses robust calculations, which uses uniform sampling from the power set of all combinations of cases. 

        :return: The case_mda_robust of this ReactDetails.
        :rtype: bool
        """
        return self._case_mda_robust

    @case_mda_robust.setter
    def case_mda_robust(self, case_mda_robust):
        """Set the case_mda_robust of this ReactDetails.

        If True, outputs each influential case's mean decrease in accuracy of predicting the action feature in the local model area, as if each individual case were included versus not included. Uses only the context features of the reacted case to determine that area. Uses robust calculations, which uses uniform sampling from the power set of all combinations of cases. 

        :param case_mda_robust: The case_mda_robust of this ReactDetails.
        :type case_mda_robust: bool
        """

        self._case_mda_robust = case_mda_robust

    @property
    def case_contributions_full(self):
        """Get the case_contributions_full of this ReactDetails.

        If true outputs each influential case's differences between the predicted action feature value and the predicted action feature value if each individual case were not included. Uses only the context features of the reacted case to determine that area. Uses full calculations, which uses leave-one-out for cases for computations. 

        :return: The case_contributions_full of this ReactDetails.
        :rtype: bool
        """
        return self._case_contributions_full

    @case_contributions_full.setter
    def case_contributions_full(self, case_contributions_full):
        """Set the case_contributions_full of this ReactDetails.

        If true outputs each influential case's differences between the predicted action feature value and the predicted action feature value if each individual case were not included. Uses only the context features of the reacted case to determine that area. Uses full calculations, which uses leave-one-out for cases for computations. 

        :param case_contributions_full: The case_contributions_full of this ReactDetails.
        :type case_contributions_full: bool
        """

        self._case_contributions_full = case_contributions_full

    @property
    def case_contributions_robust(self):
        """Get the case_contributions_robust of this ReactDetails.

        If true outputs each influential case's differences between the predicted action feature value and the predicted action feature value if each individual case were not included. Uses only the context features of the reacted case to determine that area. Uses robust calculations, which uses uniform sampling from the power set of all combinations of cases. 

        :return: The case_contributions_robust of this ReactDetails.
        :rtype: bool
        """
        return self._case_contributions_robust

    @case_contributions_robust.setter
    def case_contributions_robust(self, case_contributions_robust):
        """Set the case_contributions_robust of this ReactDetails.

        If true outputs each influential case's differences between the predicted action feature value and the predicted action feature value if each individual case were not included. Uses only the context features of the reacted case to determine that area. Uses robust calculations, which uses uniform sampling from the power set of all combinations of cases. 

        :param case_contributions_robust: The case_contributions_robust of this ReactDetails.
        :type case_contributions_robust: bool
        """

        self._case_contributions_robust = case_contributions_robust

    @property
    def global_case_feature_residual_convictions_full(self):
        """Get the global_case_feature_residual_convictions_full of this ReactDetails.

        If True, outputs this case's feature residual convictions for the global model. Computed as: global model feature residual divided by case feature residual. Uses full calculations, which uses leave-one-out for cases for computations. 

        :return: The global_case_feature_residual_convictions_full of this ReactDetails.
        :rtype: bool
        """
        return self._global_case_feature_residual_convictions_full

    @global_case_feature_residual_convictions_full.setter
    def global_case_feature_residual_convictions_full(self, global_case_feature_residual_convictions_full):
        """Set the global_case_feature_residual_convictions_full of this ReactDetails.

        If True, outputs this case's feature residual convictions for the global model. Computed as: global model feature residual divided by case feature residual. Uses full calculations, which uses leave-one-out for cases for computations. 

        :param global_case_feature_residual_convictions_full: The global_case_feature_residual_convictions_full of this ReactDetails.
        :type global_case_feature_residual_convictions_full: bool
        """

        self._global_case_feature_residual_convictions_full = global_case_feature_residual_convictions_full

    @property
    def global_case_feature_residual_convictions_robust(self):
        """Get the global_case_feature_residual_convictions_robust of this ReactDetails.

        If True, outputs this case's feature residual convictions for the global model. Computed as: global model feature residual divided by case feature residual. Uses robust calculations, which uses uniform sampling from the power set of features as the contexts for predictions. 

        :return: The global_case_feature_residual_convictions_robust of this ReactDetails.
        :rtype: bool
        """
        return self._global_case_feature_residual_convictions_robust

    @global_case_feature_residual_convictions_robust.setter
    def global_case_feature_residual_convictions_robust(self, global_case_feature_residual_convictions_robust):
        """Set the global_case_feature_residual_convictions_robust of this ReactDetails.

        If True, outputs this case's feature residual convictions for the global model. Computed as: global model feature residual divided by case feature residual. Uses robust calculations, which uses uniform sampling from the power set of features as the contexts for predictions. 

        :param global_case_feature_residual_convictions_robust: The global_case_feature_residual_convictions_robust of this ReactDetails.
        :type global_case_feature_residual_convictions_robust: bool
        """

        self._global_case_feature_residual_convictions_robust = global_case_feature_residual_convictions_robust

    @property
    def local_case_feature_residual_convictions_full(self):
        """Get the local_case_feature_residual_convictions_full of this ReactDetails.

        If True, outputs this case's feature residual convictions for the region around the prediction. Uses only the context features of the reacted case to determine that region. Computed as: region feature residual divided by case feature residual. Uses full calculations, which uses leave-one-out for cases for computations. 

        :return: The local_case_feature_residual_convictions_full of this ReactDetails.
        :rtype: bool
        """
        return self._local_case_feature_residual_convictions_full

    @local_case_feature_residual_convictions_full.setter
    def local_case_feature_residual_convictions_full(self, local_case_feature_residual_convictions_full):
        """Set the local_case_feature_residual_convictions_full of this ReactDetails.

        If True, outputs this case's feature residual convictions for the region around the prediction. Uses only the context features of the reacted case to determine that region. Computed as: region feature residual divided by case feature residual. Uses full calculations, which uses leave-one-out for cases for computations. 

        :param local_case_feature_residual_convictions_full: The local_case_feature_residual_convictions_full of this ReactDetails.
        :type local_case_feature_residual_convictions_full: bool
        """

        self._local_case_feature_residual_convictions_full = local_case_feature_residual_convictions_full

    @property
    def local_case_feature_residual_convictions_robust(self):
        """Get the local_case_feature_residual_convictions_robust of this ReactDetails.

        If True, outputs this case's feature residual convictions for the region around the prediction. Uses only the context features of the reacted case to determine that region. Computed as: region feature residual divided by case feature residual. Uses robust calculations, which uses uniform sampling from the power set of features as the contexts for predictions. 

        :return: The local_case_feature_residual_convictions_robust of this ReactDetails.
        :rtype: bool
        """
        return self._local_case_feature_residual_convictions_robust

    @local_case_feature_residual_convictions_robust.setter
    def local_case_feature_residual_convictions_robust(self, local_case_feature_residual_convictions_robust):
        """Set the local_case_feature_residual_convictions_robust of this ReactDetails.

        If True, outputs this case's feature residual convictions for the region around the prediction. Uses only the context features of the reacted case to determine that region. Computed as: region feature residual divided by case feature residual. Uses robust calculations, which uses uniform sampling from the power set of features as the contexts for predictions. 

        :param local_case_feature_residual_convictions_robust: The local_case_feature_residual_convictions_robust of this ReactDetails.
        :type local_case_feature_residual_convictions_robust: bool
        """

        self._local_case_feature_residual_convictions_robust = local_case_feature_residual_convictions_robust

    @property
    def outlying_feature_values(self):
        """Get the outlying_feature_values of this ReactDetails.

        When true, outputs the reacted case's context feature values that are outside the min or max of the corresponding feature values of all the cases in the local model area. Uses only the context features of the reacted case to determine that area. 

        :return: The outlying_feature_values of this ReactDetails.
        :rtype: bool
        """
        return self._outlying_feature_values

    @outlying_feature_values.setter
    def outlying_feature_values(self, outlying_feature_values):
        """Set the outlying_feature_values of this ReactDetails.

        When true, outputs the reacted case's context feature values that are outside the min or max of the corresponding feature values of all the cases in the local model area. Uses only the context features of the reacted case to determine that area. 

        :param outlying_feature_values: The outlying_feature_values of this ReactDetails.
        :type outlying_feature_values: bool
        """

        self._outlying_feature_values = outlying_feature_values

    @property
    def categorical_action_probabilities(self):
        """Get the categorical_action_probabilities of this ReactDetails.

        When true, outputs probabilities for each class for the action. Applicable only to categorical action features. 

        :return: The categorical_action_probabilities of this ReactDetails.
        :rtype: bool
        """
        return self._categorical_action_probabilities

    @categorical_action_probabilities.setter
    def categorical_action_probabilities(self, categorical_action_probabilities):
        """Set the categorical_action_probabilities of this ReactDetails.

        When true, outputs probabilities for each class for the action. Applicable only to categorical action features. 

        :param categorical_action_probabilities: The categorical_action_probabilities of this ReactDetails.
        :type categorical_action_probabilities: bool
        """

        self._categorical_action_probabilities = categorical_action_probabilities

    @property
    def hypothetical_values(self):
        """Get the hypothetical_values of this ReactDetails.

        A dictionary of feature name to feature value. If specified, shows how a prediction could change in a what-if scenario where the influential cases' context feature values are replaced with the specified values. Iterates over all influential cases, predicting the action features each one using the updated hypothetical values. Outputs the predicted arithmetic over the influential cases for each action feature. 

        :return: The hypothetical_values of this ReactDetails.
        :rtype: dict[str, object]
        """
        return self._hypothetical_values

    @hypothetical_values.setter
    def hypothetical_values(self, hypothetical_values):
        """Set the hypothetical_values of this ReactDetails.

        A dictionary of feature name to feature value. If specified, shows how a prediction could change in a what-if scenario where the influential cases' context feature values are replaced with the specified values. Iterates over all influential cases, predicting the action features each one using the updated hypothetical values. Outputs the predicted arithmetic over the influential cases for each action feature. 

        :param hypothetical_values: The hypothetical_values of this ReactDetails.
        :type hypothetical_values: dict[str, object]
        """

        self._hypothetical_values = hypothetical_values

    @property
    def distance_ratio(self):
        """Get the distance_ratio of this ReactDetails.

        When true, outputs the ratio of distance (relative surprisal) between this reacted case and its nearest case to the minimum distance (relative surprisal) in between the closest two cases in the local area. All distances are computed using only the specified context features. 

        :return: The distance_ratio of this ReactDetails.
        :rtype: bool
        """
        return self._distance_ratio

    @distance_ratio.setter
    def distance_ratio(self, distance_ratio):
        """Set the distance_ratio of this ReactDetails.

        When true, outputs the ratio of distance (relative surprisal) between this reacted case and its nearest case to the minimum distance (relative surprisal) in between the closest two cases in the local area. All distances are computed using only the specified context features. 

        :param distance_ratio: The distance_ratio of this ReactDetails.
        :type distance_ratio: bool
        """

        self._distance_ratio = distance_ratio

    @property
    def distance_contribution(self):
        """Get the distance_contribution of this ReactDetails.

        When true, outputs the distance contribution (expected total surprisal contribution) for the reacted case. Uses both context and action feature values. 

        :return: The distance_contribution of this ReactDetails.
        :rtype: bool
        """
        return self._distance_contribution

    @distance_contribution.setter
    def distance_contribution(self, distance_contribution):
        """Set the distance_contribution of this ReactDetails.

        When true, outputs the distance contribution (expected total surprisal contribution) for the reacted case. Uses both context and action feature values. 

        :param distance_contribution: The distance_contribution of this ReactDetails.
        :type distance_contribution: bool
        """

        self._distance_contribution = distance_contribution

    @property
    def similarity_conviction(self):
        """Get the similarity_conviction of this ReactDetails.

        When true, outputs similarity conviction for the reacted case. Uses both context and action feature values as the case values for all computations. This is defined as expected (local) distance contribution divided by reacted case distance contribution. 

        :return: The similarity_conviction of this ReactDetails.
        :rtype: bool
        """
        return self._similarity_conviction

    @similarity_conviction.setter
    def similarity_conviction(self, similarity_conviction):
        """Set the similarity_conviction of this ReactDetails.

        When true, outputs similarity conviction for the reacted case. Uses both context and action feature values as the case values for all computations. This is defined as expected (local) distance contribution divided by reacted case distance contribution. 

        :param similarity_conviction: The similarity_conviction of this ReactDetails.
        :type similarity_conviction: bool
        """

        self._similarity_conviction = similarity_conviction

    @property
    def observational_errors(self):
        """Get the observational_errors of this ReactDetails.

        When true, outputs observational errors for all features as defined in feature attributes. 

        :return: The observational_errors of this ReactDetails.
        :rtype: bool
        """
        return self._observational_errors

    @observational_errors.setter
    def observational_errors(self, observational_errors):
        """Set the observational_errors of this ReactDetails.

        When true, outputs observational errors for all features as defined in feature attributes. 

        :param observational_errors: The observational_errors of this ReactDetails.
        :type observational_errors: bool
        """

        self._observational_errors = observational_errors

    @property
    def generate_attempts(self):
        """Get the generate_attempts of this ReactDetails.

        When true, outputs the number of attempts taken to generate each case. Only applicable when 'generate_new_cases' is \"always\" or \"attempt\". When used in react_series, \"series_generate_attempts\" is also returned. 

        :return: The generate_attempts of this ReactDetails.
        :rtype: bool
        """
        return self._generate_attempts

    @generate_attempts.setter
    def generate_attempts(self, generate_attempts):
        """Set the generate_attempts of this ReactDetails.

        When true, outputs the number of attempts taken to generate each case. Only applicable when 'generate_new_cases' is \"always\" or \"attempt\". When used in react_series, \"series_generate_attempts\" is also returned. 

        :param generate_attempts: The generate_attempts of this ReactDetails.
        :type generate_attempts: bool
        """

        self._generate_attempts = generate_attempts

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
        if not isinstance(other, ReactDetails):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, ReactDetails):
            return True

        return self.to_dict() != other.to_dict()

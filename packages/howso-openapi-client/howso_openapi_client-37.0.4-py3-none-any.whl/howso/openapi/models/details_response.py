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


class DetailsResponse(object):
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
        'boundary_cases': 'list[list[object]]',
        'categorical_action_probabilities': 'list[dict[str, object]]',
        'derivation_parameters': 'list[DerivationParameters]',
        'feature_residuals_full': 'list[dict[str, object]]',
        'feature_residuals_robust': 'list[dict[str, object]]',
        'prediction_stats': 'list[dict[str, object]]',
        'outlying_feature_values': 'list[dict[str, DetailsResponseOutlyingFeatureValuesInnerValue]]',
        'influential_cases': 'list[list[object]]',
        'most_similar_cases': 'list[list[object]]',
        'observational_errors': 'list[dict[str, float]]',
        'feature_mda_full': 'list[dict[str, float]]',
        'feature_mda_robust': 'list[dict[str, float]]',
        'feature_mda_ex_post_full': 'list[dict[str, float]]',
        'feature_mda_ex_post_robust': 'list[dict[str, float]]',
        'directional_feature_contributions_full': 'list[dict[str, float]]',
        'directional_feature_contributions_robust': 'list[dict[str, float]]',
        'feature_contributions_full': 'list[dict[str, float]]',
        'feature_contributions_robust': 'list[dict[str, float]]',
        'case_directional_feature_contributions_full': 'list[dict[str, float]]',
        'case_directional_feature_contributions_robust': 'list[dict[str, float]]',
        'case_feature_contributions_full': 'list[dict[str, float]]',
        'case_feature_contributions_robust': 'list[dict[str, float]]',
        'case_mda_full': 'list[list[dict[str, object]]]',
        'case_mda_robust': 'list[list[dict[str, object]]]',
        'case_contributions_full': 'list[list[dict[str, object]]]',
        'case_contributions_robust': 'list[list[dict[str, object]]]',
        'case_feature_residuals_full': 'list[dict[str, float]]',
        'case_feature_residuals_robust': 'list[dict[str, float]]',
        'local_case_feature_residual_convictions_full': 'list[dict[str, float]]',
        'local_case_feature_residual_convictions_robust': 'list[dict[str, float]]',
        'global_case_feature_residual_convictions_full': 'list[dict[str, float]]',
        'global_case_feature_residual_convictions_robust': 'list[dict[str, float]]',
        'hypothetical_values': 'list[dict[str, object]]',
        'distance_ratio': 'list[float]',
        'distance_ratio_parts': 'list[DetailsResponseDistanceRatioPartsInner]',
        'distance_contribution': 'list[float]',
        'similarity_conviction': 'list[float]',
        'most_similar_case_indices': 'list[list[dict[str, object]]]',
        'generate_attempts': 'list[float]',
        'series_generate_attempts': 'list[list[float]]'
    }

    attribute_map = {
        'boundary_cases': 'boundary_cases',
        'categorical_action_probabilities': 'categorical_action_probabilities',
        'derivation_parameters': 'derivation_parameters',
        'feature_residuals_full': 'feature_residuals_full',
        'feature_residuals_robust': 'feature_residuals_robust',
        'prediction_stats': 'prediction_stats',
        'outlying_feature_values': 'outlying_feature_values',
        'influential_cases': 'influential_cases',
        'most_similar_cases': 'most_similar_cases',
        'observational_errors': 'observational_errors',
        'feature_mda_full': 'feature_mda_full',
        'feature_mda_robust': 'feature_mda_robust',
        'feature_mda_ex_post_full': 'feature_mda_ex_post_full',
        'feature_mda_ex_post_robust': 'feature_mda_ex_post_robust',
        'directional_feature_contributions_full': 'directional_feature_contributions_full',
        'directional_feature_contributions_robust': 'directional_feature_contributions_robust',
        'feature_contributions_full': 'feature_contributions_full',
        'feature_contributions_robust': 'feature_contributions_robust',
        'case_directional_feature_contributions_full': 'case_directional_feature_contributions_full',
        'case_directional_feature_contributions_robust': 'case_directional_feature_contributions_robust',
        'case_feature_contributions_full': 'case_feature_contributions_full',
        'case_feature_contributions_robust': 'case_feature_contributions_robust',
        'case_mda_full': 'case_mda_full',
        'case_mda_robust': 'case_mda_robust',
        'case_contributions_full': 'case_contributions_full',
        'case_contributions_robust': 'case_contributions_robust',
        'case_feature_residuals_full': 'case_feature_residuals_full',
        'case_feature_residuals_robust': 'case_feature_residuals_robust',
        'local_case_feature_residual_convictions_full': 'local_case_feature_residual_convictions_full',
        'local_case_feature_residual_convictions_robust': 'local_case_feature_residual_convictions_robust',
        'global_case_feature_residual_convictions_full': 'global_case_feature_residual_convictions_full',
        'global_case_feature_residual_convictions_robust': 'global_case_feature_residual_convictions_robust',
        'hypothetical_values': 'hypothetical_values',
        'distance_ratio': 'distance_ratio',
        'distance_ratio_parts': 'distance_ratio_parts',
        'distance_contribution': 'distance_contribution',
        'similarity_conviction': 'similarity_conviction',
        'most_similar_case_indices': 'most_similar_case_indices',
        'generate_attempts': 'generate_attempts',
        'series_generate_attempts': 'series_generate_attempts'
    }

    nullable_attributes = [
    ]

    discriminator = None

    def __init__(self, boundary_cases=None, categorical_action_probabilities=None, derivation_parameters=None, feature_residuals_full=None, feature_residuals_robust=None, prediction_stats=None, outlying_feature_values=None, influential_cases=None, most_similar_cases=None, observational_errors=None, feature_mda_full=None, feature_mda_robust=None, feature_mda_ex_post_full=None, feature_mda_ex_post_robust=None, directional_feature_contributions_full=None, directional_feature_contributions_robust=None, feature_contributions_full=None, feature_contributions_robust=None, case_directional_feature_contributions_full=None, case_directional_feature_contributions_robust=None, case_feature_contributions_full=None, case_feature_contributions_robust=None, case_mda_full=None, case_mda_robust=None, case_contributions_full=None, case_contributions_robust=None, case_feature_residuals_full=None, case_feature_residuals_robust=None, local_case_feature_residual_convictions_full=None, local_case_feature_residual_convictions_robust=None, global_case_feature_residual_convictions_full=None, global_case_feature_residual_convictions_robust=None, hypothetical_values=None, distance_ratio=None, distance_ratio_parts=None, distance_contribution=None, similarity_conviction=None, most_similar_case_indices=None, generate_attempts=None, series_generate_attempts=None, local_vars_configuration=None):  # noqa: E501
        """DetailsResponse - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default_copy()
        self.local_vars_configuration = local_vars_configuration

        self._boundary_cases = None
        self._categorical_action_probabilities = None
        self._derivation_parameters = None
        self._feature_residuals_full = None
        self._feature_residuals_robust = None
        self._prediction_stats = None
        self._outlying_feature_values = None
        self._influential_cases = None
        self._most_similar_cases = None
        self._observational_errors = None
        self._feature_mda_full = None
        self._feature_mda_robust = None
        self._feature_mda_ex_post_full = None
        self._feature_mda_ex_post_robust = None
        self._directional_feature_contributions_full = None
        self._directional_feature_contributions_robust = None
        self._feature_contributions_full = None
        self._feature_contributions_robust = None
        self._case_directional_feature_contributions_full = None
        self._case_directional_feature_contributions_robust = None
        self._case_feature_contributions_full = None
        self._case_feature_contributions_robust = None
        self._case_mda_full = None
        self._case_mda_robust = None
        self._case_contributions_full = None
        self._case_contributions_robust = None
        self._case_feature_residuals_full = None
        self._case_feature_residuals_robust = None
        self._local_case_feature_residual_convictions_full = None
        self._local_case_feature_residual_convictions_robust = None
        self._global_case_feature_residual_convictions_full = None
        self._global_case_feature_residual_convictions_robust = None
        self._hypothetical_values = None
        self._distance_ratio = None
        self._distance_ratio_parts = None
        self._distance_contribution = None
        self._similarity_conviction = None
        self._most_similar_case_indices = None
        self._generate_attempts = None
        self._series_generate_attempts = None

        if boundary_cases is not None:
            self.boundary_cases = boundary_cases
        if categorical_action_probabilities is not None:
            self.categorical_action_probabilities = categorical_action_probabilities
        if derivation_parameters is not None:
            self.derivation_parameters = derivation_parameters
        if feature_residuals_full is not None:
            self.feature_residuals_full = feature_residuals_full
        if feature_residuals_robust is not None:
            self.feature_residuals_robust = feature_residuals_robust
        if prediction_stats is not None:
            self.prediction_stats = prediction_stats
        if outlying_feature_values is not None:
            self.outlying_feature_values = outlying_feature_values
        if influential_cases is not None:
            self.influential_cases = influential_cases
        if most_similar_cases is not None:
            self.most_similar_cases = most_similar_cases
        if observational_errors is not None:
            self.observational_errors = observational_errors
        if feature_mda_full is not None:
            self.feature_mda_full = feature_mda_full
        if feature_mda_robust is not None:
            self.feature_mda_robust = feature_mda_robust
        if feature_mda_ex_post_full is not None:
            self.feature_mda_ex_post_full = feature_mda_ex_post_full
        if feature_mda_ex_post_robust is not None:
            self.feature_mda_ex_post_robust = feature_mda_ex_post_robust
        if directional_feature_contributions_full is not None:
            self.directional_feature_contributions_full = directional_feature_contributions_full
        if directional_feature_contributions_robust is not None:
            self.directional_feature_contributions_robust = directional_feature_contributions_robust
        if feature_contributions_full is not None:
            self.feature_contributions_full = feature_contributions_full
        if feature_contributions_robust is not None:
            self.feature_contributions_robust = feature_contributions_robust
        if case_directional_feature_contributions_full is not None:
            self.case_directional_feature_contributions_full = case_directional_feature_contributions_full
        if case_directional_feature_contributions_robust is not None:
            self.case_directional_feature_contributions_robust = case_directional_feature_contributions_robust
        if case_feature_contributions_full is not None:
            self.case_feature_contributions_full = case_feature_contributions_full
        if case_feature_contributions_robust is not None:
            self.case_feature_contributions_robust = case_feature_contributions_robust
        if case_mda_full is not None:
            self.case_mda_full = case_mda_full
        if case_mda_robust is not None:
            self.case_mda_robust = case_mda_robust
        if case_contributions_full is not None:
            self.case_contributions_full = case_contributions_full
        if case_contributions_robust is not None:
            self.case_contributions_robust = case_contributions_robust
        if case_feature_residuals_full is not None:
            self.case_feature_residuals_full = case_feature_residuals_full
        if case_feature_residuals_robust is not None:
            self.case_feature_residuals_robust = case_feature_residuals_robust
        if local_case_feature_residual_convictions_full is not None:
            self.local_case_feature_residual_convictions_full = local_case_feature_residual_convictions_full
        if local_case_feature_residual_convictions_robust is not None:
            self.local_case_feature_residual_convictions_robust = local_case_feature_residual_convictions_robust
        if global_case_feature_residual_convictions_full is not None:
            self.global_case_feature_residual_convictions_full = global_case_feature_residual_convictions_full
        if global_case_feature_residual_convictions_robust is not None:
            self.global_case_feature_residual_convictions_robust = global_case_feature_residual_convictions_robust
        if hypothetical_values is not None:
            self.hypothetical_values = hypothetical_values
        if distance_ratio is not None:
            self.distance_ratio = distance_ratio
        if distance_ratio_parts is not None:
            self.distance_ratio_parts = distance_ratio_parts
        if distance_contribution is not None:
            self.distance_contribution = distance_contribution
        if similarity_conviction is not None:
            self.similarity_conviction = similarity_conviction
        if most_similar_case_indices is not None:
            self.most_similar_case_indices = most_similar_case_indices
        if generate_attempts is not None:
            self.generate_attempts = generate_attempts
        if series_generate_attempts is not None:
            self.series_generate_attempts = series_generate_attempts

    @property
    def boundary_cases(self):
        """Get the boundary_cases of this DetailsResponse.


        :return: The boundary_cases of this DetailsResponse.
        :rtype: list[list[object]]
        """
        return self._boundary_cases

    @boundary_cases.setter
    def boundary_cases(self, boundary_cases):
        """Set the boundary_cases of this DetailsResponse.


        :param boundary_cases: The boundary_cases of this DetailsResponse.
        :type boundary_cases: list[list[object]]
        """

        self._boundary_cases = boundary_cases

    @property
    def categorical_action_probabilities(self):
        """Get the categorical_action_probabilities of this DetailsResponse.


        :return: The categorical_action_probabilities of this DetailsResponse.
        :rtype: list[dict[str, object]]
        """
        return self._categorical_action_probabilities

    @categorical_action_probabilities.setter
    def categorical_action_probabilities(self, categorical_action_probabilities):
        """Set the categorical_action_probabilities of this DetailsResponse.


        :param categorical_action_probabilities: The categorical_action_probabilities of this DetailsResponse.
        :type categorical_action_probabilities: list[dict[str, object]]
        """

        self._categorical_action_probabilities = categorical_action_probabilities

    @property
    def derivation_parameters(self):
        """Get the derivation_parameters of this DetailsResponse.


        :return: The derivation_parameters of this DetailsResponse.
        :rtype: list[DerivationParameters]
        """
        return self._derivation_parameters

    @derivation_parameters.setter
    def derivation_parameters(self, derivation_parameters):
        """Set the derivation_parameters of this DetailsResponse.


        :param derivation_parameters: The derivation_parameters of this DetailsResponse.
        :type derivation_parameters: list[DerivationParameters]
        """

        self._derivation_parameters = derivation_parameters

    @property
    def feature_residuals_full(self):
        """Get the feature_residuals_full of this DetailsResponse.


        :return: The feature_residuals_full of this DetailsResponse.
        :rtype: list[dict[str, object]]
        """
        return self._feature_residuals_full

    @feature_residuals_full.setter
    def feature_residuals_full(self, feature_residuals_full):
        """Set the feature_residuals_full of this DetailsResponse.


        :param feature_residuals_full: The feature_residuals_full of this DetailsResponse.
        :type feature_residuals_full: list[dict[str, object]]
        """

        self._feature_residuals_full = feature_residuals_full

    @property
    def feature_residuals_robust(self):
        """Get the feature_residuals_robust of this DetailsResponse.


        :return: The feature_residuals_robust of this DetailsResponse.
        :rtype: list[dict[str, object]]
        """
        return self._feature_residuals_robust

    @feature_residuals_robust.setter
    def feature_residuals_robust(self, feature_residuals_robust):
        """Set the feature_residuals_robust of this DetailsResponse.


        :param feature_residuals_robust: The feature_residuals_robust of this DetailsResponse.
        :type feature_residuals_robust: list[dict[str, object]]
        """

        self._feature_residuals_robust = feature_residuals_robust

    @property
    def prediction_stats(self):
        """Get the prediction_stats of this DetailsResponse.


        :return: The prediction_stats of this DetailsResponse.
        :rtype: list[dict[str, object]]
        """
        return self._prediction_stats

    @prediction_stats.setter
    def prediction_stats(self, prediction_stats):
        """Set the prediction_stats of this DetailsResponse.


        :param prediction_stats: The prediction_stats of this DetailsResponse.
        :type prediction_stats: list[dict[str, object]]
        """

        self._prediction_stats = prediction_stats

    @property
    def outlying_feature_values(self):
        """Get the outlying_feature_values of this DetailsResponse.


        :return: The outlying_feature_values of this DetailsResponse.
        :rtype: list[dict[str, DetailsResponseOutlyingFeatureValuesInnerValue]]
        """
        return self._outlying_feature_values

    @outlying_feature_values.setter
    def outlying_feature_values(self, outlying_feature_values):
        """Set the outlying_feature_values of this DetailsResponse.


        :param outlying_feature_values: The outlying_feature_values of this DetailsResponse.
        :type outlying_feature_values: list[dict[str, DetailsResponseOutlyingFeatureValuesInnerValue]]
        """

        self._outlying_feature_values = outlying_feature_values

    @property
    def influential_cases(self):
        """Get the influential_cases of this DetailsResponse.


        :return: The influential_cases of this DetailsResponse.
        :rtype: list[list[object]]
        """
        return self._influential_cases

    @influential_cases.setter
    def influential_cases(self, influential_cases):
        """Set the influential_cases of this DetailsResponse.


        :param influential_cases: The influential_cases of this DetailsResponse.
        :type influential_cases: list[list[object]]
        """

        self._influential_cases = influential_cases

    @property
    def most_similar_cases(self):
        """Get the most_similar_cases of this DetailsResponse.


        :return: The most_similar_cases of this DetailsResponse.
        :rtype: list[list[object]]
        """
        return self._most_similar_cases

    @most_similar_cases.setter
    def most_similar_cases(self, most_similar_cases):
        """Set the most_similar_cases of this DetailsResponse.


        :param most_similar_cases: The most_similar_cases of this DetailsResponse.
        :type most_similar_cases: list[list[object]]
        """

        self._most_similar_cases = most_similar_cases

    @property
    def observational_errors(self):
        """Get the observational_errors of this DetailsResponse.

        Observational errors for all features as defined in feature attributes.

        :return: The observational_errors of this DetailsResponse.
        :rtype: list[dict[str, float]]
        """
        return self._observational_errors

    @observational_errors.setter
    def observational_errors(self, observational_errors):
        """Set the observational_errors of this DetailsResponse.

        Observational errors for all features as defined in feature attributes.

        :param observational_errors: The observational_errors of this DetailsResponse.
        :type observational_errors: list[dict[str, float]]
        """

        self._observational_errors = observational_errors

    @property
    def feature_mda_full(self):
        """Get the feature_mda_full of this DetailsResponse.


        :return: The feature_mda_full of this DetailsResponse.
        :rtype: list[dict[str, float]]
        """
        return self._feature_mda_full

    @feature_mda_full.setter
    def feature_mda_full(self, feature_mda_full):
        """Set the feature_mda_full of this DetailsResponse.


        :param feature_mda_full: The feature_mda_full of this DetailsResponse.
        :type feature_mda_full: list[dict[str, float]]
        """

        self._feature_mda_full = feature_mda_full

    @property
    def feature_mda_robust(self):
        """Get the feature_mda_robust of this DetailsResponse.


        :return: The feature_mda_robust of this DetailsResponse.
        :rtype: list[dict[str, float]]
        """
        return self._feature_mda_robust

    @feature_mda_robust.setter
    def feature_mda_robust(self, feature_mda_robust):
        """Set the feature_mda_robust of this DetailsResponse.


        :param feature_mda_robust: The feature_mda_robust of this DetailsResponse.
        :type feature_mda_robust: list[dict[str, float]]
        """

        self._feature_mda_robust = feature_mda_robust

    @property
    def feature_mda_ex_post_full(self):
        """Get the feature_mda_ex_post_full of this DetailsResponse.


        :return: The feature_mda_ex_post_full of this DetailsResponse.
        :rtype: list[dict[str, float]]
        """
        return self._feature_mda_ex_post_full

    @feature_mda_ex_post_full.setter
    def feature_mda_ex_post_full(self, feature_mda_ex_post_full):
        """Set the feature_mda_ex_post_full of this DetailsResponse.


        :param feature_mda_ex_post_full: The feature_mda_ex_post_full of this DetailsResponse.
        :type feature_mda_ex_post_full: list[dict[str, float]]
        """

        self._feature_mda_ex_post_full = feature_mda_ex_post_full

    @property
    def feature_mda_ex_post_robust(self):
        """Get the feature_mda_ex_post_robust of this DetailsResponse.


        :return: The feature_mda_ex_post_robust of this DetailsResponse.
        :rtype: list[dict[str, float]]
        """
        return self._feature_mda_ex_post_robust

    @feature_mda_ex_post_robust.setter
    def feature_mda_ex_post_robust(self, feature_mda_ex_post_robust):
        """Set the feature_mda_ex_post_robust of this DetailsResponse.


        :param feature_mda_ex_post_robust: The feature_mda_ex_post_robust of this DetailsResponse.
        :type feature_mda_ex_post_robust: list[dict[str, float]]
        """

        self._feature_mda_ex_post_robust = feature_mda_ex_post_robust

    @property
    def directional_feature_contributions_full(self):
        """Get the directional_feature_contributions_full of this DetailsResponse.


        :return: The directional_feature_contributions_full of this DetailsResponse.
        :rtype: list[dict[str, float]]
        """
        return self._directional_feature_contributions_full

    @directional_feature_contributions_full.setter
    def directional_feature_contributions_full(self, directional_feature_contributions_full):
        """Set the directional_feature_contributions_full of this DetailsResponse.


        :param directional_feature_contributions_full: The directional_feature_contributions_full of this DetailsResponse.
        :type directional_feature_contributions_full: list[dict[str, float]]
        """

        self._directional_feature_contributions_full = directional_feature_contributions_full

    @property
    def directional_feature_contributions_robust(self):
        """Get the directional_feature_contributions_robust of this DetailsResponse.


        :return: The directional_feature_contributions_robust of this DetailsResponse.
        :rtype: list[dict[str, float]]
        """
        return self._directional_feature_contributions_robust

    @directional_feature_contributions_robust.setter
    def directional_feature_contributions_robust(self, directional_feature_contributions_robust):
        """Set the directional_feature_contributions_robust of this DetailsResponse.


        :param directional_feature_contributions_robust: The directional_feature_contributions_robust of this DetailsResponse.
        :type directional_feature_contributions_robust: list[dict[str, float]]
        """

        self._directional_feature_contributions_robust = directional_feature_contributions_robust

    @property
    def feature_contributions_full(self):
        """Get the feature_contributions_full of this DetailsResponse.


        :return: The feature_contributions_full of this DetailsResponse.
        :rtype: list[dict[str, float]]
        """
        return self._feature_contributions_full

    @feature_contributions_full.setter
    def feature_contributions_full(self, feature_contributions_full):
        """Set the feature_contributions_full of this DetailsResponse.


        :param feature_contributions_full: The feature_contributions_full of this DetailsResponse.
        :type feature_contributions_full: list[dict[str, float]]
        """

        self._feature_contributions_full = feature_contributions_full

    @property
    def feature_contributions_robust(self):
        """Get the feature_contributions_robust of this DetailsResponse.


        :return: The feature_contributions_robust of this DetailsResponse.
        :rtype: list[dict[str, float]]
        """
        return self._feature_contributions_robust

    @feature_contributions_robust.setter
    def feature_contributions_robust(self, feature_contributions_robust):
        """Set the feature_contributions_robust of this DetailsResponse.


        :param feature_contributions_robust: The feature_contributions_robust of this DetailsResponse.
        :type feature_contributions_robust: list[dict[str, float]]
        """

        self._feature_contributions_robust = feature_contributions_robust

    @property
    def case_directional_feature_contributions_full(self):
        """Get the case_directional_feature_contributions_full of this DetailsResponse.


        :return: The case_directional_feature_contributions_full of this DetailsResponse.
        :rtype: list[dict[str, float]]
        """
        return self._case_directional_feature_contributions_full

    @case_directional_feature_contributions_full.setter
    def case_directional_feature_contributions_full(self, case_directional_feature_contributions_full):
        """Set the case_directional_feature_contributions_full of this DetailsResponse.


        :param case_directional_feature_contributions_full: The case_directional_feature_contributions_full of this DetailsResponse.
        :type case_directional_feature_contributions_full: list[dict[str, float]]
        """

        self._case_directional_feature_contributions_full = case_directional_feature_contributions_full

    @property
    def case_directional_feature_contributions_robust(self):
        """Get the case_directional_feature_contributions_robust of this DetailsResponse.


        :return: The case_directional_feature_contributions_robust of this DetailsResponse.
        :rtype: list[dict[str, float]]
        """
        return self._case_directional_feature_contributions_robust

    @case_directional_feature_contributions_robust.setter
    def case_directional_feature_contributions_robust(self, case_directional_feature_contributions_robust):
        """Set the case_directional_feature_contributions_robust of this DetailsResponse.


        :param case_directional_feature_contributions_robust: The case_directional_feature_contributions_robust of this DetailsResponse.
        :type case_directional_feature_contributions_robust: list[dict[str, float]]
        """

        self._case_directional_feature_contributions_robust = case_directional_feature_contributions_robust

    @property
    def case_feature_contributions_full(self):
        """Get the case_feature_contributions_full of this DetailsResponse.


        :return: The case_feature_contributions_full of this DetailsResponse.
        :rtype: list[dict[str, float]]
        """
        return self._case_feature_contributions_full

    @case_feature_contributions_full.setter
    def case_feature_contributions_full(self, case_feature_contributions_full):
        """Set the case_feature_contributions_full of this DetailsResponse.


        :param case_feature_contributions_full: The case_feature_contributions_full of this DetailsResponse.
        :type case_feature_contributions_full: list[dict[str, float]]
        """

        self._case_feature_contributions_full = case_feature_contributions_full

    @property
    def case_feature_contributions_robust(self):
        """Get the case_feature_contributions_robust of this DetailsResponse.


        :return: The case_feature_contributions_robust of this DetailsResponse.
        :rtype: list[dict[str, float]]
        """
        return self._case_feature_contributions_robust

    @case_feature_contributions_robust.setter
    def case_feature_contributions_robust(self, case_feature_contributions_robust):
        """Set the case_feature_contributions_robust of this DetailsResponse.


        :param case_feature_contributions_robust: The case_feature_contributions_robust of this DetailsResponse.
        :type case_feature_contributions_robust: list[dict[str, float]]
        """

        self._case_feature_contributions_robust = case_feature_contributions_robust

    @property
    def case_mda_full(self):
        """Get the case_mda_full of this DetailsResponse.


        :return: The case_mda_full of this DetailsResponse.
        :rtype: list[list[dict[str, object]]]
        """
        return self._case_mda_full

    @case_mda_full.setter
    def case_mda_full(self, case_mda_full):
        """Set the case_mda_full of this DetailsResponse.


        :param case_mda_full: The case_mda_full of this DetailsResponse.
        :type case_mda_full: list[list[dict[str, object]]]
        """

        self._case_mda_full = case_mda_full

    @property
    def case_mda_robust(self):
        """Get the case_mda_robust of this DetailsResponse.


        :return: The case_mda_robust of this DetailsResponse.
        :rtype: list[list[dict[str, object]]]
        """
        return self._case_mda_robust

    @case_mda_robust.setter
    def case_mda_robust(self, case_mda_robust):
        """Set the case_mda_robust of this DetailsResponse.


        :param case_mda_robust: The case_mda_robust of this DetailsResponse.
        :type case_mda_robust: list[list[dict[str, object]]]
        """

        self._case_mda_robust = case_mda_robust

    @property
    def case_contributions_full(self):
        """Get the case_contributions_full of this DetailsResponse.


        :return: The case_contributions_full of this DetailsResponse.
        :rtype: list[list[dict[str, object]]]
        """
        return self._case_contributions_full

    @case_contributions_full.setter
    def case_contributions_full(self, case_contributions_full):
        """Set the case_contributions_full of this DetailsResponse.


        :param case_contributions_full: The case_contributions_full of this DetailsResponse.
        :type case_contributions_full: list[list[dict[str, object]]]
        """

        self._case_contributions_full = case_contributions_full

    @property
    def case_contributions_robust(self):
        """Get the case_contributions_robust of this DetailsResponse.


        :return: The case_contributions_robust of this DetailsResponse.
        :rtype: list[list[dict[str, object]]]
        """
        return self._case_contributions_robust

    @case_contributions_robust.setter
    def case_contributions_robust(self, case_contributions_robust):
        """Set the case_contributions_robust of this DetailsResponse.


        :param case_contributions_robust: The case_contributions_robust of this DetailsResponse.
        :type case_contributions_robust: list[list[dict[str, object]]]
        """

        self._case_contributions_robust = case_contributions_robust

    @property
    def case_feature_residuals_full(self):
        """Get the case_feature_residuals_full of this DetailsResponse.


        :return: The case_feature_residuals_full of this DetailsResponse.
        :rtype: list[dict[str, float]]
        """
        return self._case_feature_residuals_full

    @case_feature_residuals_full.setter
    def case_feature_residuals_full(self, case_feature_residuals_full):
        """Set the case_feature_residuals_full of this DetailsResponse.


        :param case_feature_residuals_full: The case_feature_residuals_full of this DetailsResponse.
        :type case_feature_residuals_full: list[dict[str, float]]
        """

        self._case_feature_residuals_full = case_feature_residuals_full

    @property
    def case_feature_residuals_robust(self):
        """Get the case_feature_residuals_robust of this DetailsResponse.


        :return: The case_feature_residuals_robust of this DetailsResponse.
        :rtype: list[dict[str, float]]
        """
        return self._case_feature_residuals_robust

    @case_feature_residuals_robust.setter
    def case_feature_residuals_robust(self, case_feature_residuals_robust):
        """Set the case_feature_residuals_robust of this DetailsResponse.


        :param case_feature_residuals_robust: The case_feature_residuals_robust of this DetailsResponse.
        :type case_feature_residuals_robust: list[dict[str, float]]
        """

        self._case_feature_residuals_robust = case_feature_residuals_robust

    @property
    def local_case_feature_residual_convictions_full(self):
        """Get the local_case_feature_residual_convictions_full of this DetailsResponse.


        :return: The local_case_feature_residual_convictions_full of this DetailsResponse.
        :rtype: list[dict[str, float]]
        """
        return self._local_case_feature_residual_convictions_full

    @local_case_feature_residual_convictions_full.setter
    def local_case_feature_residual_convictions_full(self, local_case_feature_residual_convictions_full):
        """Set the local_case_feature_residual_convictions_full of this DetailsResponse.


        :param local_case_feature_residual_convictions_full: The local_case_feature_residual_convictions_full of this DetailsResponse.
        :type local_case_feature_residual_convictions_full: list[dict[str, float]]
        """

        self._local_case_feature_residual_convictions_full = local_case_feature_residual_convictions_full

    @property
    def local_case_feature_residual_convictions_robust(self):
        """Get the local_case_feature_residual_convictions_robust of this DetailsResponse.


        :return: The local_case_feature_residual_convictions_robust of this DetailsResponse.
        :rtype: list[dict[str, float]]
        """
        return self._local_case_feature_residual_convictions_robust

    @local_case_feature_residual_convictions_robust.setter
    def local_case_feature_residual_convictions_robust(self, local_case_feature_residual_convictions_robust):
        """Set the local_case_feature_residual_convictions_robust of this DetailsResponse.


        :param local_case_feature_residual_convictions_robust: The local_case_feature_residual_convictions_robust of this DetailsResponse.
        :type local_case_feature_residual_convictions_robust: list[dict[str, float]]
        """

        self._local_case_feature_residual_convictions_robust = local_case_feature_residual_convictions_robust

    @property
    def global_case_feature_residual_convictions_full(self):
        """Get the global_case_feature_residual_convictions_full of this DetailsResponse.


        :return: The global_case_feature_residual_convictions_full of this DetailsResponse.
        :rtype: list[dict[str, float]]
        """
        return self._global_case_feature_residual_convictions_full

    @global_case_feature_residual_convictions_full.setter
    def global_case_feature_residual_convictions_full(self, global_case_feature_residual_convictions_full):
        """Set the global_case_feature_residual_convictions_full of this DetailsResponse.


        :param global_case_feature_residual_convictions_full: The global_case_feature_residual_convictions_full of this DetailsResponse.
        :type global_case_feature_residual_convictions_full: list[dict[str, float]]
        """

        self._global_case_feature_residual_convictions_full = global_case_feature_residual_convictions_full

    @property
    def global_case_feature_residual_convictions_robust(self):
        """Get the global_case_feature_residual_convictions_robust of this DetailsResponse.


        :return: The global_case_feature_residual_convictions_robust of this DetailsResponse.
        :rtype: list[dict[str, float]]
        """
        return self._global_case_feature_residual_convictions_robust

    @global_case_feature_residual_convictions_robust.setter
    def global_case_feature_residual_convictions_robust(self, global_case_feature_residual_convictions_robust):
        """Set the global_case_feature_residual_convictions_robust of this DetailsResponse.


        :param global_case_feature_residual_convictions_robust: The global_case_feature_residual_convictions_robust of this DetailsResponse.
        :type global_case_feature_residual_convictions_robust: list[dict[str, float]]
        """

        self._global_case_feature_residual_convictions_robust = global_case_feature_residual_convictions_robust

    @property
    def hypothetical_values(self):
        """Get the hypothetical_values of this DetailsResponse.


        :return: The hypothetical_values of this DetailsResponse.
        :rtype: list[dict[str, object]]
        """
        return self._hypothetical_values

    @hypothetical_values.setter
    def hypothetical_values(self, hypothetical_values):
        """Set the hypothetical_values of this DetailsResponse.


        :param hypothetical_values: The hypothetical_values of this DetailsResponse.
        :type hypothetical_values: list[dict[str, object]]
        """

        self._hypothetical_values = hypothetical_values

    @property
    def distance_ratio(self):
        """Get the distance_ratio of this DetailsResponse.


        :return: The distance_ratio of this DetailsResponse.
        :rtype: list[float]
        """
        return self._distance_ratio

    @distance_ratio.setter
    def distance_ratio(self, distance_ratio):
        """Set the distance_ratio of this DetailsResponse.


        :param distance_ratio: The distance_ratio of this DetailsResponse.
        :type distance_ratio: list[float]
        """

        self._distance_ratio = distance_ratio

    @property
    def distance_ratio_parts(self):
        """Get the distance_ratio_parts of this DetailsResponse.


        :return: The distance_ratio_parts of this DetailsResponse.
        :rtype: list[DetailsResponseDistanceRatioPartsInner]
        """
        return self._distance_ratio_parts

    @distance_ratio_parts.setter
    def distance_ratio_parts(self, distance_ratio_parts):
        """Set the distance_ratio_parts of this DetailsResponse.


        :param distance_ratio_parts: The distance_ratio_parts of this DetailsResponse.
        :type distance_ratio_parts: list[DetailsResponseDistanceRatioPartsInner]
        """

        self._distance_ratio_parts = distance_ratio_parts

    @property
    def distance_contribution(self):
        """Get the distance_contribution of this DetailsResponse.


        :return: The distance_contribution of this DetailsResponse.
        :rtype: list[float]
        """
        return self._distance_contribution

    @distance_contribution.setter
    def distance_contribution(self, distance_contribution):
        """Set the distance_contribution of this DetailsResponse.


        :param distance_contribution: The distance_contribution of this DetailsResponse.
        :type distance_contribution: list[float]
        """

        self._distance_contribution = distance_contribution

    @property
    def similarity_conviction(self):
        """Get the similarity_conviction of this DetailsResponse.


        :return: The similarity_conviction of this DetailsResponse.
        :rtype: list[float]
        """
        return self._similarity_conviction

    @similarity_conviction.setter
    def similarity_conviction(self, similarity_conviction):
        """Set the similarity_conviction of this DetailsResponse.


        :param similarity_conviction: The similarity_conviction of this DetailsResponse.
        :type similarity_conviction: list[float]
        """

        self._similarity_conviction = similarity_conviction

    @property
    def most_similar_case_indices(self):
        """Get the most_similar_case_indices of this DetailsResponse.


        :return: The most_similar_case_indices of this DetailsResponse.
        :rtype: list[list[dict[str, object]]]
        """
        return self._most_similar_case_indices

    @most_similar_case_indices.setter
    def most_similar_case_indices(self, most_similar_case_indices):
        """Set the most_similar_case_indices of this DetailsResponse.


        :param most_similar_case_indices: The most_similar_case_indices of this DetailsResponse.
        :type most_similar_case_indices: list[list[dict[str, object]]]
        """

        self._most_similar_case_indices = most_similar_case_indices

    @property
    def generate_attempts(self):
        """Get the generate_attempts of this DetailsResponse.


        :return: The generate_attempts of this DetailsResponse.
        :rtype: list[float]
        """
        return self._generate_attempts

    @generate_attempts.setter
    def generate_attempts(self, generate_attempts):
        """Set the generate_attempts of this DetailsResponse.


        :param generate_attempts: The generate_attempts of this DetailsResponse.
        :type generate_attempts: list[float]
        """

        self._generate_attempts = generate_attempts

    @property
    def series_generate_attempts(self):
        """Get the series_generate_attempts of this DetailsResponse.


        :return: The series_generate_attempts of this DetailsResponse.
        :rtype: list[list[float]]
        """
        return self._series_generate_attempts

    @series_generate_attempts.setter
    def series_generate_attempts(self, series_generate_attempts):
        """Set the series_generate_attempts of this DetailsResponse.


        :param series_generate_attempts: The series_generate_attempts of this DetailsResponse.
        :type series_generate_attempts: list[list[float]]
        """

        self._series_generate_attempts = series_generate_attempts

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
        if not isinstance(other, DetailsResponse):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, DetailsResponse):
            return True

        return self.to_dict() != other.to_dict()

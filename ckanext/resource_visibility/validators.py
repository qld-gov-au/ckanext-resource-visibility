# encoding: utf-8

import ckan.plugins.toolkit as tk


def _get_validators():
    validator_funcs = (
        resource_visible,
        governance_acknowledgement,
        de_identified_data,
        request_privacy_assessment
    )

    return {
        "resource_visibility_{}".format(func.__name__): func
        for func in validator_funcs
    }


def resource_visible(value):
    """
    Set to default value if missing

    """
    return validate_value(value, "TRUE", ["TRUE", "FALSE"],
                          'resource visibility')


def governance_acknowledgement(value):
    """
    Set to default value if missing
    """
    return validate_value(value, "NO", ["YES", "NO"],
                          'governance acknowledgement')


def de_identified_data(value):
    """
    Set to default value if missing
    """
    return validate_value(value, "NO", ["YES", "NO"], 'de-identified data')


def request_privacy_assessment(value):
    """
    Set to default value if missing
    """
    return validate_value(value, "", ["YES", "NO"],
                          "request privacy assessment")


def validate_value(value, default_value, valid_values, field):
    if not value:
        return default_value
    if value not in valid_values:
        raise tk.ValidationError(
            tk._("Invalid {field} value. It must be {valid_values}.".format(
                field=field, valid_values=" or ".join(valid_values))))
    return value

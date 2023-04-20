# encoding: utf-8

import ckan.plugins.toolkit as tk
import ckan.authz as authz

from . import constants as const


def _get_validators():
    validator_funcs = (
        resource_visible,
        governance_acknowledgement,
        de_identified_data,
        request_privacy_assessment,
        privacy_assessment_result,
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


def privacy_assessment_result(key, data, errors, context):
    if len(key) != 3 or key[2] != const.FIELD_ASSESS_RESULT:
        return

    model = context['model']
    session = context['session']
    resource_id = data.get((u'resources', key[1], 'id'))

    if resource_id:
        # if data hasn't change - do not validate
        resource = session.query(model.Resource).get(resource_id)

        if not resource:
            return

        assessment_result = resource.extras.get(const.FIELD_ASSESS_RESULT)

        if (assessment_result and assessment_result == data[key])\
                or (not assessment_result and not data[key]):
            return

    # if there's no resource ID, it's a resource creation stage
    if not resource_id and not data[key]:
        return

    if context.get("ignore_auth"):
        return

    user = context.get('user')
    if user and authz.is_sysadmin(context.get('user')):
        return

    errors[key].append(tk._('You are not allowed to edit this field.'))
    raise tk.StopOnError()

import ckan.plugins.toolkit as tk

import ckanext.resource_visibility.constants as c
from ckanext.resource_visibility.utils import user_is_editor_or_admin


def _get_actions():
    return {
        "package_show": package_show,
    }


@tk.side_effect_free
@tk.chained_action
def package_show(next_func, context, data_dict):
    if context.get('ignore_auth'):
        return next_func(context, data_dict)

    data_dict = next_func(context, data_dict)

    data_dict['resources'] = remove_hidden_resources(context, data_dict)
    data_dict['num_resources'] = len(data_dict['resources'])

    # set a default value to 'NO', probably of some old datasets
    if data_dict.get(c.FIELD_DE_IDENTIFIED) is None:
        data_dict['de_identified_data'] = 'NO'

    if not user_is_editor_or_admin(context, data_dict):
        for field in c.PKG_RESTRICTED_FIELDS:
            data_dict.pop(field, None)

        for res in data_dict['resources']:
            for field in c.RES_RESTRICTED_FIELDS:
                res.pop(field, None)

    return data_dict


def remove_hidden_resources(context, data_dict):
    for res in data_dict["resources"]:
        if _is_resource_visible(res, data_dict):
            continue

        res["qld_hidden"] = True

    return [
        resource for resource in data_dict['resources']
        if is_resource_visible(context, resource, data_dict)
    ]

def is_resource_visible(context, res_dict, pkg_dict):
    """Check if resource visible for a specific user"""

    if context.get("ignore_auth"):
        return True

    if user_is_editor_or_admin(context, pkg_dict):
        return True

    return _is_resource_visible(res_dict, pkg_dict)


def _is_resource_visible(res_dict, pkg_dict):
    resource_visible = res_dict.get(c.FIELD_RESOURCE_VISIBLE)
    gov_acknowledgement = res_dict.get(c.FIELD_GOVERNANCE_ACKN)
    request_privacy_assess = res_dict.get(c.FIELD_REQUEST_ASSESS)
    de_identified_data = pkg_dict.get(c.FIELD_DE_IDENTIFIED)

    if resource_visible == c.FALSE:
        return False

    if gov_acknowledgement == c.YES:
        if request_privacy_assess == c.NO or not request_privacy_assess:
            return True
        if request_privacy_assess == c.YES:
            return False
    elif gov_acknowledgement == c.NO:
        return de_identified_data == c.NO

    return True

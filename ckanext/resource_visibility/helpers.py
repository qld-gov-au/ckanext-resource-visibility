# encoding: utf-8

import logging

import ckan.plugins.toolkit as tk
import ckan.model as model

from . import auth_functions, constants as const

log = logging.getLogger(__name__)


def _get_helpers():
    helpers_func = (
        get_package_dict,
        get_select_field_options,
        has_user_permission_for_org,
        get_assessment_result_help_url
    )

    return {
        "resource_visibility_{}".format(func.__name__): func
        for func in helpers_func
    }


def get_package_dict(id, use_get_action=True):
    """
    Return package dict.
    """
    if len(id) == 0:
        id = tk.request.view_args.get('id')

    try:
        if use_get_action:
            return tk.get_action('package_show')({}, {'name_or_id': id})
        else:
            pkg = model.Package.get(id)
            if pkg:
                return pkg.as_dict()
    except Exception as e:
        log.error(str(e))

    return {}


def get_select_field_options(field_name, field_schema='resource_fields'):
    """
    Return a list of select options.
    """
    if 'scheming_get_dataset_schema' not in tk.h:
        return []

    schema = tk.h.scheming_get_dataset_schema('dataset')

    for field in schema.get(field_schema, []):
        if field.get('field_name') == field_name and field.get(
                'choices', None):
            return tk.h.scheming_field_choices(field)


def has_user_permission_for_org(org_id, user_obj, permission):
    """
    Return False if user doesn't have permission in the organization.
    """
    if not user_obj:
        return False

    context = {'user': user_obj.name}
    data_dict = {'org_id': org_id, 'permission': permission}
    result = auth_functions.has_user_permission_for_org(context, data_dict)

    return result and result.get('success')


def get_assessment_result_help_url():
    return tk.config.get(const.PRIVACY_ASSESS_RESULT_LINK)

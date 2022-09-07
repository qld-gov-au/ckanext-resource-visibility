import ckan.plugins.toolkit as tk

import ckanext.resource_visibility.constants as const
from ckanext.resource_visibility.helpers import has_user_permission_for_org


def _get_actions():
    return {"package_show": package_show}


@tk.side_effect_free
@tk.chained_action
def package_show(next_func, context, data_dict):
    if context.get('ignore_auth'):
        return next_func(context, data_dict)

    data_dict = next_func(context, data_dict)

    if not has_user_permission_for_org(data_dict['owner_org'], context['auth_user_obj'],
                                   'create_dataset'):
        for res in data_dict['resources']:
            for field in const.RESTRICTED_FIELDS:
                res.pop(field, None)

    return data_dict

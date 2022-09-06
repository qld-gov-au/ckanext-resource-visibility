import ckan.model as model
import ckan.plugins.toolkit as tk

import ckanext.resource_visibility.constants as const
from .helpers import has_user_permission_for_org


def get_user():
    return tk.g.userobj if 'userobj' in dir(tk.g) else None


def hide_restricted_fields(resource_dict):
    """Some fields are visible only for org editor/admin and sysadmins
    Hide it when accessing metadata via API
    """
    package = model.Session.query(model.Package).get(resource_dict['package_id'])
    has_permission = has_user_permission_for_org(package.owner_org, get_user(),
                                                 'create_dataset')

    if not has_permission:
        for field in const.RESTRICTED_FIELDS:
            resource_dict.pop(field, None)

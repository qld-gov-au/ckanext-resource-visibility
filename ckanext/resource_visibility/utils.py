from ckanext.resource_visibility.helpers import has_user_permission_for_org


def user_is_editor_or_admin(context, data_dict):
    org_id = data_dict['owner_org']
    user = context['auth_user_obj']
    return has_user_permission_for_org(org_id, user, 'create_dataset')

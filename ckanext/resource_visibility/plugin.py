import ckan.plugins as p
import ckan.plugins.toolkit as tk

import ckanext.resource_visibility.constants as const
import ckanext.resource_visibility.utils as utils
from ckanext.resource_visibility.helpers import _get_helpers
from ckanext.resource_visibility.validators import _get_validators
from ckanext.resource_visibility.logic.action import _get_actions
from ckanext.resource_visibility.cli import _get_commands


class ResourceVisibilityPlugin(p.SingletonPlugin):
    p.implements(p.IConfigurer)
    p.implements(p.ITemplateHelpers)
    p.implements(p.IValidators)
    p.implements(p.IActions)
    p.implements(p.IClick)
    p.implements(p.IResourceController, inherit=True)

    # IConfigurer

    def update_config(self, config_):
        tk.add_template_directory(config_, "templates")
        tk.add_public_directory(config_, "public")
        tk.add_resource("assets", "resource_visibility")

    # ITemplateHelpers

    def get_helpers(self):
        return _get_helpers()

    # IValidators

    def get_validators(self):
        return _get_validators()

    # IActions

    def get_actions(self):
        return _get_actions()

    # IClick

    def get_commands(self):
        return _get_commands()

    # IResourceController
    def before_update(self, context, current_resource, updated_resource):
        old_assessment_result = current_resource.get(const.FIELD_ASSESS_RESULT)
        new_assessment_result = updated_resource.get(const.FIELD_ASSESS_RESULT)

        if old_assessment_result != new_assessment_result:
            utils.save_updated_privacy_assessment_result(updated_resource)

import ckan.plugins as p
import ckan.plugins.toolkit as tk

from . import constants as const, cli, utils, helpers, validators
from .logic import action


class ResourceVisibilityPlugin(p.SingletonPlugin):

    p.implements(p.IConfigurer)
    p.implements(p.ITemplateHelpers)
    p.implements(p.IValidators)
    p.implements(p.IActions)
    # Ensure 2.8 does not crash, just disable cli options
    if helpers.is_ckan_29():
        p.implements(p.IClick)
    p.implements(p.IResourceController, inherit=True)

    # IConfigurer

    def update_config(self, config_):
        tk.add_template_directory(config_, "templates")
        tk.add_public_directory(config_, "public")
        tk.add_resource("assets", "resource_visibility")

    # ITemplateHelpers

    def get_helpers(self):
        return helpers._get_helpers()

    # IValidators

    def get_validators(self):
        return validators._get_validators()

    # IActions

    def get_actions(self):
        return action._get_actions()

    # IClick

    def get_commands(self):
        return cli._get_commands()

    # IResourceController

    def before_update(self, context, current_resource, updated_resource):
        return self.before_resource_update(context, current_resource, updated_resource)

    def before_resource_update(self, context, current_resource, updated_resource):
        old_assessment_result = current_resource.get(const.FIELD_ASSESS_RESULT)
        new_assessment_result = updated_resource.get(const.FIELD_ASSESS_RESULT)

        if new_assessment_result and old_assessment_result != new_assessment_result:
            utils.save_updated_privacy_assessment_result(updated_resource)

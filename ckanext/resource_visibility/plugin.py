import ckan.plugins as p
import ckan.plugins.toolkit as tk

from .helpers import _get_helpers
from .validators import _get_validators
from .logic.action import _get_actions


class ResourceVisibilityPlugin(p.SingletonPlugin):
    p.implements(p.IConfigurer)
    p.implements(p.ITemplateHelpers)
    p.implements(p.IValidators)
    p.implements(p.IActions)

    # IConfigurer

    def update_config(self, config_):
        tk.add_template_directory(config_, 'templates')
        tk.add_public_directory(config_, 'public')
        tk.add_resource('assets', 'resource_visibility')

    # ITemplateHelpers

    def get_helpers(self):
        return _get_helpers()

    # IValidators

    def get_validators(self):
        return _get_validators()

    # IActions

    def get_actions(self):
        return _get_actions()

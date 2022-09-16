import click

import ckanext.resource_visibility.utils as utils


def _get_commands():
    return [resource_visibility]


@click.group()
def resource_visibility():
    pass


@resource_visibility.command()
def notify_privacy_assessments():
    """Check for updated privacy_assessment_results"""
    data = utils.get_updated_privacy_assessment_result()

    if not data:
        return click.secho('No new privacy_assessment_result', fg='green')

    click.secho('Sending updated privacy_assessment_result to maintainers')

    for maintainer_email, updated_data in data.items():
        utils.send_notifications(maintainer_email, updated_data.values())
        utils._clear_upd_assessment_result_data()

    click.secho('Done', fg='green')

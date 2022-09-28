# -*- coding: utf-8 -*-

import uuid
import json
import logging
from datetime import datetime as dt

import ckan.plugins.toolkit as tk
from ckan.lib.mailer import mail_recipient, MailerException

from . import constants as const
from .helpers import has_user_permission_for_org

logger = logging.getLogger(__name__)


def user_is_editor_or_admin(context, data_dict):
    org_id = data_dict['owner_org']
    user = context['auth_user_obj']
    return has_user_permission_for_org(org_id, user, 'create_dataset')


def save_updated_privacy_assessment_result(res_data):
    pkg_dict = tk.get_action("package_show")({
        "ignore_auth": True
    }, {
        "id": res_data["package_id"]
    })

    res_url = tk.h.url_for("resource.read",
                           id=res_data["package_id"],
                           resource_id=res_data["id"],
                           _external=True)
    data_dict = {
        "id": res_data["id"],
        "package_id": res_data["package_id"],
        "maintainer": pkg_dict["maintainer"].strip(),
        const.FIELD_ASSESS_RESULT: res_data[const.FIELD_ASSESS_RESULT],
        "url": res_url,
    }

    update_upd_assessment_result_data(data_dict)


def get_updated_privacy_assessment_result():
    task = _get_upd_assessment_result_task()

    return json.loads(task['value'])


def update_upd_assessment_result_data(resource):
    task = _get_upd_assessment_result_task()
    data = json.loads(task['value'])

    maintainer = resource["maintainer"]
    data.setdefault(maintainer, {})
    data[maintainer][resource["id"]] = resource

    task['state'] = const.UPDATED
    task['last_updated'] = get_current_time()
    task['value'] = json.dumps(data)

    update_task({}, task)


def _clear_upd_assessment_result_data():
    task = _get_upd_assessment_result_task()
    task['value'] = '{}'
    task['state'] = const.EMPTY
    update_task({}, task)


def _get_upd_assessment_result_task():
    context = {"ignore_auth": True}
    data_dict = {
        'entity_id': _get_task_id(),
        'task_type': 'resource_visibility',
        'key': const.FIELD_ASSESS_RESULT,
    }

    try:
        task = tk.get_action('task_status_show')(context, data_dict)
    except tk.ObjectNotFound:
        return _create_upd_assessment_result_data()

    return task


def _get_task_id():
    return str(uuid.uuid5(uuid.NAMESPACE_DNS, const.FIELD_ASSESS_RESULT))


def _create_upd_assessment_result_data():
    data_dict = generate_task_data()
    return update_task({}, data_dict)


def generate_task_data(value=None):
    return {
        'entity_id': _get_task_id(),
        'entity_type': const.FIELD_ASSESS_RESULT,
        'task_type': 'resource_visibility',
        'last_updated': get_current_time(),
        'state': const.EMPTY,
        'key': const.FIELD_ASSESS_RESULT,
        'value': json.dumps(value or {})
    }


def get_current_time():
    return str(dt.utcnow())


def update_task(context, data_dict):
    context["ignore_auth"] = True

    task = tk.get_action('task_status_update')(context, data_dict)

    return task


def send_notifications(email, resources):
    subject = tk.render('emails/subject/privacy_assessment_result.txt', {})
    body = _prepary_email_body(resources)

    try:
        mail_recipient(email.split("@")[0], email, subject=subject, body=body)
    except MailerException:
        logger.error('Error sending email to: {}'.format(email))


def _prepary_email_body(resources):
    extra_vars = {
        'site_title': 'Home | Queensland Government',
        'resources': resources
    }

    return tk.render('emails/body/privacy_assessment_result.txt',
                         extra_vars)

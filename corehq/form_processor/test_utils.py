from couchdbkit import ResourceNotFound

from casexml.apps.case.models import CommCareCase
from casexml.apps.phone.models import SyncLog
from couchforms.models import XFormInstance
from dimagi.utils.couch.database import safe_delete
from corehq.util.test_utils import unit_testing_only


class FormProcessorTestUtils(object):

    @classmethod
    @unit_testing_only
    def delete_all_cases(cls):
        cls._delete_all(CommCareCase.get_db(), 'case/get_lite')

    @classmethod
    @unit_testing_only
    def delete_all_xforms(cls, domain=None, user_id=None):
        view = 'couchforms/all_submissions_by_domain'
        view_kwargs = {}
        if domain and user_id:
            view = 'reports_forms/all_forms'
            view_kwargs = {
                'startkey': ['submission user', domain, user_id],
                'endkey': ['submission user', domain, user_id, {}],

            }
        elif domain:
            view_kwargs = {
                'startkey': [domain],
                'endkey': [domain, {}]
            }

        cls._delete_all(
            XFormInstance.get_db(),
            view,
            **view_kwargs
        )

    @classmethod
    @unit_testing_only
    def delete_all_sync_logs(cls):
        cls._delete_all(SyncLog.get_db(), 'phone/sync_logs_by_user')

    @staticmethod
    @unit_testing_only
    def _delete_all(db, viewname, **view_kwargs):
        deleted = set()
        for row in db.view(viewname, reduce=False, **view_kwargs):
            doc_id = row['id']
            if id not in deleted:
                try:
                    safe_delete(db, doc_id)
                    deleted.add(doc_id)
                except ResourceNotFound:
                    pass
"""
    Argo Workflows API

    Argo Workflows is an open source container-native workflow engine for orchestrating parallel jobs on Kubernetes. For more information, please see https://argo-workflows.readthedocs.io/en/release-3.5/  # noqa: E501

    The version of the OpenAPI document: VERSION
    Generated by: https://openapi-generator.tech
"""


import unittest

import argo_workflows
from argo_workflows.api.archived_workflow_service_api import ArchivedWorkflowServiceApi  # noqa: E501


class TestArchivedWorkflowServiceApi(unittest.TestCase):
    """ArchivedWorkflowServiceApi unit test stubs"""

    def setUp(self):
        self.api = ArchivedWorkflowServiceApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_delete_archived_workflow(self):
        """Test case for delete_archived_workflow

        """
        pass

    def test_get_archived_workflow(self):
        """Test case for get_archived_workflow

        """
        pass

    def test_list_archived_workflow_label_keys(self):
        """Test case for list_archived_workflow_label_keys

        """
        pass

    def test_list_archived_workflow_label_values(self):
        """Test case for list_archived_workflow_label_values

        """
        pass

    def test_list_archived_workflows(self):
        """Test case for list_archived_workflows

        """
        pass

    def test_resubmit_archived_workflow(self):
        """Test case for resubmit_archived_workflow

        """
        pass

    def test_retry_archived_workflow(self):
        """Test case for retry_archived_workflow

        """
        pass


if __name__ == '__main__':
    unittest.main()

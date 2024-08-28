from django.test import TestCase
from django.utils import timezone
from mongodb import MongoDBClient
from mongo_operations import (
        find_one,
        insert_item,
        update_item,
        delete_one
)


class TaskAPITest(TestCase):

    def setUp(self):
        # Insert a test task
        self.user = 1
        self.test_task = {
            'title': 'Test Task',
            'description': 'Just a test',
            'creation_date': timezone.now(),
            'due_date': timezone.now(),
            'status': 'Pending',
            'user_id': self.user
        }
        self.test_task_id = insert_item(data=self.test_task, collection_name='test').inserted_id
        self.client = MongoDBClient.get_database()
        self.collection = self.client['test']

    def tearDown(self):
        self.collection.drop()

    def test_task_creation(self):
        task_count = self.collection.count_documents({})
        self.assertEqual(task_count, 1)

    def test_task_retrieval(self):
        task = find_one(self.user, self.test_task_id, 'test')
        self.assertIsNotNone(task)
        self.assertEqual(task['title'], 'Test Task')

    def test_task_update(self):
        update_data = {
            'title': 'new title',
            'description': 'new description',
            'due_date': timezone.now(),
            'status': 'completed',
            'user_id': self.user
        }
        update_item(
            self.user,
            self.test_task_id,
            update_data, 'test')
        task = find_one(self.user, self.test_task_id, 'test')
        self.assertEqual(task['status'], 'Completed')

    def test_task_deletion(self):
        delete_one(self.user, self.test_task_id, 'test')
        task_count = self.collection.count_documents({})
        self.assertEqual(task_count, 0)

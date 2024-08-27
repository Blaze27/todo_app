# import mongomock
# import json
# from django.test import TestCase
# from rest_framework.test import APIClient
# from django.contrib.auth.models import User
# from unittest.mock import patch, MagicMock
#
#
#
# class TaskViewSetTest(TestCase):
#     def setUp(self):
#         self.patcher = patch('tasks.mongodb.MongoClient', return_type=mongomock.MongoClient())
#         self.mocked_client = self.patcher.start()
#         self.client = APIClient()
#         self.user = User.objects.create_user(
#             username='test-user', password='testpassword', email='testuser@email.com'
#         )
#
#         self.client.force_authenticate(user=self.user)
#
#         self.db = self.mocked_client['test_db']
#         self.collection = self.db['tasks']
#
#         self.collection.insert_one = MagicMock()
#         self.collection.find_one = MagicMock(return_value={
#             'title': 'test-task',
#             'description': 'test description',
#             'creation_date': '2024-08-25',
#             'due_date': '2024-08-30',
#             'status': 'pending'
#         })
#
#     def tearDown(self):
#         self.patcher.stop()
#
#     def test_create_task(self):
#         data = {
#             'title': 'test-task',
#             'description': 'test description',
#             'creation_date': '2024-08-25',
#             'due_date': '2024-08-30',
#             'status': 'pending'
#         }
#
#         response = self.client.post(
#             '/api/tasks/', data=json.dumps(data), content_type='application/json'
#         )
#         print(response)
#         self.assertEqual(response.status_code, 201)
#         self.assertTrue('_id' in response.data)
#
#         task = self.collection.find_one(
#             {'user_id': 1},
#             {'title': 'test-task'}
#         )
#         self.assertIsNotNone(task)
#         # import pdb; pdb.set_trace()
#         # self.assertEqual(task['description'], 'test description')
#
#     def test_get_tasks(self):
#         task_id = self.collection.insert_one({
#             'title': 'test-task',
#             'description': 'test description',
#             'creation_date': '2024-08-25',
#             'due_date': '2024-08-30',
#             'status': 'pending',
#             'user_id': self.user.id
#         }).inserted_id
#
#         import pdb; pdb.set_trace()
#
#         response = self.client.get(f'/api/tasks/{task_id}')
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(len(response.data['results']), 1)
#         print(response.data)
#         self.assertEqual(response.data[0]['title'], 'test-task')
    #
    # def test_update_task(self):
    #     task_id = self.collection.insert_one({
    #         'title': 'test-task',
    #         'description': 'test description',
    #         'creation_date': '2024-08-25',
    #         'due_date': '2024-08-30',
    #         'status': 'pending',
    #         'user_id': self.user.id
    #     }).inserted_id
    #
    #     update_data = {
    #         'title': 'updated task',
    #         'description': 'updated description',
    #         'due_date': '2024-08-30',
    #         'status': 'completed'
    #     }
    #     response = self.client.put(
    #         f'/api/tasks/{task_id}', data=json.dumps(update_data), content_type='application.json'
    #     )
    #     self.assertEqual(update_data['title'], 'updated task')
    #     self.assertEqual(update_data['description'], 'updated description')
    #
    #
    # def test_delete_task(self):
    #     task_id = self.collection.insert_one({
    #         'title': 'test-task',
    #         'description': 'test description',
    #         'creation_date': '2024-08-25',
    #         'due_date': '2024-08-30',
    #         'status': 'pending',
    #         'user_id': self.user.id
    #     }).inserted_id
    #
    #     response = self.client.delete(
    #         f'/api/tasks/', params={'task_id': 1}
    #     )
    #     self.assertEqual(response.status_code, 204)
    #     task = self.collection.find_one(
    #         {'_id': task_id}
    #     )
    #     self.assertIsNone(task)
    #
    #
    # def test_pagination(self):
    #     for i in range(10):
    #         self.collection.insert_one(
    #             {
    #                 'title': f'test-task-{i}',
    #                 'description': f'test description {i}',
    #                 'creation_date': '2024-08-25',
    #                 'due_date': '2024-08-30',
    #                 'status': 'pending',
    #                 'user_id': self.user.id
    #             }
    #         )
    #
    #     response = self.client.get(
    #         '/api/tasks/?page=1&page_size=3'
    #     )
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(len(response.data), 4)
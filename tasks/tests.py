from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from datetime import date, timedelta
from employees.models import Employee
from tasks.models import Task


class TaskCRUDTests(APITestCase):

    def setUp(self):
        self.task_data = {
            "title": "Тестовая задача",
            "due_date": (date.today() + timedelta(days=3)).isoformat()
        }
        self.task = Task.objects.create(**self.task_data)

    def test_task_list(self):
        url = reverse('task-list')  # замените на ваш URL name
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_task_retrieve(self):
        url = reverse('task-detail', args=[self.task.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.task.id)

    def test_task_create(self):
        url = reverse('task-create')
        response = self.client.post(url, self.task_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], self.task_data['title'])

    def test_task_update(self):
        url = reverse('task-update', args=[self.task.id])
        updated_data = {
            "title": "Обновлённая задача",
            "due_date": (date.today() + timedelta(days=5)).isoformat()
        }
        response = self.client.put(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], updated_data['title'])

    def test_task_delete(self):
        url = reverse('task-delete', args=[self.task.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Task.objects.filter(id=self.task.id).exists())


class TaskValidationTests(APITestCase):

    def setUp(self):
        self.employee = Employee.objects.create(full_name="Иван Иванов", position="Разработчик")
        self.parent_task = Task.objects.create(
            title="Родительская задача",
            due_date=date.today() + timedelta(days=5)
        )

    def test_due_date_in_past(self):
        url = reverse('task-create')
        data = {
            "title": "Просроченная задача",
            "due_date": "2020-01-01"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Срок задачи не может быть в прошлом.", str(response.data))

    def test_self_parent_task(self):
        task = Task.objects.create(title="Задача-самоссылка", due_date=date.today() + timedelta(days=3))
        url = reverse('task-update', args=[task.id])
        data = {
            "title": "Задача-самоссылка",
            "due_date": task.due_date,
            "parent_task": task.id
        }
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Задача не может быть родительской сама себе.", str(response.data))

    def test_due_date_later_than_parent(self):
        url = reverse('task-create')
        data = {
            "title": "Подзадача с неверной датой",
            "due_date": self.parent_task.due_date + timedelta(days=2),
            "parent_task": self.parent_task.id}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Срок подзадачи не может быть позже срока родительской задачи.", str(response.data))

    def test_valid_task_creation(self):
        url = reverse('task-create')
        data = {
            "title": "Корректная задача",
            "due_date": date.today() + timedelta(days=3)
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class TaskListViewTests(APITestCase):
    def setUp(self):
        # Создаем двух сотрудников
        self.employee1 = Employee.objects.create(full_name="Иван Иванов", position="Дизайнер")
        self.employee2 = Employee.objects.create(full_name="Анна Смирнова", position="Разработчик")

        # Создаем 2 задачи
        self.task1 = Task.objects.create(
            title="Сделать логотип",
            due_date=date.today() + timedelta(days=3),
            assignee=self.employee1
        )
        self.task2 = Task.objects.create(
            title="Верстка лендинга",
            due_date=date.today() + timedelta(days=5),
            assignee=self.employee2
        )

    def test_task_list_view(self):
        url = reverse('task-list')  # соответствует name='task-list' в urls.py
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # проверяем, что 2 задачи возвращены

    # Тест на создание задачи (CreateView)
    def test_create_task(self):
        url = reverse('task-create')  # name в urls.py
        data = {
            "title": "Новая задача",
            "due_date": str(date.today() + timedelta(days=3)),
            "assignee": self.employee1.id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 3)
        self.assertEqual(Task.objects.latest('id').title, "Новая задача")

    # Тест на обновление задачи (UpdateView)
    def test_update_task(self):
        url = reverse('task-update', kwargs={"pk": self.task1.id})  # name='task-update'
        data = {
            "title": "Обновленная задача",
            "due_date": str(date.today() + timedelta(days=7)),
            "assignee": self.employee1.id
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.task1.refresh_from_db()
        self.assertEqual(self.task1.title, "Обновленная задача")

    # Тест на удаление задачи (DeleteView)
    def test_delete_task(self):
        url = reverse('task-delete', kwargs={"pk": self.task2.id})  # name='task-delete'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Task.objects.filter(id=self.task2.id).exists())


class ImportantTasksTests(APITestCase):
    def setUp(self):
        # Создаем сотрудников
        self.employee1 = Employee.objects.create(full_name="Иван Иванов", position="Дизайнер")
        self.employee2 = Employee.objects.create(full_name="Анна Смирнова", position="Разработчик")

        # Создаем родительские задачи
        self.parent_task1 = Task.objects.create(
            title="Основная задача 1",
            due_date=date.today() + timedelta(days=7),
            status="in_progress",
            assignee=self.employee1
        )
        self.parent_task2 = Task.objects.create(
            title="Основная задача 2",
            due_date=date.today() + timedelta(days=5),
            status="in_progress",
            assignee=self.employee2
        )

        # Создаем важные задачи, зависимые от родительских
        self.important_task1 = Task.objects.create(
            title="Важная задача 1",
            due_date=date.today() + timedelta(days=3),
            status="new",
            parent_task=self.parent_task1
        )
        self.important_task2 = Task.objects.create(
            title="Важная задача 2",
            due_date=date.today() + timedelta(days=6),
            status="new",
            parent_task=self.parent_task2
        )

    def test_important_tasks_view(self):
        url = reverse('important-tasks')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Проверяем, что возвращаются 2 важные задачи
        self.assertEqual(len(response.data), 2)

        # Проверяем, что важные задачи имеют правильные данные
        self.assertEqual(response.data[0]['title'], "Важная задача 1")
        self.assertEqual(response.data[1]['title'], "Важная задача 2")

        # Проверяем, что список доступных сотрудников не пустой
        self.assertIn('available_employees', response.data[0])
        self.assertIsInstance(response.data[0]['available_employees'], list)

    def test_no_available_employees_for_important_task(self):
        # Убираем у сотрудника задачи, чтобы они не имели активных задач
        self.employee1.tasks.clear()

        url = reverse('important-tasks')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Проверяем, что доступным сотрудником для задачи является least_loaded_employee
        self.assertIn(self.employee1.full_name, response.data[0]['available_employees'])

    def test_important_task_without_parent(self):
        # Создаем задачу без родительской
        task_without_parent = Task.objects.create(
            title="Задача без родителя",
            due_date=date.today() + timedelta(days=4),
            status="new"
        )

        url = reverse('important-tasks')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Проверяем, что задача без родителя не попала в список важных задач
        self.assertNotIn(task_without_parent.id, [task['id'] for task in response.data])

from django.db import models
from user_service.models import UserProfile


TEST_NAME_MAX_LEN = 255
TASK_MAX_LEN = 2024
OPTION_MAX_LEN = TASK_MAX_LEN


class Task(models.Model):
    text = models.CharField(max_length=TASK_MAX_LEN)

    def __repr__(self):
        return f'<Task text: {self.text}>'

    def __str__(self):
        return self.__repr__()

class Option(models.Model):
    text = models.CharField(max_length=OPTION_MAX_LEN)
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE
    )

    def __repr__(self):
        return f'<Option text: {self.text}>'

    def __str__(self):
        return self.__repr__()

class Test(models.Model):
    name = models.CharField(max_length=TEST_NAME_MAX_LEN)
    tasks = models.ManyToManyField(Task)

    def __repr__(self):
        return f'<Option name: {self.name}>'

    def __str__(self):
        return self.__repr__()


class Answer(models.Model):
    user = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
    )
    test = models.ForeignKey(
        Test,
        on_delete=models.CASCADE,
        )
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
    )
    option = models.ForeignKey(
        Option,
        on_delete=models.CASCADE,
    )

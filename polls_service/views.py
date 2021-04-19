from django.shortcuts import render, redirect
from django.views import View
from .models import Answer, Task, Test, Option
from user_service.models import UserProfile
from django.db import transaction
from django.db.models import Count
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
import logging

logger = logging.getLogger(__name__)
DEFAULT_CACHE_TIME = 60


class TestsView(View):
    template_name = 'polls_service/tests.html'

    def get(self, request):
        logger.info(request.user)
        user = UserProfile.objects.get(user=request.user)

        tests = Test.objects.all()

        passed = Answer.objects.filter(user=user).values('test')
        passed = set([e['test'] for e in passed])
        tests = sorted([(test, test.id in passed)
                       for test in tests], key=lambda x: x[1])
        logger.info(tests)
        return render(request, self.template_name, {'tests': tests})


class TestView(View):
    template_name = 'polls_service/test.html'

    @method_decorator(cache_page(DEFAULT_CACHE_TIME))
    def get(self, request, test_id):
        user = UserProfile.objects.get(user=request.user)

        test = Test.objects.filter(id=test_id).first()
        tasks = test.tasks.all()
        options = [task.option_set.all() for task in tasks]
        answers = self.make_answers(request, test_id)

        context = {
            'test': test,
            'tasks': zip(tasks, options, answers),
        }
        return render(request, self.template_name, context)

    def post(self, request, test_id):
        user = UserProfile.objects.get(user=request.user)

        answers = self.make_answers(request, test_id)

        if self.__validate_answers(answers):
            logger.info('POLL SAVED')
            with transaction.atomic():
                for answ in answers:
                    answ.save()
            return redirect('polls_service:tests')

        test = Test.objects.filter(id=test_id).first()
        tasks = test.tasks.all()
        options = [task.option_set.all() for task in tasks]
        context = {
            'test': test,
            'tasks': zip(tasks, options, answers),
        }
        return render(request, self.template_name, context)

    def make_answers(self, request, test_id):
        test = Test.objects.filter(id=test_id).first()
        user = UserProfile.objects.get(user=request.user)

        answers = []
        for task in test.tasks.all():
            option = request.POST.get(str(task.id), None)
            try:
                if option:
                    option = Option.objects.get(id=int(option))
            except Exception as err:
                logger.error(err)

            answ = Answer(
                task=task,
                user=user,
                test=test,
                option=option,
            )
            answers.append(answ)

        return answers

    def __validate_answers(self, answers):
        try:
            for answ in answers:
                if answ.option is None:
                    return False
        except:
            return False

        return True

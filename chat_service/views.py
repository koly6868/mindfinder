from django.shortcuts import render, redirect
from django.http import HttpResponseNotFound
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from user_service.models import UserProfile
from django.contrib.auth.models import User
from .models import Chat, Message
from .forms import CreateChatForm, NewMessageForm
from django.db.models import Count
from django.contrib.auth.models import User
from user_service.models import UserProfile
from polls_service.models import Answer
from datetime import datetime
from django.db import connection
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
import logging


DEFAULT_CACHE_TIME = 10
logger = logging.getLogger(__name__)


class ChatListView(LoginRequiredMixin, View):
    template_name = 'chat_service/chats.html'

    def get(self, request):
        user = UserProfile.objects.get(user=request.user)
        chats = Chat.objects.filter(participants__id__contains=user.id).all()
        logger.info(f'retrived {len(chats)} chats for user {user}')
        chats = [{
            'chat': chat,
            'avatar': chat.participants.exclude(id=user.id).first().avatar.name,
        } for chat in chats]
        logger.info(chats)
        return render(request, self.template_name, {'chats': chats, 'error': ''})


class ChatView(LoginRequiredMixin, View):
    template_name = 'chat_service/chat.html'

    def get(self, request, chat_id):
        user = UserProfile.objects.get(user=request.user)
        form = NewMessageForm()
        context = self.__prepare_context(request, chat_id, user, form)

        if context is None:
            return HttpResponseNotFound('something went wrong')

        return render(request, self.template_name, context)

    def post(self, request, chat_id):
        user = UserProfile.objects.get(user=request.user)

        form = NewMessageForm(request.POST)
        if form.is_valid():
            chat = Chat.objects.filter(id=form.get_chat_id()).first()
            if chat is None:
                return HttpResponseNotFound('wrong chat')

            if not chat.participants.filter(id=user.id).exists():
                return HttpResponseNotFound('wrong user')

            message = Message(
                chat=chat,
                message=form.get_message(),
                owner=user
            )
            message.save()
            return redirect('chat_service:chat', chat_id=chat.id)

        context = self.__prepare_context(request, chat_id, user, form)
        return render(request, self.template_name, context)

    def __prepare_context(self, request, chat_id, user, form):
        chat = Chat.objects.filter(
            participants__id__contains=user.id,
            id=chat_id).first()

        if chat is None:
            return None

        messages = Message.objects.filter(chat=chat.id).all()
        context = {
            'chat': chat,
            'user': user,
            'messages': messages,
            'form': form,
        }
        return context


class ChatAPIView(LoginRequiredMixin, View):
    template_name = 'chat_service/chat_api.html'

    def get(self, request, chat_id):
        user = UserProfile.objects.get(user=request.user)
        chat = Chat.objects.filter(
            participants__id__contains=user.id,
            id=chat_id).first()
        if chat is None:
            return HttpResponseNotFound('something went wrong')

        messages = Message.objects.filter(chat=chat.id).all()
        context = {
            'user': user,
            'messages': messages,
        }

        if context is None:
            return HttpResponseNotFound('something went wrong')

        return render(request, self.template_name, context)


class CreateChatView(LoginRequiredMixin, View):
    template_name = 'chat_service/new.html'

    @method_decorator(cache_page(DEFAULT_CACHE_TIME))
    def get(self, request):
        user = request.user
        u = User.objects.first()
        profiles = UserProfile.objects.all()
        user = [e for e in profiles if e.user.id == user.id][0]
        profiles = [e for e in profiles if e.user.id != user.user.id]
        profiles = self.__rank(user, profiles)
        return render(request, self.template_name, {'profiles': profiles})

    def __rank(self, user, profiles):
        sql = """SELECT t.user_id, count(*) 
                    FROM polls_service_answer
                    JOIN polls_service_answer as t 
                    ON polls_service_answer.task_id = t.task_id AND
                        polls_service_answer.user_id != t.user_id AND
                        polls_service_answer.option_id = t.option_id
                    WHERE polls_service_answer.user_id = %s
                    GROUP BY polls_service_answer.user_id, t.user_id"""
        rank_map = {}
        with connection.cursor() as cursor:
            cursor.execute(sql, [user.id])
            rows = cursor.fetchall()

            for row in rows:
                uid = int(row[0])
                r = int(row[1])
                rank_map[uid] = r
        profiles = sorted(
            profiles, key=lambda x: rank_map.get(x.id, 0), reverse=True)
        return profiles

    def post(self, request):
        form = CreateChatForm(request.POST)

        if form.is_valid():
            first_user = UserProfile.objects.get(user=request.user)
            second_user = UserProfile.objects.get(id=form.get_profile_id())
            chat_exists = Chat.objects.annotate(pc=Count('participants')) \
                .filter(pc=2).filter(participants__id__contains=first_user.id) \
                .filter(participants__id__contains=second_user.id) \
                .exists()

            if chat_exists:
                logger.info(
                    f'chat between {first_user.id} and {second_user.id} exists')
                return redirect('chat_service:chats')

            chat = Chat(
                name=f'{first_user.name},{second_user.name}',
                start_date=datetime.now(),
            )
            chat.save()
            try:
                chat.participants.add(first_user.id)
                chat.participants.add(second_user.id)
            except Exception as err:
                logger.error(err)
                chat.delete()

            return redirect('chat_service:chats')

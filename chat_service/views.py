from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from user_service.models import UserProfile
from django.contrib.auth.models import User
from .models import Chat, Message
from .forms import CreateChatForm
from django.db.models import Count
from django.contrib.auth.models import User
from user_service.models import UserProfile

from datetime import datetime
import logging


logger = logging.getLogger(__name__)


class ChatListView(LoginRequiredMixin, View):
    template_name = 'chat_service/chats.html'

    def get(self, request):
        user = UserProfile.objects.get(user=request.user)
        chats = Chat.objects.filter(participants__id__contains=user.id).all()
        logger.info(f'retrived {len(chats)} chats for user {user}')

        return render(request, self.template_name, {'chats': chats, 'error' : ''})



class ChatView(LoginRequiredMixin, View):
    template_name = 'chat_service/chat.html'

    def get(self, request, chat_id):
        user = UserProfile.objects.get(user=request.user)
        chat = Chat.objects.filter(
            participants__contains=user,
            id=chat_id).first()
        
        if chat is None:
            chat_err = 'chat does not exists'
            return render(request, self.template_name, {'chat': None, 'error' : chat_err})
        
        return render(request, self.template_name, {'chat': chat, 'error' : ''})
    
    def post(self, request):
        form = CreateChatForm(request.POST)

        if form.is_valid():
            first_user = request.user
            second_user_id = form.get_target_user_id()
            chat_exists = Chat.objects.annotate(pc=Count('participants')) \
                .filter(pc=2).filter(participants__id__contains=first_user.id) \
                .filter(participants__id__contains=second_user_id) \
                .exists()

            if chat_exists:
                logger.info(f'chat between {first_user.id} and {second_user_id} exists')
                return render(request, self.template_name, {'form' : form, 'error' : 'chat exists'})
            
            return redirect()



class CreateChatView(LoginRequiredMixin, View):
    template_name = 'chat_service/new.html'

    def get(self, request):
        user = request.user
        u = User.objects.first()
        profiles = UserProfile.objects.exclude(user=user)[:20]
        return render(request, self.template_name, {'profiles' : profiles})

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
                logger.info(f'chat between {first_user.id} and {second_user.id} exists')
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
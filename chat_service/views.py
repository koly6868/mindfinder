from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Chat, Message
from .forms import CreateChatForm
import logging


logger = logging.getLogger(__name__)


class ChatsView(LoginRequiredMixin, View):
    template_name = 'chat_service/chats.html'

    def get(self, request):
        user = request.user
        chats = Chat.objects.filter(participants__contains=user).all()
        logger.info(f'retrived {len(chats)} chats for user {user}')

        return render(request, self.template_name, {'chats' : chats})

    def post(self, request):
        form = CreateChatForm(request.POST)

        if form.is_valid():
            tuser = form.get_target_user_id()
        


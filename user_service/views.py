from django.shortcuts import render
from django.views import View
from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import UserProfile
from .forms import SignForm
from django.db import transaction

import user_service.common as common
import logging


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

LOGIN_ALREADY_EXISTS_ERROR = 'login already exists'
SOMETHING_WENT_WRONG = 'something went wrong'
TOO_SHORT_ERROR  = 'password must be 8 symbols or greater'
SYMBOLS_NOT_ALLOWED_ERROR = 'symbols not allowed'
USER_DOES_NOT_EXISTS_ERROR = 'user does not exists'


def create_user(username, password) -> auth.models.User:
    user = None
    with transaction.atomic():
        user = auth.models.User.objects.create_user(username=form.get_login(), password=form.get_password())
        user_profile = UserProfile(user=user)
        

class SignUp(View):
    template_name = 'user_service/signup.html'

    def get(self, request):
        form = SignForm()
        return render(request, self.template_name, {form : form, 'error': ''})

    def post(self, request):
        form = SignForm(request.POST)

        if form.is_valid():
            user_exists = auth.models.User.objects.filter(username=form.get_login()).exists()
            
            if user_exists:
                logger.info('signup user already exists')
                return render(request, self.template_name, {form : form, 'error': LOGIN_ALREADY_EXISTS_ERROR})   

            err = self._check_password(form.get_password())
            if err:
                logger.info(f'signup password error: {err}')
                return render(request, self.template_name, {form : form, 'error': err})
            
            err = self._check_login(form.get_login())
            if err:
                logger.info(f'signup login error: {err}')
                return render(request, self.template_name, {form : form, 'error': err})

            auth_user = auth.models.User.objects.create_user(username=form.get_login(), password=form.get_password())
            #user = User(uid=form.get_login(), name=form.get_username())
            try:
                with transaction.atomic():
                    auth_user.save()
                    #user.save()
            except Exception as err:
                logger.info(f'signup unable to create user {err}')
                return render(request, self.template_name, {form : form, 'error': SOMETHING_WENT_WRONG})
            
            return redirect('user_service:signin')

        logger.info('signup form is invalid')   
        return render(request, self.template_name, {form : form, 'error': SOMETHING_WENT_WRONG})
    
    def _check_password(self, password : str):
        if len(password) < 8:
            return f'paswword {TOO_SHORT_ERROR}'
        
        if not common.is_str_allowed(password):
            return f'password {SYMBOLS_NOT_ALLOWED_ERROR}'

        return ''
    
    def _check_login(self, login : str):
        if not len(login):
            return f'login {TOO_SHORT_ERROR}'
        
        if not common.is_str_allowed(login):
            return f'login {SYMBOLS_NOT_ALLOWED_ERROR}'
            
        return ''

        

class SignIn(View):
    template_name = 'user_service/signin.html'

    def get(self, request):
        form = SignForm()
        return render(request, self.template_name, {form : form, 'error': ''})

    def post(self, request):
        form = SignForm(request.POST)

        if form.is_valid():
            username = form.get_login()
            password = form.get_password()
            logger.debug(f'{username}, {password}')
            user = auth.authenticate(request, username=username, password=password)
            logger.debug(user)
            if user is not None:
                auth.login(request, user)
                return redirect('user_service:profile')
            else:
                return render(request, self.template_name, {form : form, 'error': USER_DOES_NOT_EXISTS_ERROR})
        
        return render(request, self.template_name, {form : form, 'error': SOMETHING_WENT_WRONG})


class UserProfile(LoginRequiredMixin, View):
    template_name = 'user_service/profile.html'

    def get(self, request):
        logger.debug(request.user)
        user = request.user

        return render(request, self.template_name, {'user' : user})
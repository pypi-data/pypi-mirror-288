from django.db import models
from datetime import datetime, timedelta
from base64 import urlsafe_b64encode, urlsafe_b64decode
from .utils import *
from django.http.request import HttpRequest
from django.contrib.auth import get_user_model

USER_MODEL = get_user_model()



class TokenManager(models.Manager): # TODO write appropriate manager for your token --> done.
    def create_token(self, user):
        if not isinstance(user, USER_MODEL):
            raise TypeError(f'\'user\' most be an instance of {USER_MODEL.__name__} model') # TODO print actual user model name wether is custom or not form project settings --> done.
        
        new_token, x = self.get_or_create(user=user)
        new_token.created_at = datetime.now()
        new_token.save()
        return new_token


class CustomToken(models.Model):
    user = models.OneToOneField(USER_MODEL, on_delete=models.CASCADE, related_name='token')
    value = models.CharField(max_length=255, default='')
    expire_date = models.DateTimeField(default=datetime.now().replace(tzinfo=pytz_UTC))
    created_at = models.DateTimeField(default=datetime.now().replace(tzinfo=pytz_UTC))

    objects = TokenManager()
    

    @classmethod
    def create(cls, user):
        if not isinstance(user, USER_MODEL):
            raise TypeError(f'\'user\' most be an instance of {USER_MODEL.__name__} model') # TODO print actual user model name wether is custom or not form project settings --> done.
        
        new_token = cls.objects.create_token(user)
        return new_token


    @classmethod
    def get_token(cls, request:HttpRequest):
        headers = request.headers
        return headers.get('Authorization')


    @classmethod
    def verify(cls, request): # TODO use this class method and give the request --> done.
        
        try:
            token = cls.objects.get(value=cls.get_token(request))
        except:
            return False
        
        token_data = token.__decode()
        token_user = token_data[0]
        
        try:
            user = USER_MODEL.objects.get(id=token_user)
        except:
            return False
        
        try:
            user_token: CustomToken = user.token
        except:
            return False
        
        if token.value == user_token.value:
            if token_data[1] < datetime.now():
                return False
            return True
        
        user_token.save()
        return False
        
        # TODO change the token value with making value empty and save it if it's outdated --> done.


    def get_user(self):
        user = self.__decode()
        try:
            user = USER_MODEL.objects.get(id=user[0])
        except:
            raise Exception('user doesn\'t exist')
        return user
    

    def is_expired(self):
        token_data = self.__decode()
        if token_data[1] < datetime.now():
            self.delete()
            return True
        return False


    def __encode(self, ):
        """
        will be used just in save method
        """
        user_id = self.user.id
        exp_date = datetime.strftime(self.expire_date, "%m-%d-%Y/%H:%M:%S")
        
        data_str = f'uid={user_id},exp={exp_date}'
        data_str = cipher(raw=data_str)
        data_str = urlsafe_b64encode(bytes(data_str, 'utf-8')).decode()
        return data_str


    def __decode(self, ):
        """
        will be used just in verify method
        """
        data_str = urlsafe_b64decode(self.value).decode()
        data_str = cipher(raw=data_str)
        
        user_id = data_str.split(',')[0]
        user_id = int(user_id[user_id.index('=')+1:])
        
        exp_date = data_str.split(',')[1]
        exp_date = datetime.strptime(exp_date[exp_date.index('=')+1:], "%m-%d-%Y/%H:%M:%S")
        
        return (user_id, exp_date)
    
    
    def save(self, *args, **kwargs):
        """
        whenever save method is called, it will change expire date and after that the value
        of the token will be changed.
        """
        expire_time = settings.CUSTOM_TOKEN_CONF.get('token-life')
        self.expire_date = datetime.now().replace(tzinfo=pytz_UTC) + timedelta(minutes=expire_time)
        self.value = ''
        self.value = self.__encode()
        return super().save(*args, **kwargs)


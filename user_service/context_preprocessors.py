from .models import UserProfile
from mindfinder.settings import MEDIA_URL
import logging



logger = logging.getLogger(__name__)



def add_avatar_url(request):
    try:
        user = request.user
        if user and not user.is_anonymous:
            return {
                'avatar_url' : MEDIA_URL + UserProfile.objects.get(user=user).avatar.name
            }

    except Exception as err:
        logger.error(err)
    
    return {}
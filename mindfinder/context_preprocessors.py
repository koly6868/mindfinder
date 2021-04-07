from .settings import MEDIA_URL



def add_media_settings(request):
    return {
        'media_url' : MEDIA_URL
    }
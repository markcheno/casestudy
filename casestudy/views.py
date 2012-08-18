
from django.template import Context, loader
from casestudy.models import Likes
from django.http import HttpResponse

#def index(request):
#	return HttpResponse("Hello, world. You're at the case study home page.")

def index(request):
    latest_likes = Likes.objects.filter(company='Starbucks').order_by('time')[:20]
    #latest_likes = Likes.objects.all()

    t = loader.get_template('casestudy/index.html')
    c = Context({
        'latest_likes': latest_likes,
    })
    return HttpResponse(t.render(c))
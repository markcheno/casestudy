from django.template import Context, loader
from casestudy.models import Likes
from django.http import HttpResponse

def index(request):

    num_rows = Likes.objects.distinct('company').count() * 20
    latest_likes = Likes.objects.all().order_by('-time')[:num_rows]

    t = loader.get_template('casestudy/index.html')
    c = Context({
        'latest_likes': latest_likes,
    })

    return HttpResponse(t.render(c))
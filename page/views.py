from django.shortcuts import render

# Create your views here.
def page_story_home(request):
    return render(request,
                  "page/page_story/index.html")
def page_story_about(request):
    return render(request,
                  "page/page_story/about.html")

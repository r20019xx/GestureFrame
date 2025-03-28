from django.shortcuts import render

# Create your views here.
def homeview(request):
    return render(request,
                  "page/page_story/index.html")
def aboutview(request):
    return render(request,
                  "page/page_story/about.html")

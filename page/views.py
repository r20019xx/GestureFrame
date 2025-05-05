import datetime
from django.http import JsonResponse
from django.shortcuts import render, redirect
from .models import comments

# Create your views here.
def homeview(request):
    return render(request,
                  "page/page_story/index.html")
def aboutview(request):
    return render(request,
                  "page/page_story/about.html")

def feedbackview(request):
    commentsList = list(comments.objects.all().values('user', 'date', 'comment'))
    commentsList = {'commentsList': commentsList}
    return render(request,
                  "page/page_story/feedback.html",
                  commentsList)


def commentview(request):
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    if is_ajax and request.method == 'POST':
        try:
            comment_text = request.POST.get('comment_text')
            user = request.session.get('username')
            newComment = comments(
                user=user,
                comment=comment_text,
            )
            newComment.save()
            commentsList = list(comments.objects.all().values('user', 'date', 'comment'))
            commentsList = {'commentsList': commentsList}
            return JsonResponse({'success': 'success', 'comments': commentsList}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Invalid Ajax request'}, status=400)

def uploadview(request):
    return render(request,
                  "page/page_story/upload.html")
def privacypolicyview(request):
    return render(request,
                  "page/page_story/privacypolicy.html")

def faqview(request):
    return render(request,
                  "page/page_story/faq.html")

def contactview(request):
    return render(request,
                  "page/page_story/contact.html")
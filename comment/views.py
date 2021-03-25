from django.shortcuts import render, redirect
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse

from comment.models import Comment


def update_comment(request):
    referer = request.META.get('HTTP_REFERER', reverse('home'))
    user = request.user
    text = request.POST.get('text', '')
    content_type = request.POST.get('content_type', '')
    object_id = int(request.POST.get('object_id', ''))

    # Blog|blog
    # model_class = ContentType.objects.get(model=content_type)
    # blog.model.Blog
    model_class = ContentType.objects.get(model=content_type).model_class()
    model_obj = model_class.objects.get(pk=object_id)

    comment = Comment()
    comment.user = user
    comment.text = text
    comment.content_object = model_obj
    comment.save()

    return redirect(referer)
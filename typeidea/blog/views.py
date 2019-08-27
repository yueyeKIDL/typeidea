from django.contrib.admin.models import LogEntry
from django.contrib.admin.options import get_content_type_for_model
from django.http import HttpResponse

# Create your views here.
from blog.models import Post


def test_get_post_log_entry(request, post_pk):
    post = Post.objects.get(id=post_pk)
    log_entries = LogEntry.objects.filter(content_type_id=get_content_type_for_model(post).pk, object_id=post.pk)
    return HttpResponse(log_entries)

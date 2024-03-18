from django.views.generic import ListView

from expenses.models import Upload


class UploadListView(ListView):
    template_name = "expenses/upload_list.html"
    context_object_name = "uploads"
    queryset = Upload.objects.order_by("-id")

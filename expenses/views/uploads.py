import csv
import json
import re
import requests
from io import StringIO
from typing import Any


from django.conf import settings
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.utils import timezone
from django.views.generic import (
    FormView,
    ListView,
    TemplateView,
)

from expenses.forms import (
    TransactionInspectionForm,
    UploadForm,
    UploadTransformForm,
)
from expenses.models import (
    Account,
    Currency,
    Transaction,
    Period,
    Upload,
)
from expenses.serializers import TransactionSerializer
from expenses.utils import (
    change_account_from_assoc,
    str_to_date,
)

DATE_FIELD = 0
DESCRIPTION_FIELD = 1
AMOUNT_FIELD = 2
ACCOUNT_FIELD = 3


class UploadListView(ListView):
    template_name = "expenses/upload_list.html"
    context_object_name = "uploads"
    queryset = Upload.objects.order_by("-id")


class UploadView(FormView):
    template_name = "expenses/upload.html"
    form_class = UploadForm

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):
        file = form.cleaned_data["file"]

        if not file:
            form.add_error(None, "File empty")
            return self.form_invalid(form)

        upload = form.save()

        # create a dictionary with the file rows and columns
        file.seek(0)
        decoded_file = file.read().decode("utf-8-sig")

        csv_file = StringIO(decoded_file)
        reader = csv.reader(csv_file)

        rows = list(reader)
        if not rows:
            max_cols = 0
            num_rows = 0
        else:
            max_cols = max(len(row) for row in rows)
            num_rows = len(rows)

        upload.dimension = {
            "rows": num_rows,
            "cols": max_cols,
        }
        upload.save()

        return HttpResponseRedirect(reverse("upload-transform", args=(upload.id,)))



class UploadResultView(TemplateView):
    template_name = "expenses/transaction_upload_result.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        try:
            upload = Upload.objects.get(pk=self.kwargs.get("pk"))
            data = json.loads(upload.result)
            context.update(data)
            context["upload"] = upload
        except Upload.DoesNotExist:
            pass

        return context


class UploadInspectView(TemplateView):
    template_name = "expenses/upload_inspection.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        try:
            upload = Upload.objects.get(pk=self.kwargs.get("pk"))
            transactions = Transaction.objects.filter(upload=upload)
            context["upload"] = upload
            context["transactions"] = transactions
            context["accounts"] = Account.objects.order_by("name")
        except Upload.DoesNotExist:
            pass

        return context

    def post(self, request, *args, **kwargs):
        print("post")
        transaction = Transaction.objects.get(pk=request.POST.get("transaction_id"))
        form = TransactionInspectionForm(request.POST, instance=transaction)
        if form.is_valid():
            form.save()
            return JsonResponse({"success": True})
        return JsonResponse({"success": False, "errors": form.errors})

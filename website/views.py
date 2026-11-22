from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_http_methods, require_POST

from website.forms import AddRecordForm
from website.models import Costumer


@login_required
@permission_required("website.view_costumer", raise_exception=True)
def home(request):
    return render(request, "home.html", {"records": Costumer.objects.all()})


@require_http_methods(["GET", "POST"])
def login_user(request):
    next_url = request.POST.get("next") if request.method == "POST" else request.GET.get("next")
    if request.method == "POST":
        user = authenticate(
            request, username=request.POST.get("username"), password=request.POST.get("password")
        )
        if user is not None:
            login(request, user)
            if next_url and url_has_allowed_host_and_scheme(
                next_url, allowed_hosts={request.get_host()}, require_https=request.is_secure()
            ):
                return redirect(next_url)
            if user.has_perm("website.view_costumer"):
                return redirect("home")
            if user.is_staff:
                return redirect("admin:index")
            if user.has_perm("website.add_costumer"):
                return redirect("add_record")
            return render(request, "login.html", status=403)
        messages.error(request, "There was an error logging in. Please try again.")
    return render(request, "login.html", {"next": next_url})


@login_required
@require_POST
def logout_user(request):
    logout(request)
    return redirect("login")


@login_required
@permission_required("website.view_costumer", raise_exception=True)
def costumer_record(request, pk):
    record = get_object_or_404(Costumer, pk=pk)
    return render(request, "record.html", {"costumer_record": record})


@login_required
@permission_required("website.delete_costumer", raise_exception=True)
@require_POST
def delete_costumer(request, pk):
    get_object_or_404(Costumer, pk=pk).delete()
    messages.success(request, "Record deleted successfully.")
    return redirect("home")


@login_required
@permission_required("website.add_costumer", raise_exception=True)
@require_http_methods(["GET", "POST"])
def add_record(request):
    form = AddRecordForm(request.POST if request.method == "POST" else None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Record added.")
        if request.user.has_perm("website.view_costumer"):
            return redirect("home")
        return redirect("add_record")
    return render(request, "add_record.html", {"form": form})


@login_required
@permission_required("website.change_costumer", raise_exception=True)
@require_http_methods(["GET", "POST"])
def update_costumer(request, pk):
    record = get_object_or_404(Costumer, pk=pk)
    form = AddRecordForm(
        request.POST if request.method == "POST" else None, instance=record
    )
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Record updated.")
        if request.user.has_perm("website.view_costumer"):
            return redirect("record", pk=record.pk)
        return redirect("update_costumer", pk=record.pk)
    return render(request, "update_record.html", {"form": form})


def stars(request):
    return render(request, "stars.html", {})

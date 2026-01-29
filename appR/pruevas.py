from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Orden
from .forms import OrdenForm, ItemOrdenFormSet

@login_required
def orden_create(request):
    if request.method == "POST":
        form = OrdenForm(request.POST)
        formset = ItemOrdenFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            orden = form.save()
            items = formset.save(commit=False)
            for item in items:
                item.orden = orden
                item.save()
            messages.success(request, "Orden registrada correctamente.")
            return redirect("ordenes_list")
    else:
        form = OrdenForm()
        formset = ItemOrdenFormSet()
    return render(request, "appR/orden_form.html", {"form": form, "formset": formset})

@login_required
def orden_edit(request, orden_id):
    orden = get_object_or_404(Orden, id=orden_id)
    if request.method == "POST":
        form = OrdenForm(request.POST, instance=orden)
        formset = ItemOrdenFormSet(request.POST, instance=orden)
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            messages.success(request, "Orden actualizada correctamente.")
            return redirect("orden_detail", orden_id=orden.id)
    else:
        form = OrdenForm(instance=orden)
        formset = ItemOrdenFormSet(instance=orden)
    return render(request, "appR/orden_form.html", {"form": form, "formset": formset, "editando": True})

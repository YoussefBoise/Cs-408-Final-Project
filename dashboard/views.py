from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import ProtectedError

from .models import MenuItem, InventoryItem, Event
from .forms import MenuItemForm, InventoryItemForm, EventForm

def home(request):
    return render(request, "dashboard/home.html")


def menu_list(request):
    items = MenuItem.objects.all().order_by("category", "name")

    return render(request, "dashboard/menu.html", {
        "items": items
    })


def menu_detail(request, pk):
    item = get_object_or_404(MenuItem, pk=pk)

    return render(request, "dashboard/menu_detail.html", {
        "item": item
    })


def menu_create(request):
    form = MenuItemForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        item = form.save()
        return redirect("menu_detail", pk=item.pk)

    return render(request, "dashboard/menu_form.html", {
        "form": form,
        "title": "Add Menu Item"
    })


def menu_edit(request, pk):
    item = get_object_or_404(MenuItem, pk=pk)

    form = MenuItemForm(request.POST or None, instance=item)

    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("menu_detail", pk=item.pk)

    return render(request, "dashboard/menu_form.html", {
        "form": form,
        "title": "Edit Menu Item"
    })


def menu_delete(request, pk):
    item = get_object_or_404(MenuItem, pk=pk)
    error = None

    if request.method == "POST":
        try:
            item.delete()
            return redirect("menu_list")
        except ProtectedError:
            error = (
                "This item cannot be deleted because "
                "it is associated with recorded sales."
            )

    return render(
        request,
        "dashboard/menu_confirm_delete.html",
        {
            "item": item,
            "error": error
        }
    )
    
def inventory_list(request):
    items = InventoryItem.objects.all().order_by("name")

    return render(request, "dashboard/inventory.html", {
        "items": items
    })


def inventory_create(request):
    form = InventoryItemForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("inventory_list")

    return render(request, "dashboard/inventory_form.html", {
        "form": form,
        "title": "Add Inventory Item"
    })


def inventory_edit(request, pk):
    item = get_object_or_404(InventoryItem, pk=pk)

    form = InventoryItemForm(request.POST or None, instance=item)

    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("inventory_list")

    return render(request, "dashboard/inventory_form.html", {
        "form": form,
        "title": "Edit Inventory Item"
    })


def inventory_delete(request, pk):
    item = get_object_or_404(InventoryItem, pk=pk)

    if request.method == "POST":
        item.delete()
        return redirect("inventory_list")

    return render(
        request,
        "dashboard/inventory_confirm_delete.html",
        {"item": item}
    )
    

def event_list(request):
    events = Event.objects.all().order_by("event_date")

    return render(request, "dashboard/events.html", {
        "events": events
    })


def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk)

    return render(request, "dashboard/event_detail.html", {
        "event": event
    })


def event_create(request):
    form = EventForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        event = form.save()
        return redirect("event_detail", pk=event.pk)

    return render(request, "dashboard/event_form.html", {
        "form": form,
        "title": "Add Event"
    })


def event_edit(request, pk):
    event = get_object_or_404(Event, pk=pk)

    form = EventForm(request.POST or None, instance=event)

    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("event_detail", pk=event.pk)

    return render(request, "dashboard/event_form.html", {
        "form": form,
        "title": "Edit Event"
    })


def event_delete(request, pk):
    event = get_object_or_404(Event, pk=pk)

    if request.method == "POST":
        event.delete()
        return redirect("event_list")

    return render(
        request,
        "dashboard/event_confirm_delete.html",
        {"event": event}
    )

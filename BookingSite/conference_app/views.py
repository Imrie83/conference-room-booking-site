from django.shortcuts import render, redirect
from django.http import HttpResponse, response
from django.views import View
from .models import Room, Reservation
from datetime import datetime
from django.contrib import messages


class AddRoomView(View):
    """
    Display form allowing to add a room to database.
    If conditions met create an instance of :model: `conference_app.Room
    and save it to database.

    **Context**

    ``new_room``
        An instance of :model:`conference_app.Room`.

    ``room_name``
        A str variable loaded from template

    ``room_capacity``
        An int variable taken from template

    ``projector``
        A bool variable taken from the template

    **Template:**

    :template:`conference_app/add_room.html`
    """
    def get(self, request):
        return render(request, 'conference_app/add_room.html')

    def post(self, request):
        # Load variables from a from in template
        room_name = request.POST.get('name')
        room_capacity = int(request.POST['capacity'])
        projector = bool(request.POST.get('projector'))

        if room_name:                   # if room name not empty...
            if not room_capacity > 0:   # room capacity cannot be lower than 1
                messages.error(request, 'Capacity has to be greater than 0')
                return redirect("/")
            try:    # create an instance of a model Room, if fails return and pass to template error messages
                new_room = Room.objects.create(name=room_name, capacity=room_capacity, projector=projector)
            except Exception:
                messages.error(request, 'Room already exist')
                return redirect("/")
        else:
            messages.error(request, 'Name required')
            return redirect("/")

        messages.success(request, 'Room added successfully')
        return redirect("/")


class ListAllRoomsView(View):
    """
    Display all elements from :model:`conference_app.Room`.

    **Context**

    ``rooms``
        An instance of :model:`conference_app.Room`.

    **Template:**

    :template:`conference_app/list_rooms.html`
    """
    def get(self, request):
        rooms = Room.objects.all()
        if not rooms:   # If no rooms in database return error
            messages.error(request, 'There are no rooms in database')
            return redirect("/")
        return render(request, 'conference_app/list_rooms.html', {'rooms': rooms})


class DeleteRoomView(View):
    """
    Based on id deletes an element from :model:`conference_app.Room`.

    **Context**

    **Template:**

    """
    def get(self, request, id):
        Room.objects.get(id=id).delete()
        return redirect("/")


class ModifyRoomView(View):
    """
    Display form allowing to modify rooms,
    creates an instance of :model: `conference_app.Room
    and saves it to database if conditions met

    **Context**

    ``room``
        An instance of :model:`conference_app.Room`.

    ``update_room``
        An instance of :model: `conference_app.Room`.

    ``room_name``
        A str variable loaded from template

    ``room_capacity``
        An int variable taken from template

    ``projector``
        A bool variable taken from the template

    **Template:**

    :template:`conference_app/edit_room.html`
    """
    def get(self, request, id):
        room = Room.objects.get(id=id)
        if room:
            return render(request, 'conference_app/edit_room.html', {'room': room})

    def post(self, request, id):
        update_room = Room.objects.get(id=id)

        room_name = request.POST.get('name')
        room_capacity = int(request.POST.get('capacity'))
        projector = bool(request.POST.get('projector'))

        if room_name:
            if not room_capacity > 0:
                messages.error(request, 'Room capacity has to be greater than 0')
                return redirect("/")
            try:
                update_room.name = room_name
                update_room.capacity = room_capacity
                update_room.projector = projector
                update_room.save()
            except Exception as e:
                messages.error(request, 'Room with this name exists')
                return redirect("/")
        else:
            messages.error(request, 'Room requires name')
            return redirect("/")

        messages.success(request, 'Room modified successfully')
        return redirect("/")


class ReserveRoomView(View):
    """
    Creates and saves a new object of :model: conference_app.Reservation

    **Context**

    ``room``
       An instance of :model:`conference_app.Room`.

    ``reservations_check``
       An instance of :model: `conference_app.Reservations`.

    ``date``
        A date variable loaded from template form.

    ``comment``
        A str variable loaded from template form.


    **Template:**

    :template:`conference_app/edit_room.html`
    """
    def get(self, request, id):
        room = Room.objects.get(id=id)
        return render(request, 'conference_app/reserve_room.html', {'room': room})

    def post(self, request, id):
        date = request.POST['date']
        comment = request.POST['comment']

        reservations_check = Reservation.objects.filter(room=id).filter(date=date)

        if not reservations_check:
            if date >= datetime.now().strftime('%Y-%m-%d'):
                Reservation.objects.create(date=date, room_id=id, comment=comment)
            else:
                messages.success(request, 'Date cannot be in the past')
                return redirect("/")
        else:
            messages.success(request, 'Room already booked on this day')
            return redirect("/")

        messages.success(request, 'Room booked successfully')
        return redirect("/")


class DetailedView(View):
    """
    Creates an instance of :model: conference_app.Room

    **Context**

    ``room``
       An instance of :model:`conference_app.Room`.

    **Template:**

    :template:`conference_app/details.html`
    """
    def get(self, request, id):
        room = Room.objects.get(id=id)
        return render(request, 'conference_app/details.html', {'room': room})

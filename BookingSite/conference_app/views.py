from django.shortcuts import render, redirect
from django.http import HttpResponse, response
from django.views import View
from .models import Room, Reservation
from datetime import datetime
from django.contrib import messages


class AddRoomView(View):
    def get(self, request):
        return render(request, 'conference_app/add_room.html')

    def post(self, request):
        room_name = request.POST.get('name')
        room_capacity = int(request.POST['capacity'])
        projector = bool(request.POST.get('projector'))

        if room_name:
            if not room_capacity > 0:
                messages.error(request, 'Capacity has to be greater than 0')
                return redirect("/")
            try:
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
    def get(self, request):
        rooms = Room.objects.all()
        if not rooms:
            messages.success(request, 'There are no rooms in database')
            return redirect("/")
        return render(request, 'conference_app/list_rooms.html', {'rooms': rooms})


class DeleteRoomView(View):
    def get(self, request, id):
        Room.objects.get(id=id).delete()
        return redirect("/")


class ModifyRoomView(View):
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
    def get(self, request, id):
        room = Room.objects.get(id=id)
        return render(request, 'conference_app/details.html', {'room': room})

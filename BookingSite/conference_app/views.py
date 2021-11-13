from django.shortcuts import render
from django.http import HttpResponse, response
from django.views import View
from .models import Room


class AddRoomView(View):
    def get(self, request):
        return render(request, 'conference_app/add_room.html')

    def post(self, request):
        room_name = request.POST.get('name')
        room_capacity = int(request.POST['capacity'])
        projector = bool(request.POST.get('projector'))

        if room_name:
            if not room_capacity > 0:
                return render(request, 'conference_app/add_room.html', {
                    'message': 'Room capacity has to be greater than 0'
                })
            try:
                new_room = Room.objects.create(name=room_name, capacity=room_capacity, projector=projector)
            except Exception:
                return render(request, 'conference_app/add_room.html', {'message': 'Room already exist'})
        else:
            return render(request, 'conference_app/add_room.html', {'message': 'Add room name'})

        return render(request, 'conference_app/add_room.html', {'message': 'Room has been added!'})


class ListAllRoomsView(View):
    def get(self, request):
        rooms = Room.objects.all()
        if not rooms:
            return render(request, 'conference_app/list_rooms.html', {'message': 'There are no rooms in database'})
        return render(request, 'conference_app/list_rooms.html', {'rooms': rooms})


class DeleteRoomView(View):
    def get(self, id):
        Room.objects.get(id=id).delete()
        return render(request, 'conference_app/delete_room.html', {'message': 'Room has been deleted'})


class ModifyRoomView(View):
    def get(self, id):
        room = Room.objects.get(id=id)
        if room:
            return render(request, 'conference_app/edit_room.html', {'room': room})
        else:
            return render(request, 'conference_app/edit_room.html', {'message': 'Room not found'})

    def post(self, id):
        update_room = Room.object.get(id=id)

        room_name = request.POST.get('name')
        room_capacity = int(request.POST['capacity'])
        projector = bool(request.POST.get('projector'))

        if room_name:
            if not room_capacity > 0:
                return render(request, 'conference_app/add_room.html', {
                    'message': 'Room capacity has to be greater than 0'
                })
            try:
                update_room.name = room_name
                update_room.capacity = room_capacity
                update_room.projector = projector
                update_room.save()
            except Exception as e:
                print(e)
                return render(request, 'conference_app/add_room.html', {'message': 'Room with this name exist'})
        else:
            return render(request, 'conference_app/add_room.html', {'message': 'Add room name'})

        return render(request, 'conference_app/add_room.html', {'message': 'Room has been modified!'})


class ReserveRoomView(View):
    def get(self, id):
        pass

    def post(self, id):
        pass
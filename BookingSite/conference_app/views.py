from django.shortcuts import render
from django.http import HttpResponse, response
from django.views import View
from .models import Room


class AddRoomView(View):
    def get(self, request):
        return render(request, 'conference_app/add_room.html')

    def post(self, request):
        # errors = ''
        room_name = request.POST.get('name')
        room_capacity = int(request.POST['capacity'])
        availability = bool(request.POST.get('availability'))

        if room_name:
            if not room_capacity > 0:
                return render(request, 'conference_app/add_room.html', {
                    'message': 'Room capacity has to be greater than 0'
                })
            try:
                new_room = Room.objects.create(name=room_name, capacity=room_capacity, availability=availability)
            except Exception:
                return render(request, 'conference_app/add_room.html', {'message': 'Room already exist'})
        else:
            return render(request, 'conference_app/add_room.html', {'message': 'Add room name'})

        return render(request, 'conference_app/add_room.html', {'message': 'Room has been added!'})
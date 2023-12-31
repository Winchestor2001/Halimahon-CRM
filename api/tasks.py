from __future__ import absolute_import, unicode_literals
from celery import shared_task
from backend.celery import app
from .serializers import PatientSerializer
from .models import *
from datetime import datetime, timedelta


@app.task
def check_patient_rooms():
    year = datetime.now().year
    patient_rooms = Patient.objects.filter(duration__gt=0).filter(created_date__year=year)
    if patient_rooms.exists():
        for room in patient_rooms:
            today = datetime.now().strftime('%m-%d')
            end_date = (room.created_date + timedelta(days=room.duration)).strftime('%m-%d')
            if today >= end_date:
                r = Room.objects.get(id=room.room.id)
                r.room_personal += 1
                room.room_status = True
                room.save()
                r.save()
    return 'SUCCESS'




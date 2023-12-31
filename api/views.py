import json

from rest_framework import generics
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import APIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import *
from .models import *
import jwt
from backend import settings
from datetime import datetime, timedelta
import logging

from .utils import *

logging.basicConfig(level=logging.INFO)


def text_to_slug(name: str):
    slug_name = ""
    name_split = name.split()

    for i in name_split:
        slug_name += i.capitalize()
    return slug_name


def decode_jwt_token(request):
    token = request.META.get('HTTP_AUTHORIZATION')
    if token:
        jwt_token = request.headers['Authorization'].split()[-1]
        return jwt.decode(jwt_token, settings.SECRET_KEY, 'HS256')['username']
    return None


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        staff = Staff.objects.filter(user=user)
        if staff.exists():
            token['position'] = staff[0].position
        token['username'] = user.username

        # ...

        return token


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class HomeAPI(APIView):
    def get(self, request):
        routes = [
            {
                'get_access_token_POST': '/api/token/',
                'refresh_access_token_POST': '/api/token_refresh/',
                'get_staff_POST': '/api/ishchi/',
                'get_doctors_GET': '/api/doctors/',
                'get_staff_POST_AND_GET': '/api/bemorlar/',
                'get_services_GET': '/api/xizmatlar/',
                'get_bemorlar_filter_GET': '/api/bemorlar_filter/',
                'check_pass_data_GET': '/api/check_pass_data/',
            }
        ]
        return Response({'status': 'OK'})


class StaffLoginAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        username = decode_jwt_token(request)
        staff = Staff.objects.filter(user__username=username)
        if staff.exists():
            staff = Staff.objects.get(user__username=username)
            serialize = StaffSerializer(staff)
            is_boss = False
        else:
            user = get_object_or_404(User, username=username)
            serialize = UserSerializer(user)
            is_boss = True
        try:
            last_patient = Patient.objects.latest('id').id
        except:
            last_patient = 0
        return Response({'status': 'OK', 'info': serialize.data, 'last_id': int(last_patient) + 1})


class PatientProfileAPI(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        patient = Patient.objects.get(pk=pk)
        serialize = PatientSerializer(patient)

        return Response({'status': 'OK', 'info': serialize.data})

    def put(self, request, *args, **kwargs):
        patient_id = kwargs.get('pk')
        patient_room = Patient.objects.get(id=patient_id)
        r = Room.objects.get(id=patient_room.room.id)
        r.room_personal += 1
        patient_room.room_status = True
        patient_room.save()
        r.save()
        return Response({"status": "OK"}, status=200)


class PatientAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        patient = Patient.objects.all()
        serialize = PatientSerializer(patient)
        return Response({'status': 'OK', 'info': serialize.data})

    def post(self, request):
        doctor = request.data['doctor']
        aparat = request.data['aparat']
        tahlil = request.data['tahlil']
        child_tahlil = request.data['child_tahlil']
        full_name = request.data['full_name']
        pass_data = request.data['pass_data']
        phone_number = request.data['phone_number']
        address = request.data['address']
        workplace = request.data['workplace']
        inspaction = request.data['inspaction']
        birthday = datetime.strptime(request.data['birthday'], '%Y-%m-%d')
        room_number = request.data['room_number']
        duration = request.data['duration']
        staff = Staff.objects.get(user__username=decode_jwt_token(request))
        # staff = Staff.objects.get(user__username='root2')

        if doctor:
            doctor = Staff.objects.get(pk=doctor)
            patient = Patient.objects.create(
                slug_name=text_to_slug(full_name),
                doctor=doctor, full_name=full_name, pass_data=pass_data,
                phone_number=phone_number, address=address, workplace=workplace,
                staff=staff, inspaction=inspaction, birthday=birthday
                )
        else:
            patient = Patient.objects.create(
                slug_name=text_to_slug(full_name),
                full_name=full_name, pass_data=pass_data,
                phone_number=phone_number, address=address, workplace=workplace,
                staff=staff, inspaction=inspaction, birthday=birthday
            )
        if len(room_number) > 0:
            room = Room.objects.get(pk=room_number)
            patient.room = room
            patient.duration = duration
            room.room_personal -= 1
            room.save()

        if len(tahlil) > 0:
            for t in tahlil:
                s = Service.objects.get(id=t)
                all_services = Service.objects.filter(service_id=s.service_id)

                for s in all_services:
                    ser = PatientService.objects.create(
                        patient=patient, service=s, is_checked=True
                    )
                    if s.tab_visible:
                        Analysis.objects.create(
                            patient=patient, service=ser, is_checked=True
                        )

        if len(child_tahlil) > 0:
            for t in child_tahlil:
                services = Service.objects.filter(service_id=t['service'])

                for s in services:

                    if s.id in t['child']:
                        is_checked = True
                    else:
                        is_checked = False

                    ser = PatientService.objects.create(
                        patient=patient, service=s, is_checked=is_checked
                    )
                    Analysis.objects.create(
                        patient=patient, service=ser, is_checked=is_checked
                    )

        if len(aparat) > 0:
            for a in aparat:
                patient.instrumental_service.add(a)

        patient.save()
        patient = Patient.objects.get(id=patient.id)
        serializer = PatientSerializer(instance=patient)

        return Response(serializer.data, status=201)


class ServiceAPI(APIView):
    def get(self, request):
        service1 = InstrumentalService.objects.all()
        service2 = MainService.objects.all()
        serialize1 = InstrumentalServiceSerializer(service1, many=True)
        serialize2 = MainServiceSerializer(service2, many=True)

        services_2 = child_services(serialize2.data)

        return Response(
            {
                'status': 'OK',
                'instrumental_service': serialize1.data,
                'analysis_service': services_2,
            }
        )


class RoomsAPI(APIView):
    def get(self, request):
        rooms = Room.objects.filter(room_personal__gt=0)
        serializer = RoomsSerializer(data=rooms, many=True)
        serializer.is_valid()
        return Response({'status': 'OK', 'rooms': serializer.data})


class AllStaffAPI(APIView):
    def get(self, request):
        doctors = Staff.objects.filter(position='doctor')
        serialize = StaffSerializer(doctors, many=True)
        return Response({'status': 'OK', 'doctors': serialize.data})


class PetientFilterAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.GET:
            inspaction = request.GET.get('rejim').capitalize()
            from_date = datetime.strptime(request.GET.get('from'), '%Y-%m-%d')
            service = request.GET.get('service')
            doctor = request.GET.get('doctor')
            to_date = datetime.strptime(request.GET.get('to'), '%Y-%m-%d') + timedelta(days=1)
            if doctor == "Barchasi":
                if inspaction == 'Rejim' and from_date == to_date:
                    patients = Patient.objects.filter(created_date=from_date).order_by(
                        'created_date')

                elif inspaction == 'Rejim' and from_date != to_date:
                    patients = Patient.objects.filter(created_date__range=[from_date, to_date]).order_by(
                        'created_date')

                elif from_date == to_date:
                    patients = Patient.objects.filter(inspaction=inspaction).filter(created_date=from_date).order_by(
                        'created_date')
                else:
                    patients = Patient.objects.filter(inspaction=inspaction).filter(
                        created_date__range=[from_date, to_date]).order_by('created_date')
                if service != 'Barchasi':
                    service = MainService.objects.get(pk=service)
                    main_services = PatientService.objects.filter(service__service_id__id=service.id)
                    if main_services.exists():
                        patient_ids = [item.patient.id for item in
                                       PatientService.objects.filter(service__service_id__id=service.id)]
                        if from_date == to_date:
                            patients = patients.filter(pk__in=patient_ids).filter(created_date=from_date).order_by(
                                'created_date')
                        else:
                            patients = patients.filter(pk__in=patient_ids).filter(
                                created_date__range=[from_date, to_date]).order_by('created_date')
            else:
                doctor = Staff.objects.get(id=doctor)
                patients = Patient.objects.filter(doctor=doctor).order_by('-created_date')

            serialize = PatientSerializer(patients, many=True)
            return Response({'status': 'OK', 'info': serialize.data})
        return Response({'status': 'ERROR'})


class AnalysisAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        patient = Patient.objects.all()
        serializer = PatientSerializer(patient, many=True)
        services = ServiceSerializer(data=Service.objects.all(), many=True)

        service2 = MainService.objects.all()
        serialize2 = MainServiceSerializer(service2, many=True)
        services_2 = child_services(serialize2.data)

        return Response({'status': 'OK', 'patient_analysis': services_2})

    def put(self, request):
        patient = Patient.objects.get(pk=request.data.get('patientId'))
        analysis = request.data.get('analysis')
        for a in analysis:
            analysis = Analysis.objects.get(id=a['analysis_id'], patient=patient)
            analysis.result = a['result']
            analysis.save()
        has_results = update_analysis_status(patient.id)
        patient.analysis_status = has_results
        patient.save()

        serialize = PatientSerializer(patient)
        return Response({'status': 'OK', 'info': serialize.data})


class DoctorConclusionAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        username = decode_jwt_token(request)
        staff = Staff.objects.get(user__username=username)
        patient = Patient.objects.filter(doctor=staff)
        serializer = PatientSerializer(patient, many=True)
        return Response({'status': 'OK', 'info': serializer.data})

    def post(self, request):
        patient_id = request.data.get("patientId")
        conclusion = request.data.get("conclusion")
        patient = Patient.objects.get(pk=patient_id)
        patient.doctor_status = True
        patient.conclusion = conclusion
        patient.save()
        return Response({'status': 'OK'})


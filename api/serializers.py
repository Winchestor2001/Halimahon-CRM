from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Staff, Patient, Service, Room, Analysis, MainService, InstrumentalService, PatientService
from collections import OrderedDict, defaultdict
from itertools import chain


class StaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = Staff
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username',)


class InstrumentalServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstrumentalService
        fields = '__all__'


class MainServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = MainService
        fields = '__all__'

    def get_children(self, obj):
        i = ServiceSerializer(data=obj.service_set.all(), many=True)
        i.is_valid()

        return i.data

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['children'] = self.get_children(instance)
        return ret


class ServiceSerializer(serializers.ModelSerializer):
    service_id = MainServiceSerializer

    class Meta:
        model = Service
        fields = '__all__'

    def get_cat_name(self, obj):
        a = Service.objects.get(id=obj.id)

        return a.service_id

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['service_id'] = str(self.get_cat_name(instance))

        return ret


class RoomsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'


# class AnalysisForPatientSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Analysis
#         fields = '__all__'


class InstrumentalServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstrumentalService
        fields = '__all__'


class PatientServiceSerializer(serializers.ModelSerializer):
    service = ServiceSerializer()

    class Meta:
        model = PatientService
        fields = '__all__'


class PatientSerializer(serializers.ModelSerializer):
    room = RoomsSerializer()
    instrumental_service = InstrumentalServiceSerializer(many=True)
    doctor = StaffSerializer()

    class Meta:
        model = Patient
        fields = '__all__'

    def get_patient_services(self, obj):
        services = PatientServiceSerializer(
            instance=PatientService.objects.filter(
                patient__id=obj.id, service__rec_visible=True,
                service__tab_visible__in=[True, False]),
            many=True
        )
        return services.data

    def get_patient_analysis(self, obj):
        analysis = AnalysisSerializer(instance=Analysis.objects.filter(patient__id=obj.id), many=True)
        return analysis.data

    def to_representation(self, instance):
        ret = super().to_representation(instance)

        analysis_services = self.get_patient_analysis(instance)
        for i, service in enumerate(analysis_services):
            s = PatientService.objects.get(id=service['service'])
            analysis_services[i]['service'] = OrderedDict(
                [
                    ('id', s.service.id),
                    ('service_name', s.service.service_name),
                    ('service_unit', s.service.service_unit),
                    ('service_norm', s.service.service_norm),
                    ('service_price', s.service.service_price),
                    ('rec_visible', s.service.rec_visible),
                    ('tab_visible', s.service.tab_visible),
                    ('service_id', s.service.service_id.service_name),
                ]
            )
        a = test(analysis_services)
        ret['services'] = self.get_patient_services(instance)
        ret['analysis'] = a
        return ret


class AnalysisSerializer(serializers.ModelSerializer):
    service = ServiceSerializer

    class Meta:
        model = Analysis
        fields = '__all__'


def test(analysis_data):
    grouped_data = defaultdict(list)
    for entry in analysis_data:
        service_info = entry.get('service')
        if isinstance(service_info, dict):
            service_id = service_info.get('service_id')
            if service_id is not None:
                grouped_data[service_id].append(entry)

    transformed_result = []
    for service_id, entries in grouped_data.items():
        children = []
        for entry in entries:
            service_info = entry.get('service')
            if isinstance(service_info, dict):
                child_entry = {
                    "id": entry['id'],
                    "result": entry['result'],
                    "created_date": entry['created_date'],
                    "patient": entry['patient'],
                    "is_checked": entry['is_checked'],
                    "service": {
                        "id": service_info['id'],
                        "service_name": service_info['service_name'],
                        "service_unit": service_info['service_unit'],
                        "service_norm": service_info['service_norm'],
                        "service_price": service_info['service_price'],
                        "rec_visible": service_info['rec_visible'],
                        "tab_visible": service_info['tab_visible'],
                        "service_id": service_id  # Assign the service_id here
                    }
                }
                children.append(child_entry)

        transformed_entry = {
            "service_name": service_id,
            "children": children
        }

        transformed_result.append(transformed_entry)
    return transformed_result

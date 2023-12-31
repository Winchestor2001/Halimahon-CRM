from itertools import groupby
from django.db.models import Q

from .models import MainService, Analysis, Patient, Service
from .serializers import AnalysisSerializer
from collections import OrderedDict


def child_services(obj):
    result = []
    for item in obj:
        if dict(item).get('children', False):
            result.append(item)

    return result


def filter_service_head(data):
    services = []
    single_service = []
    for item in data:
        service = Service.objects.filter(service_name=item["service_id"], tab_visible=False)
        if not service.exists():
            services.append(item)
        else:
            single_service.extend(service)
    if single_service:
        service_ordered_dict = OrderedDict(
            [
                ('id', single_service[0].id),
                ('service_name', single_service[0].service_name),
                ('service_unit', single_service[0].service_unit),
                ('service_norm', single_service[0].service_norm),
                ('service_price', single_service[0].service_price),
                ('is_checked', single_service[0].is_checked),
                ('rec_visible', single_service[0].rec_visible),
                ('service_id', single_service[0].service_id.service_name),
            ]
        )
        combined_list = services + [service_ordered_dict]
        return combined_list

    return services


def child_analysis_services(data, analysis, services):
    grouped_services = []
    new_analysis = []
    new_services = []
    for service_item in services:
        # print(dict(service_item))
        service_id_to_check = service_item['id']
        is_checked = any(analysis_item['service']['id'] == service_id_to_check for analysis_item in analysis if
                         'service' in analysis_item)

        new_service = service_item.copy()
        analysis_result = [item['result'] for item in analysis if item['service']['id'] == service_id_to_check]
        new_service['is_checked'] = is_checked
        if is_checked:
            new_services.append(service_item)
        new_service['result'] = analysis_result[0] if analysis_result else ""
        new_analysis.append(new_service)

    grouped_result = groupby(sorted(new_analysis, key=lambda x: x['service_id']), key=lambda x: x['service_id'])

    for service_id, group in grouped_result:
        services_group = list(group)
        main_service = MainService.objects.get(service_name=service_id)

        if main_service.service_name == 'Бошқа текширувлар':
            services_group = [service for service in services_group if service['is_checked']]

        if services_group:
            have_childer = [item for item in services_group if item['is_checked']]
            if have_childer:
                grouped_services.append({'service_id': main_service.service_name, 'children': services_group})

    new_services = filter_service_head(new_services)
    data['analysis'] = grouped_services
    data['service'] = new_services

    return data


def child_analysis_services2(data, services):
    result = []

    for i in data:
        analysis_serializer = AnalysisSerializer(
            instance=Analysis.objects.filter(patient__pk=i['id']), many=True
        )
        analysis_data = analysis_serializer.data

        grouped_services = []
        new_services = []
        for service_item in services:
            service_id_to_check = service_item['id']
            is_checked = any(
                analysis_item['service']['id'] == service_id_to_check
                for analysis_item in analysis_data if 'service' in analysis_item
            )

            analysis_result = [item['result'] for item in analysis_data if item['service']['id'] == service_id_to_check]
            new_service = service_item.copy()
            new_service['is_checked'] = is_checked
            if is_checked:
                service_item['is_checked'] = is_checked
                new_services.append(service_item)
            new_service['result'] = analysis_result[0] if analysis_result else ""
            i['analysis'].append(new_service)

        grouped_result = groupby(sorted(i['analysis'], key=lambda x: x['service_id']), key=lambda x: x['service_id'])

        for service_id, group in grouped_result:
            services_group = list(group)
            main_service = MainService.objects.get(id=service_id)

            if main_service.service_name == 'Бошқа текширувлар':
                services_group = [service for service in services_group if service['is_checked']]

            if services_group:
                grouped_services.append({'service_id': main_service.service_name, 'children': services_group})

        new_services = filter_service_head(new_services)
        i['analysis'] = grouped_services
        i['service'] = new_services
        result.append(i)

    return result


def update_analysis_status(patient):
    has_results = Analysis.objects.filter(
        patient=patient,
        result=None, is_checked=True).exists()

    has_results = False if has_results else True
    return has_results


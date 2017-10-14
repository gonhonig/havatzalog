from django.shortcuts import render, reverse, redirect
from panel.models import Cut
from django.db.models import Q
from .tables import ResultsTable
from django_tables2.config import RequestConfig
from django_tables2.export.export import TableExport
import datetime


def search_view(request):
    results = None
    url = request.get_full_path()
    count = url.count('select')
    queries = []
    if count > 0:
        for i in range(1, count+1):
            operator = request.GET.get('operator'+str(i)) or None
            field = request.GET.get('select'+str(i))
            value = request.GET.get('field'+str(i))
            if field == 'tags__name__in':
                values_list = value.split(', ')
                value = values_list
            if field == 'updated_time__range':
                dates = value.split(' - ')
                start = datetime.date(*[int(x) for x in dates[0].split('/')])
                end = datetime.date(*[int(x) for x in dates[1].split('/')])
                end = end + datetime.timedelta(days=1)
                value = [start, end]
            queries.append({
                'operator': operator,
                'field': field,
                'value': value,
            })
        query = Q(**{queries[0]['field']: queries[0]['value']})

        for item in queries[1:]:
            if item['operator'] == 'or':
                query.add(Q(**{item['field']: item['value']}), Q.OR)
            else:
                query.add(Q(**{item['field']: item['value']}), Q.AND)
        results = ResultsTable(Cut.objects.filter(pupil__can_read=request.user).filter(query).distinct())
        RequestConfig(request).configure(results)
        export_format = request.GET.get('_export', None)
        if TableExport.is_valid_format(export_format):
            exporter = TableExport(export_format, results)
            return exporter.response('table.{}'.format(export_format))

    context = {
        'title': 'הפאנל',
        'nbar': 'search',
        'results': results
    }
    return render(request, 'search/search.html', context)



# def old_search_view(request):
#     query = request.GET.get('q')
#     tags = request.GET.get('t')
#     pupils = request.GET.get('pu')
#     parameters = request.GET.get('pa')
#     content = request.GET.get('c')
#     tags_q, pupils_q, parameters_q, content_q = Cut.objects.none(), Cut.objects.none(), Cut.objects.none(), Cut.objects.none()
#     results = None
#     if query:
#         query_list = query.split(', ')
#         if tags:
#             print(query_list)
#             tags_q = Cut.objects.filter(tags__name__in=query_list)
#         if pupils:
#             pupils_q = Cut.objects.filter(pupil__first_name__contains=query, pupil__last_name__contains=query)
#         if parameters:
#             parameters_q = Cut.objects.filter(parameter__name__contains=query, parameter__category__contains=query)
#         if content:
#             content_q = Cut.objects.filter(details__contains=query)
#         results = tags_q | pupils_q | parameters_q | content_q
#         results.distinct()
#         results = CutTable(results)
#     context = {
#         'title': 'הפאנל',
#         'nbar': 'search',
#         'results': results
#     }
#     return render(request, 'search/search2.html', context)
from django.shortcuts import render
from django.db.models import Q
from .tables import ExportEvents, ExportCuts
from panel.models import Cut, Event

from django_tables2.config import RequestConfig
from django_tables2.export.export import TableExport


def export(request):
    config = RequestConfig(request)
    cuts_export = ExportCuts(
        Cut.objects.filter(pupil__can_read=request.user).exclude(Q(private=True)&~Q(updated_by=request.user)),
        prefix='cuts'
    )
    events_export = ExportEvents(
        Event.objects.filter(pupil__can_read=request.user),
        prefix='events'
    )
    config.configure(cuts_export)
    config.configure(events_export)
    export_format = request.GET.get('_export', None)
    model = request.GET.get('model', None)
    if TableExport.is_valid_format(export_format):
        if model == 'update':
            exporter = TableExport(export_format, cuts_export)
            return exporter.response('updates.{}'.format(export_format))
        elif model == 'event':
            exporter = TableExport(export_format, events_export)
            return exporter.response('events.{}'.format(export_format))

    return render(request, 'export/export.html', {})
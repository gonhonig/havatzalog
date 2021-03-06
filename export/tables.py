import django_tables2 as tables
from panel.models import Cut, Event


class ExportEvents(tables.Table):
    class Meta:
        model = Event
        fields = ('pupil', 'headline', 'details', 'date', 'updated_by')


class ExportCuts(tables.Table):
    class Meta:
        model = Cut
        fields = ('pupil', 'headline', 'parameter', 'details', 'event', 'status', 'updated_time', 'updated_by', 'private', 'comments')
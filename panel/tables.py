import django_tables2 as tables
from panel.models import Cut, Event


class ExportEvents(tables.Table):
    class Meta:
        model = Event
        fields = ('pupil', 'headline', 'details', 'date', 'updated_by')


class ExportCuts(tables.Table):
    class Meta:
        model = Cut
        fields = ('pupil', 'parameter', 'headline', 'details', 'status', 'updated_time', 'updated_by', 'private', 'event')

    def get_queryset(self, request):
        return super(ExportCuts, self).get_queryset(request).prefetch_related('tags')

    def tag_list(self, obj):
        return u", ".join(o.name for o in obj.tags.all())
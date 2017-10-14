import django_tables2 as tables
from panel.models import Cut


class ResultsTable(tables.Table):
    class Meta:
        model = Cut
        fields = ('pupil', 'parameter', 'headline', 'status', 'trend', 'updated_time', 'updated_by')
        attrs = {'class': 'table table-sm table-hover margin-top-05', 'width': '100%', 'th': {'class': 'text-align-right'}, 'td': {'class': 'text-align-right'}}
from  django.shortcuts import render, HttpResponseRedirect
from django.contrib import admin
from .models import Pupil, Cut, Parameter
from .forms import PremAddForm
from django.contrib.auth.models import User


class CutAdmin(admin.ModelAdmin):
    list_display = ('pupil', 'headline', 'status', 'trend', 'updated_time')
    list_filter = ('pupil', 'parameter', 'status', 'trend', 'updated_by')


class PupilAdmin(admin.ModelAdmin):
    list_display = ('name', 'year', 'platoon')
    filter_horizontal = ('can_read',)
    list_filter = ('year', 'platoon', 'can_read')
    actions = ['add_admin', 'prem_add']

    def add_admin(self, request, queryset):
        the_admin = User.objects.get(username='gonhonig')
        for pupil in queryset:
            pupil.can_read.add(the_admin)
    add_admin.short_description = "הוסף הרשאות למנהל"

    def prem_add(self, request, queryset):
        if "apply" in request.POST:
            print('entered--')
            form = PremAddForm(request.POST)
            if form.is_valid():
                print('entered')
                to_add = form.cleaned_data['to_add']
                count = 0
                for pupil in queryset:
                    pupil.can_read.add(to_add)
                    pupil.save()
                    count += 1
                self.message_user(request, "%s חניכים עודכנו" % count)
                return
        else:
            print('not entered')
            form = PremAddForm()
        return render(request, 'panel/action_form.html', {'form': form})
    prem_add.short_description = "הוספת מורשים"


class ParameterAdmin(admin.ModelAdmin):
    list_display = ('name', 'category')
    list_filter = ('category',)



admin.site.register(Pupil, PupilAdmin)
admin.site.register(Parameter, ParameterAdmin)
admin.site.register(Cut, CutAdmin)


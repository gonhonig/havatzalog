from django.shortcuts import render, reverse, redirect
from datetime import datetime
from .forms import *
from .models import Cut, Pupil, Parameter
from django.views.generic.edit import UpdateView, DeleteView
from django.db.models import Count


def selector(request, extra = None):
    if request.user.is_authenticated:
        all_pupils = Pupil.objects.filter(can_read=request.user)
    else:
        all_pupils = None

    context = {
        'title': 'הפאנל',
        'nbar': 'panel',
        'all_pupils': all_pupils,
    }
    if extra:
        context['extra'] = extra
    return render(request, 'panel/selector.html', context)


def pupil(request, pupil_id):
    the_user = request.user
    the_pupil = Pupil.objects.get(pk=pupil_id)
    if the_pupil not in the_user.pupil_set.all():
        return selector(request, 'אל תנסה/י לצפות בחניכים שאינך מורשה אליהם!')
    recent_view = request.GET.get('recent')

    if recent_view == 'on':
        view_type = 'recent'
        cuts_ids = {}
        all_parameters = Parameter.objects.filter(cut__pupil=pupil_id).distinct()
        for the_parameter in all_parameters:
            parameter_cuts = Cut.objects.filter(pupil=the_pupil, parameter=the_parameter)
            the_cut = parameter_cuts.order_by('-updated_time')[0]
            if the_cut.pk not in cuts_ids:
                cuts_ids[the_cut.pk] = [the_parameter]
            else:
                cuts_ids[the_cut.pk].append(the_parameter)
        the_queryset = Cut.objects.filter(id__in=cuts_ids.keys()).order_by('-updated_time')
        all_cuts = []
        for the_cut in the_queryset:
            for the_parameter in cuts_ids[the_cut.pk]:
                parameter_cuts = Cut.objects.filter(pupil=the_pupil, parameter=the_parameter)
                frequency_list = parameter_cuts.values_list('status').annotate(freq=Count('status')).order_by('-freq')
                frequent_status = frequency_list[0][0]
                all_cuts.append({'parameter': the_parameter, 'cut': the_cut,'freq': frequent_status})

    else:
        view_type = 'mashov'
        all_cuts = {}
        categories = ('התנהלות מקצועית', 'חשיבה והצגה', 'ערכים', 'פיקוד ומנהיגות', 'קבוצה ובין אישי', 'יעדים', 'אחר')
        pupils_cuts = Cut.objects.filter(pupil=pupil_id)
        for category in categories:
            all_cuts[category] = []
            for the_parameter in Parameter.objects.filter(cut__pupil=pupil_id, category=category).distinct():
                parameter_cuts = the_parameter.cut_set.all()
                frequency_list = parameter_cuts.values_list('status').annotate(freq=Count('status')).order_by('-freq')
                frequent_status = frequency_list[0][0]
                the_cut = pupils_cuts.filter(parameter=the_parameter).order_by('-updated_time')[0]
                all_cuts[category].append({'parameter': the_parameter, 'cut': the_cut,'freq': frequent_status})

    context = {
        'pupil': the_pupil,
        'nbar': 'panel',
        'view_type': view_type,
        'all_cuts': all_cuts,
        'all_pupils': Pupil.objects.filter(can_read=request.user),
    }
    return render(request, 'panel/pupil.html', context)


def parameter(request, pupil_id, parameter_id):
    the_user = request.user
    the_pupil = Pupil.objects.get(pk=pupil_id)
    if the_pupil not in the_user.pupil_set.all():
        return selector(request, 'אל תנסה/י לצפות בחניכים שאינך מורשה אליהם!')
    the_parameter = Parameter.objects.get(pk=parameter_id)
    context = {
        'pupil': the_pupil,
        'parameter': the_parameter,
        'nbar': 'panel',
        'all_cuts': the_pupil.cut_set.filter(parameter=parameter_id)
    }
    return render(request, 'panel/parameter.html', context)


def cut_create(request, pupil_id):
    form = CutForm(request.POST or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.pupil = Pupil.objects.get(pk=pupil_id)
        instance.updated_time = datetime.now()
        instance.updated_by = request.user.first_name + ' ' + request.user.last_name
        if not form.cleaned_data['headline']:
            instance.headline = form.cleaned_data['details'][:40]
        instance.save()
        form.save_m2m()
        return redirect(reverse('panel:pupil', kwargs={'pupil_id': instance.pupil.pk}))

    form.fields['parameter'].widget.attrs['multiple'] = "multiple"
    form.fields['parameter'].widget.attrs['class'] = "select2"
    context = {
        'form': form,
        'pupil': Pupil.objects.get(pk=pupil_id),
        'parameter': 'לבחירתך'
    }
    return render(request, 'panel/cut_form.html', context)


def cut_create_specific(request, pupil_id, parameter_id):
    form = CutFormSpecific(request.POST or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.pupil = Pupil.objects.get(pk=pupil_id)
        instance.updated_time = datetime.now()
        instance.updated_by = request.user.first_name + ' ' + request.user.last_name
        if not form.cleaned_data['headline']:
            instance.headline = form.cleaned_data['details'][:40]
        instance.save()
        instance.parameter.add(Parameter.objects.get(pk=parameter_id))
        instance.save()
        form.save_m2m()
        return redirect(reverse('panel:parameter', kwargs={'pupil_id': instance.pupil.pk, 'parameter_id': parameter_id}))

    context = {
        'form': form,
        'pupil': Pupil.objects.get(pk=pupil_id),
        'parameter': Parameter.objects.get(pk=parameter_id)
    }
    return render(request, 'panel/cut_form.html', context)


def pupil_create(request):
    form = PupilForm(request.POST or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        form.save_m2m()
        return redirect(reverse('panel:pupil', kwargs={'pupil_id': instance.id}))

    can_read_choices = ()
    for user in form.fields['can_read'].queryset:
        can_read_choices += ((str(user.pk), user.first_name + ' ' + user.last_name),)
    form.fields['can_read'].choices = can_read_choices

    context = {
        'form': form,
    }
    return render(request, 'panel/pupil_form.html', context)


class ChangePermissions(UpdateView):
    model = Pupil
    form_class = ChangePermissionsForm
    template_name = 'panel/change_permissions_form.html'

    def get_success_url(self):
        return reverse('panel:pupil', kwargs={'pupil_id': self.object.pk})

    def get_form(self, form_class=None):
        form = super(ChangePermissions, self).get_form(form_class)
        can_read_choices = ()
        for user in form.fields['can_read'].queryset:
            can_read_choices += ((str(user.pk), user.first_name + ' ' + user.last_name),)
        form.fields['can_read'].choices = can_read_choices
        return form

    def dispatch(self, request, *args, **kwargs):
        the_user = request.user
        the_pupil = Pupil.objects.get(pk=int(kwargs['pk']))
        if the_pupil not in the_user.pupil_set.all():
            return selector(request, 'אל תנסה/י לערוך חניכים שאינך מורשה אליהם!')
        return super(ChangePermissions, self).dispatch(request, *args, **kwargs)


def parameter_create(request, pupil_id):
    form = ParameterForm(request.POST or None)
    if form.is_valid():
        instance = form.save()
        return redirect(reverse('panel:cut-add-specific', kwargs={'pupil_id': pupil_id, 'parameter_id': instance.id}))
    form.fields['category'].widget.attrs['class'] = "select2"
    context = {
        'form': form
    }
    return render(request, 'panel/parameter_form.html', context)


def cut_delete(request, pupil_id, parameter_id, cut_id):
    the_cut = Cut.objects.get(pk = cut_id)
    the_cut.delete()
    return redirect(reverse('panel:parameter', kwargs={'pupil_id': pupil_id, 'parameter_id': parameter_id}))



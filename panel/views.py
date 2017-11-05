import datetime

from django.contrib.contenttypes.models import ContentType
from django.db.models import Count
from django.forms import modelformset_factory
from django.forms.models import model_to_dict
from django.shortcuts import render, reverse, redirect
from notifications.signals import notify

from comments.forms import CommentForm
from comments.models import Comment
from .forms import *
from .models import Cut, Pupil, Parameter


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
                count = parameter_cuts.count()
                all_cuts.append({'parameter': the_parameter, 'cut': the_cut,'freq': frequent_status, 'count': count})

    else:
        view_type = 'mashov'
        all_cuts = {}
        categories = ('יעדים', 'התנהלות מקצועית', 'חשיבה והצגה', 'ערכים', 'פיקוד ומנהיגות', 'קבוצה ובין אישי', 'אחר')
        pupils_cuts = Cut.objects.filter(pupil=pupil_id)
        for category in categories:
            all_cuts[category] = []
            for the_parameter in Parameter.objects.filter(cut__pupil=pupil_id, category=category).distinct():
                parameter_cuts = the_parameter.cut_set.filter(pupil=the_pupil)
                frequency_list = parameter_cuts.values_list('status').annotate(freq=Count('status')).order_by('-freq')
                frequent_status = frequency_list[0][0]
                the_cut = pupils_cuts.filter(parameter=the_parameter).order_by('-updated_time')[0]
                count = parameter_cuts.count()
                all_cuts[category].append({'parameter': the_parameter, 'cut': the_cut,'freq': frequent_status, 'count': count})
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

    comment_form = CommentForm(request.POST or None)
    if comment_form.is_valid():
        object_id = request.POST['cut_id']
        content_type = ContentType.objects.get_for_model(Cut)
        content = comment_form.cleaned_data.get("content")
        new_comment, created = Comment.objects.get_or_create(
            user = the_user,
            content_type = content_type,
            object_id = object_id,
            content = content,
        )

        recipients = the_pupil.can_read.exclude(pk=the_user.pk)
        if recipients:
            the_cut = Cut.objects.get(pk=object_id)
            user_name = "{} {} ".format(the_user.first_name, the_user.last_name)
            message = '<strong>{}</strong> הגיב/ה על העדכון <strong>{}</strong> השייך ל<strong>{}</strong>'.format(user_name,
                                                                                                                 the_cut.headline,
                                                                                                                 the_pupil.name)
            notify.send(
                sender=the_user,
                recipient=recipients,
                verb=message,
                action_object=new_comment,
                target=the_pupil,
                description='/panel/{}/{}'.format(pupil_id, parameter_id)
            )

        return redirect(reverse('panel:parameter', kwargs={'pupil_id': pupil_id, 'parameter_id': parameter_id}))

    context = {
        'pupil': the_pupil,
        'parameter': the_parameter,
        'nbar': 'panel',
        'all_cuts': the_pupil.cut_set.filter(parameter=parameter_id),
        'comment_form': comment_form,
    }
    return render(request, 'panel/parameter.html', context)


def events(request, pupil_id):
    the_user = request.user
    the_pupil = Pupil.objects.get(pk=pupil_id)
    if the_pupil not in the_user.pupil_set.all():
        return selector(request, 'אל תנסה/י לצפות בחניכים שאינך מורשה אליהם!')

    context = {
        'pupil': the_pupil,
        'nbar': 'panel',
        'all_events': the_pupil.event_set.all().order_by('date')
    }
    return render(request, 'panel/events.html', context)


def event(request, pupil_id, event_id):
    the_user = request.user
    the_pupil = Pupil.objects.get(pk=pupil_id)
    if the_pupil not in the_user.pupil_set.all():
        return selector(request, 'אל תנסה/י לצפות בחניכים שאינך מורשה אליהם!')
    the_event = Event.objects.get(pk=event_id)

    comment_form = CommentForm(request.POST or None)
    if comment_form.is_valid():
        try:
            object_id = request.POST['cut_id']
            content_type = ContentType.objects.get_for_model(Cut)
            the_object = Cut.objects.get(pk=object_id)
            notif = 'העדכון'
        except:
            object_id = request.POST['event_id']
            content_type = ContentType.objects.get_for_model(Event)
            the_object = Event.objects.get(pk=object_id)
            notif = 'האירוע'
        content = comment_form.cleaned_data.get("content")
        new_comment, created = Comment.objects.get_or_create(
            user=the_user,
            content_type=content_type,
            object_id=object_id,
            content=content,
        )

        recipients = the_pupil.can_read.exclude(pk=the_user.pk)
        if recipients:
            user_name = "{} {} ".format(the_user.first_name, the_user.last_name)
            message = '<strong>{}</strong> הגיב/ה על {} <strong>{}</strong> השייך ל<strong>{}</strong>'.format(user_name,
                                                                                                             notif,
                                                                                                             the_object.headline,
                                                                                                             the_pupil.name)
            notify.send(
                sender=the_user,
                recipient=recipients,
                verb=message,
                action_object=new_comment,
                target=the_pupil,
                description='/panel/{}/events/{}'.format(pupil_id, event_id)
            )

        return redirect(reverse('panel:event', kwargs={'pupil_id': pupil_id, 'event_id': event_id}))

    context = {
        'pupil': the_pupil,
        'event': the_event,
        'nbar': 'panel',
        'all_cuts': the_pupil.cut_set.filter(event_id=event_id),
        'comment_form': comment_form
    }
    return render(request, 'panel/event.html', context)


def cut_create(request, pupil_id):
    the_user = request.user
    the_pupil = Pupil.objects.get(pk=pupil_id)
    form = CutForm(request.POST or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.pupil = the_pupil
        instance.updated_time = datetime.datetime.now()
        instance.updated_by = request.user
        if not form.cleaned_data['headline']:
            instance.headline = form.cleaned_data['details'][:40]
        instance.save()
        form.save_m2m()

        recipients = the_pupil.can_read.exclude(pk=the_user.pk)
        if recipients:
            user_name = "{} {} ".format(the_user.first_name, the_user.last_name)
            message = '<strong>{}</strong> הוסיף/ה עדכון ל<strong>{}</strong>: <i>{}</i>'.format(user_name, the_pupil.name,
                                                                                                 instance.headline)
            notify.send(
                sender=the_user,
                recipient=recipients,
                verb=message,
                action_object=instance,
                target=the_pupil,
                description='/panel/{}/{}'.format(pupil_id, instance.parameter.all()[0].pk)
            )

        return redirect(reverse('panel:pupil', kwargs={'pupil_id': instance.pupil.pk}))

    form.fields['parameter'].widget.attrs['multiple'] = "multiple"
    form.fields['parameter'].widget.attrs['class'] = "select2"
    context = {
        'form': form,
        'pupil': the_pupil,
        'parameter': 'לבחירתך'
    }
    return render(request, 'panel/cut_form.html', context)


def cut_create_specific(request, pupil_id, parameter_id):
    form = CutFormSpecific(request.POST or None)
    the_pupil = Pupil.objects.get(pk=pupil_id)
    the_user = request.user
    if form.is_valid():
        instance = form.save(commit=False)
        instance.pupil = the_pupil
        instance.updated_time = datetime.datetime.now()
        instance.updated_by = the_user
        if not form.cleaned_data['headline']:
            instance.headline = form.cleaned_data['details'][:40]
        instance.save()
        instance.parameter.add(Parameter.objects.get(pk=parameter_id))
        instance.save()
        form.save_m2m()

        recipients = the_pupil.can_read.exclude(pk=the_user.pk)
        if recipients:
            user_name = "{} {} ".format(the_user.first_name, the_user.last_name)
            message = '<strong>{}</strong> הוסיף/ה עדכון ל<strong>{}</strong>: <i>{}</i>'.format(user_name, the_pupil.name,
                                                                                                 instance.headline)
            notify.send(
                sender=the_user,
                recipient=recipients,
                verb=message,
                action_object=instance,
                target=the_pupil,
                description='/panel/{}/{}'.format(pupil_id, parameter_id)
            )

        return redirect(reverse('panel:parameter', kwargs={'pupil_id': instance.pupil.pk, 'parameter_id': parameter_id}))

    context = {
        'form': form,
        'pupil': the_pupil,
        'parameter': Parameter.objects.get(pk=parameter_id)
    }
    return render(request, 'panel/cut_form.html', context)


def cut_edit(request, pupil_id, parameter_id, cut_id):
    the_cut = Cut.objects.get(pk=cut_id)
    the_user = request.user
    the_pupil = Pupil.objects.get(pk=pupil_id)
    form = CutForm(request.POST or None, initial=model_to_dict(the_cut), instance=the_cut)

    if form.is_valid():
        instance = form.save()

        recipients = the_pupil.can_read.exclude(pk=the_user.pk)
        if recipients:
            user_name = "{} {} ".format(the_user.first_name, the_user.last_name)
            message = '<strong>{}</strong> ערך/ה עדכון השייך ל<strong>{}</strong>: <i>{}</i>'.format(user_name, the_pupil.name,
                                                                                                 instance.headline)
            notify.send(
                sender=the_user,
                recipient=recipients,
                verb=message,
                action_object=instance,
                target=the_pupil,
                description='/panel/{}/{}'.format(pupil_id, parameter_id)
            )

        return redirect(reverse('panel:parameter', kwargs={'pupil_id': instance.pupil.pk, 'parameter_id': parameter_id}))

    form.fields['parameter'].widget.attrs['multiple'] = "multiple"
    form.fields['parameter'].widget.attrs['class'] = "select2"
    context = {
        'from_event': False,
        'middle_id': parameter_id,
        'the_cut': the_cut,
        'form': form,
        'pupil': the_pupil,
    }
    return render(request, 'panel/cut_edit_form.html', context)


def cut_edit2(request, pupil_id, event_id, cut_id):
    the_cut = Cut.objects.get(pk=cut_id)
    the_user = request.user
    the_pupil = Pupil.objects.get(pk=pupil_id)

    form = CutForm(request.POST or None, initial=model_to_dict(the_cut), instance=the_cut)
    if form.is_valid():
        instance = form.save()

        recipients = the_pupil.can_read.exclude(pk=the_user.pk)
        if recipients:
            user_name = "{} {} ".format(the_user.first_name, the_user.last_name)
            message = '<strong>{}</strong> ערך/ה עדכון השייך ל<strong>{}</strong>: <i>{}</i>'.format(user_name,
                                                                                                     the_pupil.name,
                                                                                                     instance.headline)
            notify.send(
                sender=the_user,
                recipient=recipients,
                verb=message,
                action_object=instance,
                target=the_pupil,
                description='/panel/{}/events/{}'.format(pupil_id, event_id)
            )

        return redirect(reverse('panel:event', kwargs={'pupil_id': instance.pupil.pk, 'event_id': event_id}))

    form.fields['parameter'].widget.attrs['multiple'] = "multiple"
    form.fields['parameter'].widget.attrs['class'] = "select2"
    context = {
        'from_event': True,
        'middle_id': event_id,
        'the_cut': the_cut,
        'form': form,
        'pupil': the_pupil,
    }
    return render(request, 'panel/cut_edit_form.html', context)


def pupil_create(request):
    the_user = request.user
    form = PupilForm(request.POST or None, initial={'can_read': request.user})
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        form.save_m2m()

        recipients = instance.can_read.exclude(pk=the_user.pk)
        if recipients:
            user_name = "{} {} ".format(the_user.first_name, the_user.last_name)
            message = '<strong>{}</strong> הוסיף את החניך/ה <strong>{}</strong> ונתן לך הרשאות'.format(user_name, instance.name)
            notify.send(
                sender=the_user,
                recipient=recipients,
                verb=message,
                action_object=instance,
                target=instance,
                description='/panel/{}'.format(instance.id)
            )

        return redirect(reverse('panel:pupil', kwargs={'pupil_id': instance.id}))

    can_read_choices = ()
    for user in form.fields['can_read'].queryset:
        can_read_choices += ((str(user.pk), user.first_name + ' ' + user.last_name),)
    form.fields['can_read'].choices = can_read_choices

    context = {
        'form': form,
    }
    return render(request, 'panel/pupil_form.html', context)


def pupil_edit(request, pupil_id):
    the_user = request.user
    the_pupil = Pupil.objects.get(pk=pupil_id)
    if the_pupil not in the_user.pupil_set.all():
        return selector(request, 'אל תנסה/י לצפות בחניכים שאינך מורשה אליהם!')

    form = PupilEditForm(request.POST or None, initial=model_to_dict(the_pupil), instance=the_pupil)
    if form.is_valid():
        form.save()

        recipients = the_pupil.can_read.exclude(pk=the_user.pk)
        if recipients:
            user_name = "{} {} ".format(the_user.first_name, the_user.last_name)
            message = '<strong>{}</strong> ערך את הפרטים של <strong>{}</strong>'.format(user_name, the_pupil.name)
            notify.send(
                sender=the_user,
                recipient=recipients,
                verb=message,
                action_object=the_pupil,
                target=the_pupil,
                description='/panel/{}/edit'.format(the_pupil.id)
            )

        return redirect(reverse('panel:pupil', kwargs={'pupil_id': pupil_id}))

    can_read_choices = ()
    for user in form.fields['can_read'].queryset:
        can_read_choices += ((str(user.pk), user.first_name + ' ' + user.last_name),)
    form.fields['can_read'].choices = can_read_choices

    context = {
        'form': form,
        'pupil': the_pupil
    }
    return render(request, 'panel/pupil_edit_form.html' , context)


def parameter_create(request, pupil_id):
    form = ParameterForm(request.POST or None)
    if form.is_valid():
        instance = form.save()
        return redirect(reverse('panel:cut-add', kwargs={'pupil_id': pupil_id}))
    form.fields['category'].widget.attrs['class'] = "select2"
    context = {
        'form': form
    }
    return render(request, 'panel/parameter_form.html', context)


def parameter_create_from_pupil_edit(request, pupil_id):
    form = ParameterForm(request.POST or None)
    if form.is_valid():
        instance = form.save()
        return redirect(reverse('panel:pupil-edit', kwargs={'pupil_id': pupil_id}))
    form.fields['category'].widget.attrs['class'] = "select2"
    context = {
        'form': form
    }
    return render(request, 'panel/parameter_form.html', context)


def parameter_create_from_event(request, pupil_id):
    form = ParameterForm(request.POST or None)
    if form.is_valid():
        instance = form.save()
        return redirect(reverse('panel:event-add', kwargs={'pupil_id': pupil_id}))
    form.fields['category'].widget.attrs['class'] = "select2"
    context = {
        'form': form
    }
    return render(request, 'panel/parameter_form.html', context)


def parameter_create_from_event_edit(request, pupil_id, event_id):
    form = ParameterForm(request.POST or None)
    if form.is_valid():
        instance = form.save()
        return redirect(reverse('panel:event-edit', kwargs={'pupil_id': pupil_id, 'event_id': event_id}))
    form.fields['category'].widget.attrs['class'] = "select2"
    context = {
        'form': form
    }
    return render(request, 'panel/parameter_form.html', context)


def parameter_create_from_cut_edit(request, pupil_id, parameter_id, cut_id):
    form = ParameterForm(request.POST or None)
    if form.is_valid():
        instance = form.save()
        return redirect(reverse('panel:cut-edit', kwargs={'pupil_id': pupil_id, 'parameter_id': parameter_id, 'cut_id': cut_id}))
    form.fields['category'].widget.attrs['class'] = "select2"
    context = {
        'form': form
    }
    return render(request, 'panel/parameter_form.html', context)


def parameter_create_from_cut_edit2(request, pupil_id, event_id, cut_id):
    form = ParameterForm(request.POST or None)
    if form.is_valid():
        instance = form.save()
        return redirect(reverse('panel:cut-edit2', kwargs={'pupil_id': pupil_id, 'event_id': event_id, 'cut_id': cut_id}))
    form.fields['category'].widget.attrs['class'] = "select2"
    context = {
        'form': form
    }
    return render(request, 'panel/parameter_form.html', context)


def cut_delete(request, pupil_id, parameter_id, cut_id):
    the_user = request.user
    the_pupil = Pupil.objects.get(pk=pupil_id)
    the_cut = Cut.objects.get(pk = cut_id)

    recipients = the_pupil.can_read.exclude(pk=the_user.pk)
    if recipients:
        user_name = "{} {} ".format(the_user.first_name, the_user.last_name)
        message = '<strong>{}</strong> מחק/ה עדכון השייך ל<strong>{}</strong>: <i>{}</i>'.format(user_name,
                                                                                                 the_pupil.name,
                                                                                                 the_cut.headline)
        notify.send(
            sender=the_user,
            recipient=recipients,
            verb=message,
            action_object=the_cut,
            target=the_pupil,
            description='/panel/{}/{}'.format(pupil_id, parameter_id)
        )

    the_cut.delete()

    return redirect(reverse('panel:parameter', kwargs={'pupil_id': pupil_id, 'parameter_id': parameter_id}))


def cut_delete2(request, pupil_id, event_id, cut_id):
    the_user = request.user
    the_pupil = Pupil.objects.get(pk=pupil_id)
    the_cut = Cut.objects.get(pk=cut_id)

    recipients = the_pupil.can_read.exclude(pk=the_user.pk)
    if recipients:
        user_name = "{} {} ".format(the_user.first_name, the_user.last_name)
        message = '<strong>{}</strong> מחק/ה עדכון השייך ל<strong>{}</strong>: <i>{}</i>'.format(user_name,
                                                                                                 the_pupil.name,
                                                                                                 the_cut.headline)
        notify.send(
            sender=the_user,
            recipient=recipients,
            verb=message,
            action_object=the_cut,
            target=the_pupil,
            description='/panel/{}/events/{}'.format(pupil_id, event_id)
        )

    the_cut.delete()
    return redirect(reverse('panel:event', kwargs={'pupil_id': pupil_id, 'event_id': event_id}))


def event_delete(request, pupil_id, event_id):
    the_user = request.user
    the_pupil = Pupil.objects.get(pk=pupil_id)
    the_event = Event.objects.get(pk = event_id)

    recipients = the_pupil.can_read.exclude(pk=the_user.pk)
    if recipients:
        user_name = "{} {} ".format(the_user.first_name, the_user.last_name)
        message = '<strong>{}</strong> מחק/ה אירוע השייך ל<strong>{}</strong>: <i>{}</i>'.format(user_name,
                                                                                                 the_pupil.name,
                                                                                                 the_event.headline)
        notify.send(
            sender=the_user,
            recipient=recipients,
            verb=message,
            action_object=the_event,
            target=the_pupil,
            description='/panel/{}/events'.format(pupil_id)
        )

    the_event.delete()
    return redirect(reverse('panel:events', kwargs={'pupil_id': pupil_id}))


def event_create(request, pupil_id):
    the_user = request.user
    the_pupil = Pupil.objects.get(pk=pupil_id)
    CutFormSet = modelformset_factory(
        Cut,
        form=CutFormEvent,
        extra=10
    )
    if request.method == 'POST':
        event = EventForm(request.POST, prefix='event')
        cut_forms = CutFormSet(request.POST, prefix='cuts')
        if event.is_valid() and cut_forms.is_valid():
            instance = event.save(commit=False)
            instance.pupil = Pupil.objects.get(pk=pupil_id)
            instance.headline = event.cleaned_data["headline"]
            instance.details = event.cleaned_data["details"]
            instance.date = event.cleaned_data["date"]
            instance.updated_by = the_user
            instance.save()
            listing = cut_forms.save(commit=False)
            for cut in listing:
                cut.pupil = Pupil.objects.get(pk=pupil_id)
                cut.updated_time = datetime.datetime.now()
                cut.updated_by = the_user
                cut.headline = event.cleaned_data['headline']
                cut.event = instance
                cut.save()
            cut_forms.save_m2m()

            recipients = the_pupil.can_read.exclude(pk=the_user.pk)
            if recipients:
                user_name = "{} {} ".format(the_user.first_name, the_user.last_name)
                message = '<strong>{}</strong> הוסיף/ה אירוע ל<strong>{}</strong>: <i>{}</i>'.format(user_name,
                                                                                                         the_pupil.name,
                                                                                                         instance.headline)
                notify.send(
                    sender=the_user,
                    recipient=recipients,
                    verb=message,
                    action_object=instance,
                    target=the_pupil,
                    description='/panel/{}/events/{}'.format(pupil_id, instance.pk)
                )

            return redirect(reverse('panel:events', kwargs={'pupil_id': pupil_id}))
        else:
            context = {
                'event': event,
                'cut_forms': cut_forms,
                'pupil': the_pupil,
                'has_errors': True,
            }
            return render(request, 'panel/event_form.html', context)
    else:
        cut_forms = CutFormSet(prefix='cuts', queryset=Cut.objects.none())
        context = {
            'event': EventForm(prefix='event'),
            'cut_forms': cut_forms,
            'pupil': the_pupil,
            'has_errors': False,
        }
        return render(request, 'panel/event_form.html', context)


def event_edit(request, pupil_id, event_id):
    the_user = request.user
    the_pupil = Pupil.objects.get(pk=pupil_id)
    the_event = Event.objects.get(pk=event_id)
    CutFormSet = modelformset_factory(
        Cut,
        form=CutFormEvent,
        extra=10
    )
    if request.method == 'POST':
        event = EventForm(request.POST, prefix='event', instance=the_event)
        cut_forms = CutFormSet(request.POST, prefix='cuts')
        if event.is_valid() and cut_forms.is_valid():
            instance = event.save(commit=False)
            instance.pupil = Pupil.objects.get(pk=pupil_id)
            instance.headline = event.cleaned_data["headline"]
            instance.details = event.cleaned_data["details"]
            instance.date = event.cleaned_data["date"]
            instance.updated_by = the_user
            instance.save()
            listing = cut_forms.save(commit=False)
            for cut in listing:
                cut.pupil = Pupil.objects.get(pk=pupil_id)
                cut.updated_time = datetime.datetime.now()
                cut.updated_by = the_user
                cut.headline = event.cleaned_data['headline']
                cut.event = instance
                cut.save()
            cut_forms.save_m2m()

            recipients = the_pupil.can_read.exclude(pk=the_user.pk)
            if recipients:
                user_name = "{} {} ".format(the_user.first_name, the_user.last_name)
                message = '<strong>{}</strong> ערך/ה אירוע השייך ל<strong>{}</strong>: <i>{}</i>'.format(user_name,
                                                                                                     the_pupil.name,
                                                                                                     instance.headline)
                notify.send(
                    sender=the_user,
                    recipient=recipients,
                    verb=message,
                    action_object=instance,
                    target=the_pupil,
                    description='/panel/{}/events/{}'.format(pupil_id, instance.pk)
                )

            return redirect(reverse('panel:events', kwargs={'pupil_id': pupil_id}))
        else:
            context = {
                'event': event,
                'cut_forms': cut_forms,
                'pupil': the_pupil,
                'has_errors': True,
            }
            return render(request, 'panel/event_form.html', context)
    else:
        cut_forms = CutFormSet(prefix='cuts', queryset=Cut.objects.none())
        context = {
            'event': the_event,
            'event_form': EventForm(prefix='event', initial=model_to_dict(the_event)),
            'cut_forms': cut_forms,
            'pupil': the_pupil,
            'has_errors': False,
        }
        return render(request, 'panel/event_edit_form.html', context)


def notifications(request):
    the_user = request.user
    context = {
        'notifications': the_user.notifications.all()
    }
    return render(request, 'panel/notifications.html', context)
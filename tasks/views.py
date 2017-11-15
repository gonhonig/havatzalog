from django.shortcuts import render, redirect
from .models import Task
from panel.models import Cut
from .forms import TaskForm
from django.contrib.contenttypes.models import ContentType


def done(request, task_id):
    the_task = Task.objects.get(pk=task_id)
    the_task.done = True
    the_task.save()
    url = request.GET.get('ret')
    if 'panel' in url:
        request.session['t_obj'] = the_task.content_object.pk
    return redirect(url)


def undone(request, task_id):
    the_task = Task.objects.get(pk=task_id)
    the_task.done = False
    the_task.save()
    url = request.GET.get('ret')
    if 'panel' in url:
        if the_task.content_type == ContentType.objects.get_for_model(Cut):
            c_type = 'c_tasks_'
        else:
            c_type = 'e_tasks_'
        request.session['t_obj'] = c_type + str(the_task.content_object.pk)
    return redirect(url)


def tasks(request):
    the_user = request.user
    if request.method == 'POST':
        task_form = TaskForm(request.POST)
        if task_form.is_valid():
            content = task_form.cleaned_data.get("content")
            area = task_form.cleaned_data.get("area")
            deadline = task_form.cleaned_data.get("deadline")

            new_task, created = Task.objects.get_or_create(
                user=the_user,
                content=content,
                area=area,
                deadline=deadline,
            )
    context = {
        'done': Task.objects.filter(user=request.user, done=True),
        'undone': Task.objects.filter(user=request.user, done=False),
        'nbar': 'tasks',
        'task_form': TaskForm()
    }
    return render(request, 'tasks/tasks.html', context)

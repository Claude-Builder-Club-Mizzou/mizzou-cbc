from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import EventForm, GalleryImageForm, ProjectForm
from .models import Event, GalleryImage, Project

LOGIN_URL = '/cb-exec/'


def dashboard_login(request):
    if request.user.is_authenticated:
        return redirect('dashboard:home')

    error = None
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard:home')
        else:
            error = 'Invalid credentials.'

    return render(request, 'dashboard/login.html', {'error': error})


def dashboard_logout(request):
    logout(request)
    return redirect('index')


@login_required(login_url=LOGIN_URL)
def dashboard_home(request):
    context = {
        'active_page': 'home',
        'gallery_count': GalleryImage.objects.count(),
        'event_count': Event.objects.count(),
        'project_count': Project.objects.count(),
    }
    return render(request, 'dashboard/home.html', context)


# ── Gallery ──────────────────────────────────────────────────────────────


@login_required(login_url=LOGIN_URL)
def gallery_list(request):
    images = GalleryImage.objects.all()

    # Handle upload
    if request.method == 'POST':
        form = GalleryImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('dashboard:gallery')
    else:
        form = GalleryImageForm(initial={'order': GalleryImage.objects.count()})

    context = {
        'active_page': 'gallery',
        'images': images,
        'form': form,
    }
    return render(request, 'dashboard/gallery.html', context)


@login_required(login_url=LOGIN_URL)
def gallery_delete(request, pk):
    image = get_object_or_404(GalleryImage, pk=pk)
    if request.method == 'POST':
        image.image.delete(save=False)
        image.delete()
    return redirect('dashboard:gallery')


# ── Events ───────────────────────────────────────────────────────────────


@login_required(login_url=LOGIN_URL)
def event_list(request):
    events = Event.objects.all()
    context = {
        'active_page': 'events',
        'events': events,
    }
    return render(request, 'dashboard/events.html', context)


@login_required(login_url=LOGIN_URL)
def event_create(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard:events')
    else:
        form = EventForm()

    context = {
        'active_page': 'events',
        'form': form,
        'editing': False,
    }
    return render(request, 'dashboard/event_form.html', context)


@login_required(login_url=LOGIN_URL)
def event_edit(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            return redirect('dashboard:events')
    else:
        form = EventForm(instance=event)

    context = {
        'active_page': 'events',
        'form': form,
        'event': event,
        'editing': True,
    }
    return render(request, 'dashboard/event_form.html', context)


@login_required(login_url=LOGIN_URL)
def event_delete(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        event.delete()
    return redirect('dashboard:events')


# ── Projects ─────────────────────────────────────────────────────────────


@login_required(login_url=LOGIN_URL)
def project_list(request):
    projects = Project.objects.all()
    context = {
        'active_page': 'projects',
        'projects': projects,
    }
    return render(request, 'dashboard/projects.html', context)


@login_required(login_url=LOGIN_URL)
def project_create(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('dashboard:projects')
    else:
        form = ProjectForm(initial={'order': Project.objects.count()})

    context = {
        'active_page': 'projects',
        'form': form,
        'editing': False,
    }
    return render(request, 'dashboard/project_form.html', context)


@login_required(login_url=LOGIN_URL)
def project_edit(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            return redirect('dashboard:projects')
    else:
        form = ProjectForm(instance=project)

    context = {
        'active_page': 'projects',
        'form': form,
        'project': project,
        'editing': True,
    }
    return render(request, 'dashboard/project_form.html', context)


@login_required(login_url=LOGIN_URL)
def project_delete(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method == 'POST':
        project.delete()
    return redirect('dashboard:projects')
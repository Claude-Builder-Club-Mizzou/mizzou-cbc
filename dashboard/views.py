from collections import defaultdict

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .forms import BuilderForm, EventForm, GalleryImageForm, ProjectForm, ProjectImageFormSet, TeamMemberForm
from .models import Builder, Event, GalleryImage, Project, TeamMember
from .terms import all_terms, current_term, term_label, term_status

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
        'team_count': TeamMember.objects.filter(term=current_term()).count(),
        'current_term_label': term_label(current_term()),
        'past_board_count': TeamMember.objects.exclude(term=current_term()).values('term').distinct().count(),
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
    projects = Project.objects.prefetch_related('builders')
    context = {
        'active_page': 'projects',
        'projects': projects,
    }
    return render(request, 'dashboard/projects.html', context)


@login_required(login_url=LOGIN_URL)
def project_create(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        formset = ProjectImageFormSet(request.POST, request.FILES, instance=form.instance)
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            return redirect('dashboard:projects')
    else:
        form = ProjectForm(initial={'order': Project.objects.count()})
        formset = ProjectImageFormSet(instance=form.instance)

    context = {
        'active_page': 'projects',
        'form': form,
        'formset': formset,
        'editing': False,
    }
    return render(request, 'dashboard/project_form.html', context)


@login_required(login_url=LOGIN_URL)
def project_edit(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance=project)
        formset = ProjectImageFormSet(request.POST, request.FILES, instance=project)
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            return redirect('dashboard:projects')
    else:
        form = ProjectForm(instance=project)
        formset = ProjectImageFormSet(instance=project)

    context = {
        'active_page': 'projects',
        'form': form,
        'formset': formset,
        'project': project,
        'editing': True,
    }
    return render(request, 'dashboard/project_form.html', context)


@login_required(login_url=LOGIN_URL)
def project_delete(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method == 'POST':
        for img in project.images.all():
            img.image.delete(save=False)
        project.image.delete(save=False)
        project.delete()
    return redirect('dashboard:projects')


# ── Builders ─────────────────────────────────────────────────────────────


@login_required(login_url=LOGIN_URL)
def builder_list(request):
    context = {
        'active_page': 'builders',
        'builders': Builder.objects.prefetch_related('projects'),
    }
    return render(request, 'dashboard/builders.html', context)


@login_required(login_url=LOGIN_URL)
def builder_create(request):
    if request.method == 'POST':
        form = BuilderForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('dashboard:builders')
    else:
        form = BuilderForm()

    context = {'active_page': 'builders', 'form': form, 'editing': False}
    return render(request, 'dashboard/builder_form.html', context)


@login_required(login_url=LOGIN_URL)
def builder_edit(request, pk):
    builder = get_object_or_404(Builder, pk=pk)
    if request.method == 'POST':
        form = BuilderForm(request.POST, request.FILES, instance=builder)
        if form.is_valid():
            form.save()
            return redirect('dashboard:builders')
    else:
        form = BuilderForm(instance=builder)

    context = {'active_page': 'builders', 'form': form, 'builder': builder, 'editing': True}
    return render(request, 'dashboard/builder_form.html', context)


@login_required(login_url=LOGIN_URL)
def builder_delete(request, pk):
    builder = get_object_or_404(Builder, pk=pk)
    if request.method == 'POST':
        builder.photo.delete(save=False)
        builder.delete()
    return redirect('dashboard:builders')


# ── Team ─────────────────────────────────────────────────────────────────


def _team_redirect(term):
    return redirect(f"{reverse('dashboard:team')}?term={term}")


def _requested_term(request):
    """The ?term= key if it's a known term, else the current board."""
    keys = [key for key, _ in all_terms()]
    term = request.GET.get('term')
    return term if term in keys else current_term()


@login_required(login_url=LOGIN_URL)
def team_list(request):
    by_term = defaultdict(list)
    for member in TeamMember.objects.all():
        by_term[member.term].append(member)

    current_board = None
    past_boards = []
    # Newest first, so the dropdown reads as a timeline going back.
    for key, label in reversed(all_terms()):
        status = term_status(key)
        members = by_term.get(key, [])
        if status == 'upcoming' and not members:
            continue
        board = {'key': key, 'label': label, 'members': members, 'status': status}
        if status == 'current':
            current_board = board
        else:
            past_boards.append(board)

    context = {
        'active_page': 'team',
        'current_board': current_board,
        'past_boards': past_boards,
        # Keep the board you just edited open after the redirect.
        'open_term': _requested_term(request),
    }
    return render(request, 'dashboard/team.html', context)


@login_required(login_url=LOGIN_URL)
def team_create(request):
    term = _requested_term(request)
    if request.method == 'POST':
        form = TeamMemberForm(request.POST, request.FILES)
        if form.is_valid():
            member = form.save()
            return _team_redirect(member.term)
    else:
        form = TeamMemberForm(initial={
            'term': term,
            'order': TeamMember.objects.filter(term=term).count(),
        })

    context = {
        'active_page': 'team',
        'form': form,
        'editing': False,
        'back_term': term,
    }
    return render(request, 'dashboard/team_form.html', context)


@login_required(login_url=LOGIN_URL)
def team_edit(request, pk):
    member = get_object_or_404(TeamMember, pk=pk)
    if request.method == 'POST':
        form = TeamMemberForm(request.POST, request.FILES, instance=member)
        if form.is_valid():
            member = form.save()
            return _team_redirect(member.term)
    else:
        form = TeamMemberForm(instance=member)

    context = {
        'active_page': 'team',
        'form': form,
        'member': member,
        'editing': True,
        'back_term': member.term,
    }
    return render(request, 'dashboard/team_form.html', context)


@login_required(login_url=LOGIN_URL)
def team_delete(request, pk):
    member = get_object_or_404(TeamMember, pk=pk)
    term = member.term
    if request.method == 'POST':
        member.photo.delete(save=False)
        member.delete()
    return _team_redirect(term)

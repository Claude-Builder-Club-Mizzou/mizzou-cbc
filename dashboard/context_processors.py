from .models import Project


def pending_submissions(request):
    """Pending-review count for the dashboard sidebar badge (exec pages only)."""
    if request.path.startswith('/cb-exec/') and request.user.is_authenticated:
        return {'pending_count': Project.objects.pending().count()}
    return {}

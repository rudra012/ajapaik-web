from django.core.management.base import BaseCommand
from project.home.views import _calculate_recent_activity_scores


class Command(BaseCommand):
    help = "Recalculates scores taking only recent activity into account"

    def handle(self, *args, **options):
        _calculate_recent_activity_scores()
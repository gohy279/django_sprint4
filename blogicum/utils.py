from django.utils import timezone
from django.core.paginator import Paginator
from django.db.models import Count


def get_public_posts(data):
    return (
        data.filter(
            is_published=True,
            pub_date__lte=timezone.now(),
            category__is_published=True,
        )
    )


def get_comments(data):
    return (
        data
        .select_related("author")
        .annotate(comment_count=Count("comments"))
        .order_by("-pub_date")
    )


def paginate_queryset(request, queryset, per_page=10):
    paginator = Paginator(queryset, per_page)
    page_number = request.GET.get('page')
    return paginator.get_page(page_number)

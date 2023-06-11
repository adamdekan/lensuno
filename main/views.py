from django.shortcuts import render, redirect

# from django.contrib.auth.decorators import user_passes_test
from country_list import countries_for_language
from portfolio.models import Portfolio, Gig
from users.models import User

# from shootbe.decorators import is_freelancer
from django.views.generic.base import TemplateView
from .filters import GigFilter
from main.forms import IndexSearchForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from django.template.response import TemplateResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.admin.views.decorators import staff_member_required


# Create your views here.
def index(response):
    return render(response, "main/index.html", {})


def redirect_to_portal(response):
    return redirect("https://portal.lensuno.com")


class Home(TemplateView):
    template_name = "home/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["gigs"] = Gig.objects.filter(
            gallery__isnull=False, is_active=True, is_featured=True
        )
        context["post_production"] = Gig.objects.filter(
            category__in=["PT", "VE"],
            gallery__isnull=False,
            is_active=True,
        )
        context["portfolios"] = Portfolio.objects.filter(is_featured=True)
        context["profiles"] = User.objects.all()
        context["black_header"] = True
        context["index_search"] = IndexSearchForm()
        context["categories"] = Gig.CATEGORY_CHOICES
        return context


# from shootbe/decorators.py
# https://stackoverflow.com/questions/4789021/in-django-how-do-i-check-if-a-user-is-in-a-certain-group
@staff_member_required
def test_page(response):
    return render(response, "main/sign-thanks.html", {})


def test_page2(response, slug):
    print(slug)
    return render(response, "main/test-page.html", {})


# not working yet
def my_404_view(request, exception):
    return render(request, "main/404.html", {"exception": exception}, status=404)


def check_country(search):
    countries = countries_for_language("en")
    for city in countries:
        if city[1].lower() == search:
            return True
    return False


def search_city(request, search):
    # if check_country(search):
    #     search_query = Gig.objects.filter(
    #         location__icontains=search,
    #         is_active=True,
    #         gallery__isnull=False,
    #     )
    if search == "world":
        search_query = Gig.objects.filter(
            is_active=True,
            gallery__isnull=False,
        )
    else:
        search_query = Gig.objects.filter(
            location__icontains=search,
            is_active=True,
            gallery__isnull=False,
        )
    f = GigFilter(request.GET, queryset=search_query)
    filtered_qs = GigFilter(request.GET, queryset=search_query).qs
    paginator = Paginator(filtered_qs, 12)
    page = request.GET.get("page")
    try:
        query = paginator.page(page)
    except PageNotAnInteger:
        query = paginator.page(1)
    except EmptyPage:
        query = paginator.page(paginator.num_pages)
    # if request.htmx:
    #     html = render_block_to_string("main/search.html", "cards")
    #     return TemplateResponse(request, html)
    # else:
    response = "main/search.html"
    return TemplateResponse(
        request,
        response,
        {"city": search, "filter": f, "query": query},
    )


def search(request):
    if request.method == "GET":
        string = request.GET["search"]
        try:
            category = request.GET["category"]
        except KeyError:
            category = ""
        if string is None or string.strip() == "":
            search_query = "world"
        else:
            search_query = string.split(",")[0].lower()
        return redirect(f"{search_query}/?category={category}")


@csrf_exempt
def copy_url(request):
    url = request.build_absolute_uri()
    return HttpResponse(url, content_type="text/plain")


def about_us(response):
    return render(response, "main/about-us.html", {})


# @require_GET
# def results(request, search):
#     if request.htmx:
#         base_template = "main/search-result.html"
#     else:
#         base_template = "main/search.html"

#     if check_country(search):
#         search_query = Gig.objects.filter(country__icontains=search, is_active=True)
#     elif search == "world":
#         search_query = Gig.objects.all()
#     else:
#         search_query = Gig.objects.filter(city__icontains=search, is_active=True)
#     f = GigFilter(request.GET, queryset=search_query)
#     return render(
#         request,
#         base_template,
#         {"city": search, "filter": f},
#     )

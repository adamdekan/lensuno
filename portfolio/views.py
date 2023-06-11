from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import get_user_model
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy, reverse
from .models import Portfolio, Gig, Package
from django.views.generic.detail import DetailView
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse
from .forms import GigUpdateForm, PortfolioUpdateForm, PackageForm
from shootbe.decorators import is_freelancer
from django.contrib import messages
from comments.forms import CommentGigForm
from gallery.models import DemoGallery
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from users.forms import SettingsForm
from django.views.decorators.csrf import csrf_exempt
from main.helpers import send_email_admin

# users.user
User = get_user_model()


# ----------------------------------------------
# PORTFOLIO
# ----------------------------------------------
class PortfolioCreateView(LoginRequiredMixin, CreateView):
    model = Portfolio
    template_name = "portfolio/portfolio-create.html"
    form_class = PortfolioUpdateForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        self.request.user.groups.add(Group.objects.get(name="freelancer"))
        print("adding to freelancer group")
        self.object = form.save(commit=False)
        self.object.user.is_freelancer = True
        self.object.user.save()
        self.object.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("portfolio:gig-create")

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context["form"] = PortfolioUpdateForm()
    #     context["black_header"] = True


class PortfolioDetailView(DetailView):
    model = Portfolio
    template_name = "portfolio/portfolio-detail.html"
    slug_url_kwarg = "slug"
    context_object_name = "portfolio"

    def get_object(self, queryset=None):
        queryset = self.get_queryset()
        slug = self.kwargs.get(self.slug_url_kwarg)
        obj = get_object_or_404(queryset, slug=slug)
        return obj

    def validate_url(self, url, website):
        if not url:
            return False

        if not url.startswith(f"https://www.{website}.com/"):
            return False

        if len(url) <= len(f"https://www.{website}.com/"):
            return False

        return url

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["social_fb"] = self.validate_url(self.object.social_fb, "facebook")
        context["social_ig"] = self.validate_url(self.object.social_ig, "instagram")
        context["social_yt"] = self.validate_url(self.object.social_yt, "youtube")
        context["social_vm"] = self.validate_url(self.object.social_vm, "vimeo")
        context["gigs"] = Gig.query.portfolio_active(self.object.user)
        context["black_header"] = True
        return context


@user_passes_test(is_freelancer)
def portfolio_update_view(request):
    template = "portfolio/portfolio-update.html"
    context = {}

    obj = get_object_or_404(Portfolio, user__pk=request.user.pk)
    form = PortfolioUpdateForm(instance=obj)
    if request.method == "POST":
        form = PortfolioUpdateForm(request.POST, request.FILES, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, f"Portfolio '{obj.slug}' updated.")
            return HttpResponseRedirect(obj.get_absolute_url())

    context["portfolio"] = obj
    context["form"] = form
    return TemplateResponse(request, template, context)


# ----------------------------------------------
# GIGS
# ----------------------------------------------
def gig_detail_view(request, slug, pk):
    if request.htmx:
        template = "comments/comment.html"
    else:
        template = "gigs/gig-detail.html"
    context = {}

    gig = get_object_or_404(Gig, id=pk)
    if gig.portfolio.user.id == request.user.id:
        context["is_owner"] = True
    else:
        context["is_owner"] = False

    try:
        context["gallery"] = get_object_or_404(DemoGallery, gig_id=gig.id)
    # trunk-ignore(ruff/E722)
    except:
        context["gallery"] = None

    if request.method == "POST":
        form = CommentGigForm(request.POST, request.FILES)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.gig = gig
            comment.author = request.user
            comment.save()
            return redirect("main:gig-detail", slug=slug, pk=pk)

    form = CommentGigForm()

    comments = gig.gig_comment.all() if gig.gig_comment.all().count() > 0 else None
    if comments is None:
        comments_page = False
    else:
        paginator = Paginator(comments, 4)
        page = request.GET.get("page", 1)
        try:
            comments_page = paginator.page(page)
        except PageNotAnInteger:
            comments_page = paginator.page(1)
        except EmptyPage:
            comments_page = None

    context["standard_package"] = gig.packages.filter(package_type="standard").first()
    context["premium_package"] = gig.packages.filter(package_type="premium").first()
    context["master_package"] = gig.packages.filter(package_type="master").first()
    context["gig"] = gig
    context["form"] = form
    context["comments"] = comments_page
    return TemplateResponse(request, template, context)


# CREATE GIG
# ----------------------------------------------
class GigCreateView(LoginRequiredMixin, CreateView):
    model = Gig
    form_class = GigUpdateForm
    template_name = "gigs/gig-update.html"

    def form_valid(self, form):
        form.instance.portfolio = self.request.user.portfolio
        # add slug for link from Portfolio
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["create"] = True

        return context


# MY-GIGS
# ----------------------------------------------
@user_passes_test(is_freelancer)
def gig_list_view(request):
    template = "gigs/my-gigs.html"
    context = {}

    context["gig_list"] = Gig.objects.filter(portfolio__user__pk=request.user.pk)

    return TemplateResponse(request, template, context)


# UPDATE GIG
# ----------------------------------------------
@user_passes_test(is_freelancer)
def gig_update_view(request, slug, pk):
    template = "gigs/gig-update.html"
    context = {}

    gig = get_object_or_404(Gig, pk=pk)
    if request.method == "POST":
        form = GigUpdateForm(request.POST, request.FILES, instance=gig)
        if form.is_valid():
            form.save()
            messages.success(request, f"Gig '{gig.title}' updated.")
            return HttpResponseRedirect(gig.get_absolute_url())
    else:
        form = GigUpdateForm(instance=gig)

    context["gig"] = gig
    context["form"] = form

    return TemplateResponse(request, template, context)


# DELETE GIG
# ----------------------------------------------
@csrf_exempt
@user_passes_test(is_freelancer)
def gig_delete(request, slug, pk):
    gig = get_object_or_404(Gig, pk=pk)
    gig.delete()
    return HttpResponseRedirect(reverse("portfolio:my-gigs"))


# ----------------------------------------------
# PACKAGES
# ----------------------------------------------
#
# ----------------------------------------------
@user_passes_test(is_freelancer)
def create_package(request, package, gig_pk):
    template = "gigs/package-update.html"
    context = {}

    gig = get_object_or_404(Gig, pk=gig_pk)

    form = PackageForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            pcg = form.save(commit=False)
            pcg.package_type = package
            pcg.gig = gig
            pcg.save()
            return HttpResponseRedirect(gig.get_absolute_url())

    context["create"] = True
    context["gig"] = gig
    context["type"] = package
    context["form"] = form
    return TemplateResponse(request, template, context)


@user_passes_test(is_freelancer)
def update_package(request, package, gig_pk):
    template = "gigs/package-update.html"
    context = {}

    obj = get_object_or_404(Package, gig__pk=gig_pk, package_type=package)
    form = PackageForm(instance=obj)
    if request.method == "POST":
        form = PackageForm(request.POST, instance=obj)
        if form.is_valid():
            # activates the gig when updates the package
            # obj.gig.is_active = True
            # obj.gig.save()
            form.save()
            messages.success(request, f"Package {package} updated.")
            return HttpResponseRedirect(obj.gig.get_absolute_url())

    context["gig"] = obj.gig
    context["type"] = package
    context["form"] = form
    return TemplateResponse(request, template, context)


@csrf_exempt
@user_passes_test(is_freelancer)
def delete_package(request, package, gig_pk):
    gig = get_object_or_404(Gig, pk=gig_pk)
    package = get_object_or_404(Package, gig__pk=gig_pk, package_type=package)
    package.delete()
    messages.success(request, f"Package {package} deleted.")
    return HttpResponseRedirect(gig.get_absolute_url())


# ----------------------------------------------
# FREELANCER PATH
# ----------------------------------------------
@login_required
def start_portfolio(response):
    return render(response, "portfolio/start.html", {})


@login_required
def first_step(request):
    template = "portfolio/step-one.html"
    context = {}

    obj = get_object_or_404(User, id=request.user.pk)
    form = SettingsForm(request.POST or None, instance=obj)

    if form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse("portfolio:create"))

    context["form"] = form
    context["black_header"] = True

    return TemplateResponse(request, template, context)


class StepTwo(PortfolioCreateView):
    def get_context_data(self, **kwargs):
        """Insert the form into the context dict."""
        if "form" not in kwargs:
            kwargs["form"] = self.get_form()
        kwargs["black_header"] = True
        return super().get_context_data(**kwargs)

    def get_initial(self):
        """Return the initial data to use for forms on this view."""
        return self.initial.copy()

    def get_success_url(self):
        return reverse_lazy("portfolio:first-gig")


class FirstGig(LoginRequiredMixin, CreateView):
    model = Gig
    form_class = GigUpdateForm
    template_name = "gigs/gig-update.html"

    def form_valid(self, form):
        form.instance.portfolio = self.request.user.portfolio
        send_email_admin(
            f"User: {self.request.user.email} has created a new gig.",
            f"Portfolio: {self.request.user.portfolio.slug}",
        )
        # add slug for link from Portfolio
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        kwargs["black_header"] = True
        kwargs["create"] = True

        return super().get_context_data(**kwargs)

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http.response import HttpResponseRedirect
from django.urls import reverse
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from portfolio.models import Gig
from .forms import GalleryForm
from .models import DemoGallery
from django.shortcuts import get_object_or_404


class GalleryCreateView(LoginRequiredMixin, CreateView):
    form_class = GalleryForm
    template_name = "gallery/form.html"
    extra_context = {"form_description": "Create a new gallery"}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_description"] = "Create a new gallery"
        context["gig_detail"] = Gig.objects.get(
            pk=self.kwargs.get("pk")
        ).get_absolute_url()
        return context

    def get_object(self, queryset=None):
        pk = self.kwargs.get("pk")
        gig = get_object_or_404(Gig, pk=pk)
        obj, created = DemoGallery.objects.get_or_create(
            gig=gig, defaults={"owner": self.request.user}
        )
        return obj

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.owner = self.request.user
        # get gig pk from url
        pk = self.kwargs.get("pk")
        self.object.gig = get_object_or_404(Gig, id=pk)
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse("gallery:update", kwargs={"pk": self.object.gig.pk})


class GalleryUpdateView(UserPassesTestMixin, LoginRequiredMixin, UpdateView):
    model = DemoGallery
    form_class = GalleryForm
    template_name = "gallery/form.html"

    def get_object(self, queryset=None):
        pk = self.kwargs.get("pk")
        gig = get_object_or_404(Gig, pk=pk)
        obj, created = DemoGallery.objects.get_or_create(
            gig=gig, defaults={"owner": self.request.user}
        )
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context[
            "form_description"
        ] = "Update gallery - maximum image size 20Mb and maximum resolution 1920x1920px"
        context["gig_detail"] = Gig.objects.get(
            pk=self.kwargs.get("pk")
        ).get_absolute_url()
        return context

    def test_func(self):
        return (
            self.request.user == self.get_object().owner
            or self.request.user.is_superuser
        )


class GalleryDetailView(DetailView):
    model = DemoGallery

    def get_object(self, queryset=None):
        pk = self.kwargs.get("pk")
        gig = get_object_or_404(Gig, pk=pk)
        obj, created = DemoGallery.objects.get_or_create(
            gig=gig, defaults={"owner": self.request.user}
        )
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_description"] = "Gallery Detail"
        context["update_view_url"] = reverse(
            "gallery:update", kwargs={"pk": self.object.pk}
        )
        return context

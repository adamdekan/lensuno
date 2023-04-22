from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.contrib.auth import get_user_model
from .forms import CommentForm, ReportCommentForm
from django.views.generic import CreateView, ListView, FormView, DetailView
from django.views.generic.detail import SingleObjectMixin
from users.models import ProfileComment
from django.http import JsonResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.template.response import TemplateResponse
from portfolio.models import Gig
from comments.models import Comment
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


User = get_user_model()


def profile_view(request, pk):
    if request.htmx:
        template = "comments/comment.html"
    else:
        template = "users/profile-detail.html"
    context = {}

    profile = get_object_or_404(User, id=pk)
    if profile.id == request.user.id:
        context["is_owner"] = True

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.profile = profile
            comment.author = request.user
            comment.save()
            return redirect("users:profile", pk=pk)

    form = CommentForm()

    comments = ProfileComment.objects.filter(profile=profile)
    if comments == None:
        comments_page = None
    else:
        paginator = Paginator(comments, 5)
        page = request.GET.get("page", 1)
        try:
            comments_page = paginator.page(page)
        except PageNotAnInteger:
            comments_page = paginator.page(1)
        except EmptyPage:
            comments_page = None

    # context["user_pk"] = request.user.pk
    context["form"] = form
    context["gig_comments"] = Comment.objects.filter(gig__portfolio__user=profile)
    context["profile_comments"] = comments
    context["comments"] = comments_page
    context["gigs"] = Gig.query.active(profile)
    context["profile"] = profile
    return TemplateResponse(request, template, context)


# Create your views here.
# class ProfileCommentView(DetailView):
#     model = get_user_model()
#     context_object_name = "profile"
#     template_name = "users/profile-detail.html"
#     pk_url_kwarg = "pk"

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         pk = self.kwargs.get(self.pk_url_kwarg)
#         context["user_pk"] = self.request.user.pk
#         context["form"] = CommentForm()
#         context["gig_comments"] = Comment.objects.filter(gig__portfolio__user__pk=pk)
#         context["profile_comments"] = ProfileComment.objects.filter(profile_id=pk)
#         context["gigs"] = Gig.objects.filter(portfolio__user__pk=pk)
#         return context


# # django for beginners - 274
# class CommentPost(SingleObjectMixin, FormView):
#     model = get_user_model()
#     form_class = CommentForm
#     template_name = "users/profile-detail.html"

#     def post(self, request, *args, **kwargs):
#         self.object = self.get_object()
#         return super().post(request, *args, **kwargs)

#     def form_valid(self, form):
#         comment = form.save(commit=False)
#         comment.profile = self.object
#         comment.author = self.request.user
#         comment.save()
#         return super().form_valid(form)

#     def get_success_url(self):
#         return reverse("users:profile", kwargs={"pk": self.object.pk})


# django htmx https://django-htmx.readthedocs.io/en/latest/middleware.html#django_htmx.middleware.HtmxDetails


@csrf_exempt
def report_gig_comment_htmx(request, pk):
    if request.method == "POST":
        comment = Comment.objects.get(pk=pk)
        comment.is_flagged = True
        comment.save()
        print(f"Flagging {pk}")
        return JsonResponse({"success": True})
    else:
        return JsonResponse({"success": False})


@csrf_exempt
def report_profile_comment_htmx(request, pk):
    if request.method == "POST":
        comment = ProfileComment.objects.get(pk=pk)
        comment.is_flagged = True
        comment.save()
        print(f"Flagging {pk}")
        return JsonResponse({"success": True})
    else:
        return JsonResponse({"success": False})

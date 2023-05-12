from django import template
from portfolio.models import Gig, Portfolio

register = template.Library()


@register.simple_tag(name="trans")
def trans(format_string):
    return format_string


@register.filter(name="times")
def times(number):
    return range(number)


@register.inclusion_tag("gigs/gigs-list-profile.html")
def show_gigs_profile(portfolio_id):
    gigs = Gig.objects.filter(portfolio_id=portfolio_id)
    return {"gigs": gigs}


@register.inclusion_tag("gigs/gigs-list-portfolio.html")
def show_gigs_portfolio(portfolio_id):
    gigs = Gig.objects.filter(portfolio_id=portfolio_id)
    return {"gigs": gigs}


@register.simple_tag(name="full_name")
def full_name(user):
    return user.get_full_name()


@register.simple_tag(name="get_portfolio")
def get_portfolio(pk):
    return Portfolio.objects.get(user__id=pk).get_absolute_url()


# @register.simple_tag
# def get_user_comments(pk):
#     result_list = {}
#     gig_comments = Comment.objects.filter(gig__portfolio__user__pk=pk)
#     user_comments = ProfileComment.objects.filter(profile_id=pk)
#     result_list = list(
#         sorted(
#             chain(user_comments, gig_comments),
#             key=lambda instance: instance.date,
#             reverse=True,
#         )
#     )
#     return result_list

from django import template
from django.template import Template, Context
from django.template.loader import get_template

from messageboard.models import Board

register = template.Library()


@register.simple_tag
def board_list():
    boards = Board.objects.all()
    t = get_template("_navbar/board_list.html")
    return t.render({'boards': boards})

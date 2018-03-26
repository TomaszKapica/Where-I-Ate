from django.template import Library

register = Library()


@register.filter
def sub_date(value, arg):
    if value == arg:
        return True
    else:
        return False


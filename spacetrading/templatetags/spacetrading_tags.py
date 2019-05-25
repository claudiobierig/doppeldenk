from django import template

register = template.Library()


@register.simple_tag
def get_class(label):
    if "Buy" in label:
        return "table-danger"
    elif "Sell" in label:
        return "table-success"
    else:
        return "table-light"

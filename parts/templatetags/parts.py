from django import template


register = template.Library()


@register.simple_tag(takes_context=True)
def htmlId(context):
    part = context["self"]
    rendered_id = 'id="%s"' % part.name
    return rendered_id

@register.simple_tag(takes_context=True)
def jqId(context):
    part = context["self"]
    rendered_id = '$("#%s")' % part.name
    return rendered_id

@register.simple_tag(takes_context=True)
def getClass(context):
    if context["self"].CLASS is not None:
        return "class='%s'" % context["self"].CLASS

@register.simple_tag(takes_context=True)
def makeUrl(context,new_url=""):
    current_url = context["request"].get_full_path
    print current_url
    return current_url

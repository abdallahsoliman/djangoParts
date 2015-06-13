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

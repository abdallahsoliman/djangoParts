from django import template


register = template.Library()


@register.simple_tag(takes_context=True)
def htmlId(context,id_string):
    part = context["self"]
    rendered_id = 'id="%s_%s"' % (part.NAME, id_string)
    return rendered_id

@register.simple_tag(takes_context=True)
def jqId(context,id_string):
    part = context["self"]
    rendered_id = '$("#%s_%s")' % (part.NAME, id_string)
    return rendered_id

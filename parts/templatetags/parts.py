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
def makeUrl(context,*args,**kwargs):
    current_url = context["request"].get_full_path()
    #Make arg_dict from current_url
    arg_dict = {}
    url_args = current_url.split("?")[1]
    for arg in url_args.split("&"):
        if "=" in arg:
            split_arg = arg.split("=")
            key = split_arg[0]
            value = split_arg[1]
        else:
            key = arg
            value = None
        arg_dict[key] = value
    #Merge the new args into the arg dict
    for key in kwargs:
        arg_dict[key] = kwargs[key]
    for arg in args:
        arg_dict[arg] = None
    #Remove all args that start with minus
    delete_keys = [key for key in arg_dict if key[0] == "-"]
    print delete_keys
    for key in delete_keys:
        arg_dict.pop(key,None)
        arg_dict.pop(key[1:],None)
    #Reconstruct the url
    args = ["{0}={1}".format(key,arg_dict[key]) for key in arg_dict if arg_dict[key] != None]
    args += [key for key in arg_dict if arg_dict[key] == None]
    url = "/?" + "&".join(args)
    return url

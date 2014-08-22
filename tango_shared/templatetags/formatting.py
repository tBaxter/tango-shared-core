from django.template import Library

register = Library()


@register.filter
def replace(value, arg):
    """
    Replaces one string with another in a given string
    usage: {{ foo|replace:"aaa|xxx"}}
    """

    replacement = arg.split('|')
    try:
        return value.replace(replacement[0], replacement[1])
    except:
        return value


@register.filter
def fixbreaks(value):
    """
    fixes line breaks to make markdown happy.
    Be careful. It won't play nice with para breaks.
    """
    return value.replace('\n', '  \n')

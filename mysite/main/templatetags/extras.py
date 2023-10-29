from django import template

register = template.Library()

@register.filter
def get_index(h, i):
    try:
        value = h[i]
    except:
        value = -1
    
    return value

@register.filter
def dict_key(h, key):
    try:
        value = h[key]
    except:
        value = -1
    
    return value

@register.filter
def stringify(var1, var2):
    return f"{var1},{var2}"

@register.filter
def get_initials(name):
    try:
        temp = name.split(" ")
        return f"{temp[0][0]}{temp[1][0]}"
    except:
        return name
    
@register.filter
def get_index(l, i):
    try:
        return l[int(i)]
    except:
        return None
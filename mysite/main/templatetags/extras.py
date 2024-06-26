from django import template
from django.contrib.auth.models import User
import datetime

register = template.Library()

@register.filter
def get_index(h, i):
    try:
        value = h[int(i)]
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

@register.filter
def display_name(name):
    name = str(name)
    try:
        for o in User.objects.all():
            user = o.get_username()
            if user == name:
                display = o.get_full_name().split(" ")
                return f"{display[0][0]}{display[1][:4]}"
    except:
        return name[:5]

@register.filter
def find(l, i):
    try:
        return l.index(i)
    except:
        return None

@register.filter
def get_date(date):
    date_lst = date.split("-")

    return datetime.date(int(date_lst[0]), int(date_lst[1]), int(date_lst[2]))

@register.filter
def get_role(position):
    try:
        return position.split(",")[0]
    except:
        return ""

@register.filter
def get_time(position):
    try:
        return position.split(",")[1]
    except:
        return ""
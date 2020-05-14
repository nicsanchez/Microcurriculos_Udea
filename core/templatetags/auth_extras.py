from django import template
from django.contrib.auth.models import Group

register = template.Library()

@register.filter(name='has_group')
def has_group(user, group_name): 
    group = Group.objects.get(name=group_name) 
    return True if group in user.groups.all() else False

@register.filter(name='has_rol')
def has_rol(user, rol_name): 
    if(str(user.userrol.rol)==str(rol_name) and str(user.groups.all()[0])=='Coordinador'):
        return True    
    else:
        return False

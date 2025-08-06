from django import template

register = template.Library()

@register.filter(name='add_class')
def add_class(field, css):
    existing_classes = field.field.widget.attrs.get('class', '')
    if existing_classes:
        css = existing_classes + ' ' + css
    field.field.widget.attrs['class'] = css
    return field

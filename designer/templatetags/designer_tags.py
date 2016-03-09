from django import template

register = template.Library()


@register.filter
def add_class(value, cls):
    cur_cls = value.field.widget.attrs['class'].split(' ') if 'class' in value.field.widget.attrs else []
    cur_cls.append(cls)
    return value.as_widget(attrs={'class': ' '.join(cur_cls)})

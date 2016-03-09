from django import forms

from structure.models import Unit

extra_unit_fields = {
    '__ALL__': {
        'surface': forms.FloatField(min_value=0),
    },
    'GENERIC_BUILDING,FACTORY': {
        'year-of-construction': forms.IntegerField(),
    },
    'FACTORY': {
        'industry': forms.CharField(max_length=255),
    }
}


class UnitForm(forms.ModelForm):
    class Meta:
        model = Unit
        exclude = ['user', 'location', ]

    def __init__(self, unit_type, *args, **kwargs):
        super(UnitForm, self).__init__(*args, **kwargs)
        self.extra_fields = []

        # make several fields non-visible
        for fk in ['lat', 'lng', 'address', 'info']:
            self.fields[fk].widget = forms.HiddenInput()

        # add the appropriate fields
        for k in extra_unit_fields.keys():
            if k == '__ALL__' or unit_type in k.split(','):
                for fk in extra_unit_fields[k]:
                    self.fields[fk] = extra_unit_fields[k][fk]
                    self.extra_fields.append(fk)

    def clean(self):
        data = super(UnitForm, self).clean()

        # gather info fields
        self.fields['info'] = {}
        for fk in self.extra_fields:
            self.fields['info'][fk] = data.pop(fk)

        return data

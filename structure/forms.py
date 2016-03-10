from django import forms

from structure.models import Unit

extra_unit_fields = {
    '__ALL__': {
        'surface': forms.FloatField(min_value=0),
    },
    'GENERIC_BUILDING,FACTORY': {
        'year_of_construction': forms.IntegerField(),
    },
    'FACTORY': {
        'industry': forms.CharField(max_length=255),
    }
}


class UnitForm(forms.ModelForm):
    class Meta:
        model = Unit
        exclude = ['user', 'location', ]

    def __init__(self, *args, **kwargs):
        unit_type = kwargs.pop('unit_type', None)
        self.extra_fields = []

        super(UnitForm, self).__init__(*args, **kwargs)

        # make several fields non-visible
        for fk in ['lat', 'lng', 'address', 'info', 'unit_type']:
            self.fields[fk].widget = forms.HiddenInput()

        self.fields['info'].required = False

        # add the appropriate fields
        for k in extra_unit_fields.keys():
            if k == '__ALL__' or unit_type in k.split(','):
                for fk in extra_unit_fields[k]:
                    self.fields[fk] = extra_unit_fields[k][fk]
                    self.extra_fields.append(fk)

    def clean(self):
        data = super(UnitForm, self).clean()

        # gather info fields
        data['info'] = {}
        for fk in self.extra_fields:
            try:
                data['info'][fk] = data.pop(fk)
            except KeyError:
                pass  # an error has already been added

        return data

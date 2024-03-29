from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db.models import F
from django.forms import Textarea

from bootstrap_modal_forms.mixins import PopRequestMixin, CreateUpdateAjaxMixin
from bootstrap_modal_forms.forms import BSModalForm

from pams_system.models.levels import InputData, Level, KPIWeight, KPIWeightings, KpiData
from pams_system.models.maps import MapList, MapType


class LevelStructureForm(BSModalForm, forms.ModelForm):
    class Meta:
        model = InputData
        fields = ['parent', 'name']
        # widgets = {
        #     'parent': Select2MultipleWidget,
        # }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['parent'].label = "Data Structure"
        # self.fields['levelset'].queryset = Level.objects.none()
        # # self.fields['parent'].queryset = InputData.objects.none()

        # if 'maptype' in self.data:
        #     try:
        #         maptype_id = int(self.data.get('maptype'))
        #         self.fields['maplist'].queryset = MapList.objects.filter(maptype_name_id=maptype_id)
        #     except (ValueError, TypeError):
        #         pass
        # elif self.instance.pk:
        #     self.fields['maplist'].queryset = MapList.objects.filter(maptype_name_id=2)

        # if 'maplist' in self.data:
        #     try:
        #         maplist_id = int(self.data.get('maplist'))
        #         self.fields['levelset'].queryset = Level.objects.filter(maplist_id=maplist_id)
        #     except (ValueError, TypeError):
        #         pass  # invalid input from the client; ignore and fallback to empty City queryset
        # elif self.instance.maplist_id:
        #     self.fields['levelset'].queryset = Level.objects.filter(maplist_id=1)


class KpiStructureForm(BSModalForm, forms.ModelForm, forms.Form):
    class Meta:
        model = InputData
        fields = ['parent','kpis']
        # widgets = {
        #     'parent': Select2MultipleWidget,
        # }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['maplist'].queryset = MapList.objects.none()
        # self.fields['parent'].queryset = InputData.objects.none()
# 
        # if 'maptype' in self.data:
        #     try:
        #         maptype_id = int(self.data.get('maptype'))
        #         self.fields['maplist'].queryset = MapList.objects.filter(maptype_name_id=maptype_id)
        #     except (ValueError, TypeError):
        #         pass
        # elif self.instance.pk:
        #     self.fields['maplist'].queryset = MapList.objects.filter(maptype_name_id=2)
        # #
        # if 'maplist' in self.data:
        #     try:
        #         maplist = int(self.data.get('maplist'))
        #         self.fields['levelset'].queryset = Level.objects.filter(maplist_id=maplist)
        #     except (ValueError, TypeError):
        #         pass
        # elif self.instance.pk:
        #     self.fields['levelset'].queryset = Level.objects.filter(maplist_id=2)
        # #
        #
class LevelListForm(BSModalForm):
    class Meta:
        model = Level
        fields = ['previous_level', 'name']


class LevelTypeForm(BSModalForm):
    class Meta:
        model = InputData
        fields = ['data_name']


class KPIWeightForm(forms.ModelForm):
    class Meta:
        model = KPIWeightings
        fields = ['effective_date', 'weight']

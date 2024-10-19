from django import forms
from .models import Broker, UpdateReport

from django.forms import modelformset_factory
from django.utils.numberformat import format
from django.forms import BaseModelFormSet
from datetime import datetime, timedelta
from django.core.exceptions import ValidationError


class InputBrokerForm(forms.ModelForm):
    DELETE = forms.BooleanField(required=False, widget=forms.HiddenInput)  # Add delete field

    class Meta:
        model = Broker
        fields = [
            'BKID',
            'BK名',
            'BK担当者名',
            'BKEメール',
            'BK電話番号',
            'BK会社番号',
            'BK住所',
            'BK短名',
        ]


InputBrokerFormSet = modelformset_factory(
    Broker,
    form=InputBrokerForm,
    extra=1,  # Start with 1 empty form
    can_delete=True  # Enable deletion
)


class UpdateReportForm(forms.ModelForm):
    DELETE = forms.BooleanField(required=False, widget=forms.HiddenInput)  # Add delete field

    class Meta:
        model = UpdateReport
        fields = [
            'BKID',
            'RP日付',
            'RP内容',
            '物件ID',
        ]


UpdateReportFormSet = modelformset_factory(
    UpdateReport,
    form=UpdateReportForm,
    extra=1,  # Start with 1 empty form
    can_delete=True  # Enable deletion
)
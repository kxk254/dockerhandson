from django import forms
from .models import InputField, 売上, 物件, テナント, 管理項目, 契約, 保証会社, 支払先, 敷金保証金, 費用, ステータス, BMInputField, BMItems, BM入力フォーム
from django.forms import modelformset_factory
from django.utils.numberformat import format
from django.forms import BaseModelFormSet
from datetime import datetime, timedelta
from django.core.exceptions import ValidationError

class CommaSeparatedInput(forms.TextInput ):  # Use TextInput instead of NumberInput
    def render(self, name, value, attrs=None, renderer=None):
        if value is not None:
            value = format(value, ',')  # Format number with commas
        return super().render(name, value, attrs, renderer)

class DeciSeparatedInput(forms.TextInput):  # Use TextInput instead of NumberInput
    def render(self, name, value, attrs=None, renderer=None):
        if value is not None:
            try:
                # Convert the value to a float and format with commas and 2 decimal places
                value = "{:,.2f}".format(float(value))
            except (ValueError, TypeError):
                # Handle cases where the value is not a valid number
                pass
        return super().render(name, value, attrs, renderer)

class ShortDateInput(forms.DateInput):
    pass
    
    # def format_value(self, value):
    #     if value is None:
    #         return ''
    #     return format(value, "%y/%m/%d")  # Format as YY/M/D

class InputFieldForm(forms.ModelForm):
    DELETE = forms.BooleanField(required=False, widget=forms.HiddenInput)  # Add delete field

    class Meta:
        model = InputField
        fields = [
            '物件ID', 'テナントID', '管理項目コード', '契約ID', '請求金額',
        ]


InputFieldFormSet = modelformset_factory(
    InputField,
    form=InputFieldForm,
    extra=1,  # Start with 1 empty form
    can_delete=True  # Enable deletion
)

class RevenueInputForm(forms.ModelForm):
    DELETE = forms.BooleanField(required=False, widget=forms.HiddenInput)  # Add delete field

    class Meta:
        model = 売上
        fields = [
            '物件ID', 'テナントID', '管理項目コード', '契約ID', 'レポート日',
            '該当月開始月','該当月終了月','請求書発行日','請求金額','請求消費税','請求税込金額','当月入金日',
            '備考',
        ]
        widgets = {
            '請求金額': CommaSeparatedInput(attrs={'class': 'comma-separated'}),
            '請求消費税': CommaSeparatedInput(attrs={'class': 'comma-separated'}),
            '請求税込金額': CommaSeparatedInput(attrs={'class': 'comma-separated'}),
            '該当月開始月': ShortDateInput(attrs={'class': 'short-date-input'}),
            '該当月終了月': ShortDateInput(attrs={'class': 'short-date-input'}),
            '請求書発行日': ShortDateInput(attrs={'class': 'short-date-input'}),
            '当月入金日': ShortDateInput(attrs={'class': 'short-date-input'}),
        }
    
class BaseRevenueInputFormSet(BaseModelFormSet):
    def clean(self):
        selected_bukken = self.data.get('bukken')
        selected_month = self.data.get('months')
        start_date = datetime.strptime(selected_month, '%B %d %Y')
        start_of_month = start_date.strftime('%Y-%m-01')
        print("selected_bukken in formset", selected_bukken)
        print("selected_month in formset", selected_month)
        print("selected_month in formset", start_of_month)

        for form in self.forms:
            if not form.cleaned_data.get('物件ID'):
                form.cleaned_data['物件ID'] = selected_bukken
            if not form.cleaned_data.get('レポート日'):
                form.cleaned_data['レポート日'] = start_of_month
                
        super().clean()

RevenueInputFormSet = modelformset_factory(売上, form=RevenueInputForm, formset=BaseRevenueInputFormSet, extra=1, can_delete=True)



###　契約項目を設定する
class ContractInputForm(forms.ModelForm):
    DELETE = forms.BooleanField(required=False, widget=forms.HiddenInput)  # Add delete field

    class Meta:
        model = 契約
        fields = [
            '契約ID', 'テナントID', '物件ID', '部屋番号', '契約日',
            '当初開始日','当初終了日','現在契約開始日','現在契約終了日','賃料金額','共益費','契約種類',
            '自動更新','契約年数','更新料有無','更新料金額','解約通知期間','居室タイプ','平米数',
            '坪数','保証金金額','保証金月数','保証有無','保証会社コード','フリーレント','備考',
        ]
        widgets = {
            '賃料金額': CommaSeparatedInput(attrs={'class': 'comma-separated'}),
            '共益費': CommaSeparatedInput(attrs={'class': 'comma-separated'}),
            '更新料金額': CommaSeparatedInput(attrs={'class': 'comma-separated'}),
            '保証金金額': CommaSeparatedInput(attrs={'class': 'comma-separated'}),
            '契約年数': CommaSeparatedInput(attrs={'class': 'comma-separated'}),
            '解約通知期間': CommaSeparatedInput(attrs={'class': 'comma-separated'}),
            '保証金月数': CommaSeparatedInput(attrs={'class': 'comma-separated'}),
            '契約日': ShortDateInput(attrs={'class': 'short-date-input'}),
            '当初開始日': ShortDateInput(attrs={'class': 'short-date-input'}),
            '当初終了日': ShortDateInput(attrs={'class': 'short-date-input'}),
            '現在契約開始日': ShortDateInput(attrs={'class': 'short-date-input'}),
            '現在契約終了日': ShortDateInput(attrs={'class': 'short-date-input'}),
        }


ContractInputFormSet = modelformset_factory(
    契約,
    form=ContractInputForm,
    extra=1,  # Start with 1 empty form
    can_delete=True  # Enable deletion
)

###　物件設定を設定する
class 物件InputForm(forms.ModelForm):
    DELETE = forms.BooleanField(required=False, widget=forms.HiddenInput)  # Add delete field

    class Meta:
        model = 物件
        fields = [
            '物件名', '物件住所', '物件種類', '建築年月日', '敷地面積','床面積', '構造'
        ]
        widgets = {
            '敷地面積': DeciSeparatedInput(attrs={'class': 'deci-separated'}),
            '床面積': DeciSeparatedInput(attrs={'class': 'deci-separated'}),
        }


物件InputFormSet = modelformset_factory(
    物件,
    form=物件InputForm,
    extra=1,  # Start with 1 empty form
    can_delete=True  # Enable deletion
)

###　テナント設定を設定する
class テナントInputForm(forms.ModelForm):
    DELETE = forms.BooleanField(required=False, widget=forms.HiddenInput)  # Add delete field

    class Meta:
        model = テナント
        fields = [
            'id','テナント名', 'テナント短縮名', 'テナント住所', 'テナント電話番号', 'テナント担当者名', 'テナントソート'
        ]
        
テナントInputFormSet = modelformset_factory(
    テナント,
    form=テナントInputForm,
    extra=1,  # Start with 1 empty form
    can_delete=True  # Enable deletion
)

###　敷金保証金を設定する
class 敷金保証金InputForm(forms.ModelForm):
    DELETE = forms.BooleanField(required=False, widget=forms.HiddenInput)  # Add delete field

    class Meta:
        model = 敷金保証金
        fields = [
            '契約番号','物件ID', 'テナントID', '契約区画', '定借区分', '前月末残高','当月増額', '当月減少',
            '今月末残高', '移動予定日', '保証会社コード', '種類', '備考'
        ]
        widgets = {
            '前月末残高': CommaSeparatedInput(attrs={'class': 'comma-separated'}),
            '当月増額': CommaSeparatedInput(attrs={'class': 'comma-separated'}),
            '当月減少': CommaSeparatedInput(attrs={'class': 'comma-separated'}),
            '今月末残高': CommaSeparatedInput(attrs={'class': 'comma-separated'}),
        }

敷金保証金InputFormSet = modelformset_factory(
    敷金保証金,
    form=敷金保証金InputForm,
    extra=1,  # Start with 1 empty form
    can_delete=True  # Enable deletion
)

###　管理項目設定を設定する
class 管理項目InputForm(forms.ModelForm):
    DELETE = forms.BooleanField(required=False, widget=forms.HiddenInput)  # Add delete field

    class Meta:
        model = 管理項目
        fields = [
            '管理項目コード', '管理項目印字名', '管理項目短縮名', '管理項目レポート分類区分'
        ]
        
管理項目InputFormSet = modelformset_factory(
    管理項目,
    form=管理項目InputForm,
    extra=1,  # Start with 1 empty form
    can_delete=True  # Enable deletion
)

###　保証会社設定を設定する
class 保証会社InputForm(forms.ModelForm):
    DELETE = forms.BooleanField(required=False, widget=forms.HiddenInput)  # Add delete field

    class Meta:
        model = 保証会社
        fields = [
            '保証会社コード', '保証会社名', '保証会社住所', '保証会社担当者名', '保証会社連絡先'
        ]
        
保証会社InputFormSet = modelformset_factory(
    保証会社,
    form=保証会社InputForm,
    extra=1,  # Start with 1 empty form
    can_delete=True  # Enable deletion
)

###　支払先設定を設定する
class 支払先InputForm(forms.ModelForm):
    DELETE = forms.BooleanField(required=False, widget=forms.HiddenInput)  # Add delete field

    class Meta:
        model = 支払先
        fields = [
            '支払先コード', '請求先名', '請求先住所', '請求先担当者', '請求先電話番号'
        ]
        
支払先InputFormSet = modelformset_factory(
    支払先,
    form=支払先InputForm,
    extra=1,  # Start with 1 empty form
    can_delete=True  # Enable deletion
)

###　ステータスを設定する
class ステータスInputForm(forms.ModelForm):
    DELETE = forms.BooleanField(required=False, widget=forms.HiddenInput)  # Add delete field

    class Meta:
        model = ステータス
        fields = [
            'レポート日', '物件ID', '新テナント', 'テナント関連', '遅延状況',
            '検査情報', 'メンテナンス', 'その他', '特別項目', 
        ]
        widgets = {
            '新テナント': forms.Textarea(attrs={'rows': 5}),
            'テナント関連': forms.Textarea(attrs={'rows': 5}),
            '遅延状況': forms.Textarea(attrs={'rows': 5}),
            '検査情報': forms.Textarea(attrs={'rows': 5}),
            'メンテナンス': forms.Textarea(attrs={'rows': 5}),
            'その他': forms.Textarea(attrs={'rows': 5}),
            '特別項目': forms.Textarea(attrs={'rows': 5}),
        }

ステータスInputFormSet = modelformset_factory(
    ステータス,
    form=ステータスInputForm,
    extra=0,  # Start with 1 empty form
    can_delete=True  # Enable deletion
)

#費用入力を設定する
class 費用InputForm(forms.ModelForm):
    DELETE = forms.BooleanField(required=False, widget=forms.HiddenInput)  # Add delete field

    class Meta:
        model = 費用
        fields = [
            '物件ID', '支払先コード', '管理項目コード', 'レポート日', '当該月開始月', '当該月終了月', 
            '請求書発行月', '計上日', '請求金額', '請求消費税', '請求税金込', '当月支払日', 
            '備考', 
        ]
        widgets = {
            '請求金額': CommaSeparatedInput(attrs={'class': 'comma-separated'}),
            '請求消費税': CommaSeparatedInput(attrs={'class': 'comma-separated'}),
            '請求税金込': CommaSeparatedInput(attrs={'class': 'comma-separated'}),
            'レポート日': ShortDateInput(attrs={'class': 'short-date-input'}),
            '当該月開始月': ShortDateInput(attrs={'class': 'short-date-input'}),
            '当該月終了月': ShortDateInput(attrs={'class': 'short-date-input'}),
            '請求書発行月': ShortDateInput(attrs={'class': 'short-date-input'}),
            '計上日': ShortDateInput(attrs={'class': 'short-date-input'}),
            '当月支払日': ShortDateInput(attrs={'class': 'short-date-input'}),
        }

費用InputFormSet = modelformset_factory(
    費用,
    form=費用InputForm,
    extra=1,  # Start with 1 empty form
    can_delete=True  # Enable deletion
)

###　BM入力を設定する（物件ソート）
class BMInputFieldForm(forms.ModelForm):
    DELETE = forms.BooleanField(required=False, widget=forms.HiddenInput)  # Add delete field

    class Meta:
        model = BMInputField
        fields = [
            '物件ID', 'BM項目', 'BM回数', 'BM予定数', 
        ]

BMInputFieldFormSet = modelformset_factory(
    BMInputField,
    form=BMInputFieldForm,
    extra=1,  # Start with 1 empty form
    can_delete=True  # Enable deletion
)

###　BM項目設定を設定する（ソートはなし。ただ項目を設定するのみ。）
class BMItemForm(forms.ModelForm):
    DELETE = forms.BooleanField(required=False, widget=forms.HiddenInput)  # Add delete field

    class Meta:
        model = BMItems
        fields = [
            'BM項目','BM項目CD', 'BM内容説明',
        ]

BMItemFormSet = modelformset_factory(
    BMItems,
    form=BMItemForm,
    extra=1,  # Start with 1 empty form
    can_delete=True  # Enable deletion
)

###　BM報告を設定する（物件及び年月でソート）
class BMForm(forms.ModelForm):
    DELETE = forms.BooleanField(required=False, widget=forms.HiddenInput)  # Add delete field

    class Meta:
        model = BM入力フォーム
        fields = [
            '物件ID', 'レポート日','BM項目','BM回数','BM予定数','BM予定','BM実施','BMコメント',
        ]

BMFormSet = modelformset_factory(
    BM入力フォーム,
    form=BMForm,
    extra=1,  # Start with 1 empty form
    can_delete=True  # Enable deletion
)
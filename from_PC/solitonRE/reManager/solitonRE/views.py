from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from .models import テナント, 物件, 管理項目, 契約, 支払先, 保証会社, 敷金保証金, 売上, 費用, ステータス, MonthSelect, InputField, BMItems, BMInputField, BM入力フォーム
from django.urls import reverse_lazy, reverse
from datetime import datetime, timedelta
from django.views.generic.base import TemplateResponseMixin, View
from django.views.generic.list import ListView
from .forms import InputFieldFormSet,  RevenueInputFormSet, ContractInputFormSet, 物件InputFormSet, テナントInputFormSet, 敷金保証金InputFormSet, 管理項目InputFormSet, 保証会社InputFormSet, 支払先InputFormSet, ステータスInputFormSet, 費用InputFormSet, BMInputFieldFormSet, BMItemFormSet, BMFormSet
from django.db.models import Sum
import csv, io
from django.core.management import call_command
from collections import defaultdict


#  konno
#  kkonno@solition-cm.com
#  yuta0126

# Create your views here.
def main(request):
    bukkens = 物件.objects.all()
    months = MonthSelect.objects.all()
    return render(request, 'start.html', {'bukkens':bukkens, 'months':months})

def console(request):
    bukken = request.GET.get('bukken')
    month = request.GET.get('months')
    action = request.GET.get('action')

    # Determine which button was pressed and redirect accordingly
    if action == "売上リスト":
        url = reverse('solitonRE:売上-list')  # This gets the URL pattern for '売上-input'
        query_params = f'?bukken={bukken}&months={month}'
        redirect_url = f'{url}{query_params}'
        return HttpResponseRedirect(redirect_url)
    elif action == "売上入力":
        url = reverse('solitonRE:売上-input')  # This gets the URL pattern for '売上-input'
        query_params = f'?bukken={bukken}&months={month}'
        redirect_url = f'{url}{query_params}'
        return HttpResponseRedirect(redirect_url)
    elif action == "ステータス":
        url = reverse('solitonRE:ステータス-input')  # This gets the URL pattern for '売上-input'
        query_params = f'?bukken={bukken}&months={month}'
        redirect_url = f'{url}{query_params}'
        return HttpResponseRedirect(redirect_url)
    elif action == "費用":
        url = reverse('solitonRE:費用-input')  # This gets the URL pattern for '売上-input'
        query_params = f'?bukken={bukken}&months={month}'
        redirect_url = f'{url}{query_params}'
        return HttpResponseRedirect(redirect_url)
    elif action == "BM報告":
        url = reverse('solitonRE:bm_view')  # This gets the URL pattern for '売上-input'
        query_params = f'?bukken={bukken}&months={month}'
        redirect_url = f'{url}{query_params}'
        return HttpResponseRedirect(redirect_url)
    elif action == "入力項目":
        url = reverse('solitonRE:input_field_view')  # This gets the URL pattern for '売上-input'
        query_params = f'?bukken={bukken}'
        redirect_url = f'{url}{query_params}'
        return HttpResponseRedirect(redirect_url)
    elif action == "契約項目":
        url = reverse('solitonRE:契約-input')  # This gets the URL pattern for '売上-input'
        query_params = f'?bukken={bukken}'
        redirect_url = f'{url}{query_params}'
        return HttpResponseRedirect(redirect_url)
    elif action == "敷金保証金項目":
        url = reverse('solitonRE:敷金保証金-input')  # This gets the URL pattern for '売上-input'
        query_params = f'?bukken={bukken}'
        redirect_url = f'{url}{query_params}'
        return HttpResponseRedirect(redirect_url)
    elif action == "BM入力":
        url = reverse('solitonRE:bminput_field_view')  # This gets the URL pattern for '売上-input'
        query_params = f'?bukken={bukken}'
        redirect_url = f'{url}{query_params}'
        return HttpResponseRedirect(redirect_url)
    # Add other actions as needed


### 売上リスト　を表示
### 売上_list.htmlを使用　　ルートは 売上_list
###  DBは売上, Form:  RevenueInputForm/BaseRevenueInputFormSet/RevenueInputFormSet
class 売上ListView(ListView):
    model = 売上
    template_name = '売上_list.html'
    context_object_name = '売上_list'

    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Get selected bukken and month from GET parameters
        selected_bukken = self.request.GET.get('bukken')
        selected_month = self.request.GET.get('months')

        # Filter by the selected bukken if provided
        if selected_bukken:
            queryset = queryset.filter(物件ID_id=selected_bukken)
            print("first queryset", queryset)
        
        if selected_month:
            start_date = datetime.strptime(selected_month, '%B %d, %Y')
            start_of_month = start_date.strftime('%Y-%m-01')
            end_of_month = (start_date.replace(day=28) + timedelta(days=4)).replace(day=1) - timedelta(days=1)
            queryset = queryset.filter(
                レポート日__gte=start_of_month,
                レポート日__lte=end_of_month
            )
        queryset = queryset.select_related('テナントID', '管理項目コード').order_by(
            '-テナントID__テナントソート',
            '管理項目コード__管理項目レポート分類区分'
        )
   
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get the selected values from GET parameters
        selected_bukken = self.request.GET.get('bukken')
        selected_month = self.request.GET.get('months')

        context['bukkens'] = 物件.objects.all()  # Assuming 物件 is your model name
        context['months'] = MonthSelect.objects.all()  # Replace with your actual month model
        context['selected_bukken'] = selected_bukken  # Selected bukken value
        context['selected_month'] = selected_month  # Selected month value

        # Get the filtered queryset
        queryset = self.get_queryset()

        # Initialize a dictionary to store subtotals by テナントID
        tenants_data  = defaultdict(lambda:{'items': [], 'subtotals':{'請求金額': 0, '請求消費税': 0, '請求税込金額': 0}})

        # Calculate subtotals for each テナントID
        for obj in queryset:
            tenant_id = obj.テナントID

            tenants_data[tenant_id]['items'].append({
                '管理項目コード': obj.管理項目コード,
                'レポート日': obj.レポート日.strftime('%Y-%m-%d') if obj.レポート日 else '',
                '該当月開始月': obj.該当月開始月.strftime('%Y-%m-%d') if obj.該当月開始月 else '',
                '該当月終了月': obj.該当月終了月.strftime('%Y-%m-%d') if obj.該当月終了月 else '',
                '請求書発行日': obj.請求書発行日.strftime('%Y-%m-%d') if obj.請求書発行日 else '',
                '請求金額': obj.請求金額 or 0,
                '請求消費税': obj.請求消費税 or 0,
                '請求税込金額': obj.請求税込金額 or 0,
                '当月入金日': obj.当月入金日.strftime('%Y-%m-%d') if obj.当月入金日 else '',
                '備考': obj.備考 or '',
            })
            tenants_data[tenant_id]['subtotals']['請求金額'] += obj.請求金額 or 0
            tenants_data[tenant_id]['subtotals']['請求消費税'] += obj.請求消費税 or 0
            tenants_data[tenant_id]['subtotals']['請求税込金額'] += obj.請求税込金額 or 0 # Add subtotals to context
        
        context['tenants_data'] = dict(tenants_data)

        grand_totals = {
            'total_請求金額': 0,
            'total_請求消費税': 0,
            'total_請求税込金額': 0,
        }

        for tenant_data in tenants_data.values():
            for item in tenant_data['items']:
                grand_totals['total_請求金額'] += item['請求金額']
                grand_totals['total_請求消費税'] += item['請求消費税']
                grand_totals['total_請求税込金額'] += item['請求税込金額']

        context['grand_totals'] = grand_totals

        from pprint import pprint  
        print(f"Type of subtotals: {type(tenants_data)}")             #debugging
        pprint(tenants_data)           #debugging

        return context
    
    def post(self, request, *args, **kwargs):
        if 'export_csv' in request.POST:
            queryset = self.get_queryset()
            if queryset is not None:
                return self.export_to_csv(queryset)
            else:
                return HttpResponse("No data available to export.", content_type="text/plain")
        
        formset = RevenueInputFormSet(self.request.POST, queryset=self.get_queryset())
        if formset.is_valid():
            formset.save()
            return HttpResponseRedirect(reverse('solitonRE:売上-input'))
        else:
            context = self.get_context_data(formset=formset)
            return render(request, self.template_name, context)
        
    def export_to_csv(self, queryset):
        response = HttpResponse(content_type='text/csv', charset='utf_8_sig')
        response['Content-Disposition'] = 'attachment; filename = Revenue_list.csv'
        # response.write("\xEF\xBB\xBF")
        writer = csv.writer(response, delimiter=',')

        writer.writerow(['物件ID', 'テナントID', '管理項目短縮名', '契約ID',
                         'レポート日', '該当月開始月', '該当月終了月', '請求書発行日', 
                         '請求金額', '請求消費税', '請求税込金額', '当月入金日', '備考'
                         ])

        for obj in queryset:
            writer.writerow([
                obj.物件ID.物件名,  # Assuming 物件ID is a ForeignKey
                obj.テナントID.テナント短縮名,  # Assuming テナントID is a ForeignKey
                obj.管理項目コード.管理項目短縮名,  # Assuming 管理項目コード is a related object with a code field
                obj.契約ID.契約ID,  # Assuming 契約ID is a ForeignKey
                obj.レポート日.strftime('%Y-%m-%d'),  # Format the date as a string
                obj.該当月開始月.strftime('%Y-%m-%d') if obj.該当月開始月 else '',
                obj.該当月終了月.strftime('%Y-%m-%d') if obj.該当月終了月 else '',
                obj.請求書発行日.strftime('%Y-%m-%d') if obj.請求書発行日 else '',  # Format the date as a string
                obj.請求金額 if obj.請求金額 is not None else '',
                obj.請求消費税 if obj.請求消費税 is not None else '',
                obj.請求税込金額 if obj.請求税込金額 is not None else '',
                obj.当月入金日.strftime('%Y-%m-%d') if obj.当月入金日 else '',
                obj.備考 if obj.備考 else '',
            ])
        
        return response

###  入力項目を設定する
###  テンプレートはinput_field.html  ルートはinput_field_view
###  DBはInputField, Form:  InputFieldForm/InputFieldFormSet
class InputFieldView(View):
    template_name = 'input_field.html'

    def get(self, request, *args, **kwargs):
        bukken_id = request.GET.get('bukken')  
        print("bukken_id data:", bukken_id)
        bukkens = 物件.objects.all()
        months = MonthSelect.objects.all() 
        selected_bukken = request.GET.get('bukken', None)
        
        if bukken_id:
            formset = InputFieldFormSet(
                queryset=InputField.objects.filter(物件ID_id=bukken_id).order_by('テナントID','管理項目コード')
                )
        else:
            formset = InputFieldFormSet(queryset=InputField.objects.none())
        return render(request, self.template_name, {
            'formset': formset, 
            'bukken_id': bukken_id, 
            'bukkens':bukkens, 
            'months':months, 
            'selected_bukken': selected_bukken
            })

    def post(self, request, *args, **kwargs):
        print("kwargs print", kwargs)
        if kwargs:
            bukken_id = kwargs.get['pk']
            selected_bukken = bukken_id
            print("request data pk", bukken_id)
        else:
            bukken_id = request.POST.get('bukken') 
            selected_bukken = request.POST.get('bukken', None)
        print("request data", request.POST)  # Print POST data for debugging

        bukkens = 物件.objects.all()
        months = MonthSelect.objects.all() 

        if not bukken_id:
            bukken_id = request.POST.get('form-0-物件ID')
            selected_bukken = bukken_id
            print("bukken_id print", bukken_id)
        elif not request.POST.get('form-0-物件ID'):
            formset = InputFieldFormSet(queryset=InputField.objects.none())
            return render(request, self.template_name, {'formset': formset})
        
        formset = InputFieldFormSet(request.POST, queryset=InputField.objects.filter(物件ID_id=bukken_id))
        if formset.is_valid():
            formset.save()
            formset = InputFieldFormSet(queryset=InputField.objects.filter(物件ID_id=bukken_id))
            return render(request, self.template_name, {
            'formset': formset, 
            'bukken_id': bukken_id,
            'bukkens':bukkens, 
            'months':months, 
            'selected_bukken': selected_bukken
            })
        else:
            print("error",formset.errors)
        return render(request, self.template_name, {
            'formset': formset, 
            'bukken_id': bukken_id,
            'bukkens':bukkens, 
            'months':months, 
            'selected_bukken': selected_bukken
            })

###　　売上入力を設定する
###  テンプレートは売上_input.html  ルートは売上-input
###  DBはInputField, Form:  InputFieldForm/InputFieldFormSet
class 売上InputView(View):
    template_name = '売上_input.html'

    def get_queryset(self):
        queryset = 売上.objects.all()  # Use your model's queryset
        
        # Get selected bukken and month from GET parameters
        selected_bukken = self.request.GET.get('bukken')
        selected_month = self.request.GET.get('months')
   
        # Filter by the selected bukken if provided
        if selected_bukken:
            queryset = queryset.filter(物件ID=selected_bukken)
        
        if selected_month:
            start_date = datetime.strptime(selected_month, '%B %d, %Y')
            start_of_month = start_date.strftime('%Y-%m-01')
            end_of_month = (start_date.replace(day=28) + timedelta(days=4)).replace(day=1) - timedelta(days=1)
            
            queryset = queryset.filter(
                レポート日__gte=start_of_month,
                レポート日__lte=end_of_month
            )

            queryset = queryset.select_related('テナントID', '管理項目コード').order_by(
                '-テナントID__テナントソート',
                '管理項目コード__管理項目レポート分類区分'
            )

        return queryset if queryset.exists() else None
    
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if queryset is None:
            context = self.get_context_data()
            context['message'] = 'No data found. Would you like to create a new dataset?'
            context['show_create_button'] = True
            return render(request, self.template_name, context)
        
        formset = RevenueInputFormSet(queryset=self.get_queryset())
        context = self.get_context_data(formset=formset)
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        
        print("request in POST", request)
        selected_bukken = request.POST.get('bukken', None)
        selected_month = request.POST.get('months', None)
        print("selected_bukken in POST", selected_bukken)
        print("selected_month in POST", selected_month)

        if 'create_new_dataset' in request.POST:
            # Call the create_new_dataset method
            selected_bukken = request.POST.get('bukken', None)
            selected_month = request.POST.get('months', None)
            self.create_new_dataset(request, selected_bukken, selected_month)
            # After dataset creation, redirect to the input page
            url = reverse('solitonRE:売上-input')  # This gets the URL pattern for '売上-input'
            query_params = f'?bukken={selected_bukken}&months={selected_month}'
            redirect_url = f'{url}{query_params}'
            return HttpResponseRedirect(redirect_url)

        if 'tax_calc' in request.POST:
            print("tax_calc PASSING!!")
            # Call the create_new_dataset method
            selected_bukken = request.POST.get('bukken', None)
            selected_month = request.POST.get('months', None)
            self.tax_calc_def(selected_bukken, selected_month)
            # After dataset creation, redirect to the input page
            url = reverse('solitonRE:売上-input')  # This gets the URL pattern for '売上-input'
            query_params = f'?bukken={selected_bukken}&months={selected_month}'
            redirect_url = f'{url}{query_params}'
            return HttpResponseRedirect(redirect_url)
        
        print("this part of post is now passing through")
        cleaned_post_data = request.POST.copy()
        for key, value in cleaned_post_data.items():
            cleaned_post_data[key] = value.replace(',', '')
            
        formset = RevenueInputFormSet(cleaned_post_data, queryset=self.get_queryset())   
        # formset = RevenueInputFormSet(self.request.POST, queryset=self.get_queryset())
        
        if formset.is_valid():
            formset.save()
            selected_bukken = request.POST.get('bukken')
            selected_month = request.POST.get('months')
            query_params = f'?bukken={selected_bukken}&months={selected_month}'
            url = reverse('solitonRE:売上-input')
            redirect_url = f'{url}{query_params}'
            return HttpResponseRedirect(redirect_url)
            # return HttpResponseRedirect(reverse('solitonRE:売上-input'))
        else:
            print("formerror", formset.errors)
            context = self.get_context_data(formset=formset)
            return render(request, self.template_name, context)

    def get_context_data(self, **kwargs):
        context = {}

        # Get the selected values from GET parameters
        selected_bukken = self.request.GET.get('bukken')
        selected_month = self.request.GET.get('months')

        context['bukkens'] = 物件.objects.all()  # Assuming 物件 is your model name
        context['months'] = MonthSelect.objects.all()  # Replace with your actual month model
        context['selected_bukken'] = selected_bukken  # Selected bukken value
        context['selected_month'] = selected_month  # Selected month value

        context.update(kwargs)  # Include formset in the context
        return context
    
    def create_new_dataset(self, request, selected_bukken, selected_month):
        bukken_instance = 物件.objects.get(id=selected_bukken)
        start_date = datetime.strptime(selected_month, '%B %d, %Y')
        # Get selected_info from InputField
        selected_infos = InputField.objects.filter(物件ID_id=selected_bukken)
        if not selected_infos:
            print("No selected_info found.")
            # Handle the case where no data is found
            return  # or raise an error

        for selected_info in selected_infos:
            print(f"Type of 管理項目コード: {type(selected_info.管理項目コード)}")
            print("selected_info.管理項目コード", selected_info.管理項目コード)
            code = selected_info.管理項目コード.管理項目コード.strip()
            print("code:", code)
            if code in ['110010', '110011', '110020']:
                # Calculate next month
                next_month = (start_date.replace(day=28) + timedelta(days=4)).replace(day=1)
                end_of_next_month = (next_month + timedelta(days=31)).replace(day=1) - timedelta(days=1)
                print(f"next_month: {next_month}")
                print(f"end_of_next_month: {end_of_next_month}")
                該当月開始月 = next_month.strftime('%Y-%m-01')
                該当月終了月 = end_of_next_month.strftime('%Y-%m-%d')
            elif code in ['110090', '110091']:
                # Calculate previous month
                previous_month = (start_date.replace(day=1) - timedelta(days=1)).replace(day=1)
                end_of_previous_month = (start_date.replace(day=1) - timedelta(days=1)).strftime('%Y-%m-%d')
                該当月開始月 = previous_month.strftime('%Y-%m-01')
                該当月終了月 = end_of_previous_month
            else:
                # Default case
                該当月開始月 = start_date.strftime('%Y-%m-01')
                該当月終了月 = (start_date.replace(day=28) + timedelta(days=4)).replace(day=1) - timedelta(days=1)
                該当月終了月 = 該当月終了月.strftime('%Y-%m-%d')
            # Create new dataset
            new_data = 売上.objects.create(
                物件ID=bukken_instance,
                テナントID=selected_info.テナントID,
                管理項目コード=selected_info.管理項目コード,  # Adding data from selected_info
                契約ID=selected_info.契約ID,
                レポート日=start_date,  # Assuming this should be the start date of the selected month
                該当月開始月=該当月開始月,
                該当月終了月=該当月終了月,
                請求書発行日=start_date,
                請求金額=selected_info.請求金額,
                請求消費税=int(selected_info.請求金額 * 0.1),
                請求税込金額=selected_info.請求金額 + int(selected_info.請求金額 * 0.1),
            )

        new_data.save()

    def tax_calc_def(self, selected_bukken, selected_month):
        queryset = 売上.objects.all()  # Use your model's queryset

        # Filter by the selected bukken if provided
        if selected_bukken:
            queryset = queryset.filter(物件ID=selected_bukken)
        
        if selected_month:
            start_date = datetime.strptime(selected_month, '%B %d, %Y')
            start_of_month = start_date.strftime('%Y-%m-01')
            end_of_month = (start_date.replace(day=28) + timedelta(days=4)).replace(day=1) - timedelta(days=1)
            
            queryset = queryset.filter(
                レポート日__gte=start_of_month,
                レポート日__lte=end_of_month
            )
        print("BEFORE QUERY SET TAX")
        for query in queryset:
            print("QUERY", query)
            print("QUERY 管理項目コード", query.管理項目コード)
            print("QUERY 管理項目コード", query.管理項目コード, type(query.管理項目コード))
            if query.管理項目コード.管理項目短縮名 in ['電気', '水道']:
                print("管理項目コード KANRI CODE", query.管理項目コード)
                query.請求消費税 = int(query.請求税込金額*(1-1/1.1))
                print("請求消費税 KANRI CODE", query.請求消費税)
                query.請求金額 = query.請求税込金額 - query.請求消費税
                query.save()

###　費用入力を設定する
###  テンプレートは費用_input.html  ルートは費用-input
###  DBは費用, Form:  費用InputForm/費用InputFormSet           
class 費用InputView(View):
    template_name = '費用_input.html'

    def get_queryset(self):
        queryset = 費用.objects.all()  # Use your model's queryset
        
        # Get selected bukken and month from GET parameters
        selected_bukken = self.request.GET.get('bukken')
        selected_month = self.request.GET.get('months')
   
        # Filter by the selected bukken if provided
        if selected_bukken:
            queryset = queryset.filter(物件ID=selected_bukken)
        
        if selected_month:
            start_date = datetime.strptime(selected_month, '%B %d, %Y')
            start_of_month = start_date.strftime('%Y-%m-01')
            end_of_month = (start_date.replace(day=28) + timedelta(days=4)).replace(day=1) - timedelta(days=1)
            
            queryset = queryset.filter(
                レポート日__gte=start_of_month,
                レポート日__lte=end_of_month
            )

        return queryset 

    def get_queryset_csv(self, selected_bukken, selected_month):
        queryset = 費用.objects.all()  # Use your model's queryset
        if selected_bukken:
            queryset = queryset.filter(物件ID=selected_bukken)
        if selected_month:
            start_date = datetime.strptime(selected_month, '%B %d, %Y')
            start_of_month = start_date.strftime('%Y-%m-01')
            end_of_month = (start_date.replace(day=28) + timedelta(days=4)).replace(day=1) - timedelta(days=1)
            queryset = queryset.filter(レポート日__gte=start_of_month,レポート日__lte=end_of_month)
        return queryset 
    
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if queryset is None:
            context = self.get_context_data()
            context['message'] = 'No data found. Would you like to create a new dataset?'
            context['show_create_button'] = True
            return render(request, self.template_name, context)
        
        formset = 費用InputFormSet(queryset=self.get_queryset())
        context = self.get_context_data(formset=formset)
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        
        if 'create_new_dataset' in request.POST:
            # Call the create_new_dataset method
            selected_bukken = request.POST.get('bukken', None)
            selected_month = request.POST.get('months', None)
            self.create_new_dataset(request, selected_bukken, selected_month)
            # After dataset creation, redirect to the input page
            url = reverse('solitonRE:費用-input')  # This gets the URL pattern for '売上-input'
            query_params = f'?bukken={selected_bukken}&months={selected_month}'
            redirect_url = f'{url}{query_params}'
            return HttpResponseRedirect(redirect_url)

        if 'export_csv' in request.POST:
            selected_bukken = request.POST.get('bukken', None)
            selected_month = request.POST.get('months', None)
            print("bukken for csv", selected_bukken)
            print("month for csv", selected_month)
            queryset = self.get_queryset_csv(selected_bukken, selected_month)
            if queryset is not None:
                return self.export_to_csv(queryset)
            else:
                return HttpResponse("No data available to export.", content_type="text/plain")
            
        if 'tax_calc' in request.POST:
            print("tax_calc PASSING!!")
            # Call the create_new_dataset method
            selected_bukken = request.POST.get('bukken', None)
            selected_month = request.POST.get('months', None)
            self.tax_calc_def(selected_bukken, selected_month)
            # After dataset creation, redirect to the input page
            url = reverse('solitonRE:費用-input')  # This gets the URL pattern for '売上-input'
            query_params = f'?bukken={selected_bukken}&months={selected_month}'
            redirect_url = f'{url}{query_params}'
            return HttpResponseRedirect(redirect_url)

        selected_bukken = request.POST.get('bukken', None)
        selected_month = request.POST.get('months', None)
        print("this part of post is now passing through")
        print("bukken for save", selected_bukken)
        print("month for save", selected_month)
        

        cleaned_post_data = request.POST.copy()
        for key, value in cleaned_post_data.items():
            cleaned_post_data[key] = value.replace(',', '')
            
        formset = 費用InputFormSet(cleaned_post_data, queryset=self.get_queryset())    
        if formset.is_valid():
            formset.save()
            selected_bukken = request.POST.get('bukken')
            selected_month = request.POST.get('months')
            query_params = f'?bukken={selected_bukken}&months={selected_month}'
            url = reverse('solitonRE:費用-input')
            redirect_url = f'{url}{query_params}'
            return HttpResponseRedirect(redirect_url)
            # return HttpResponseRedirect(reverse('solitonRE:費用-input'))
        else:
            print("invalid formset", formset.errors)
            context = self.get_context_data(formset=formset)
            return render(request, self.template_name, context)

    def get_context_data(self, **kwargs):
        context = {}

        # Get the selected values from GET parameters
        selected_bukken = self.request.GET.get('bukken')
        selected_month = self.request.GET.get('months')

        context['bukkens'] = 物件.objects.all()  # Assuming 物件 is your model name
        context['months'] = MonthSelect.objects.all()  # Replace with your actual month model
        context['selected_bukken'] = selected_bukken  # Selected bukken value
        context['selected_month'] = selected_month  # Selected month value

        context.update(kwargs)  # Include formset in the context
        return context
    
    def create_new_dataset(self, request, selected_bukken, selected_month):
        bukken_instance = 物件.objects.get(id=selected_bukken)
        start_date = datetime.strptime(selected_month, '%B %d, %Y')
        start_of_month = start_date.strftime('%Y-%m-01')
        end_of_month = (start_date.replace(day=28) + timedelta(days=4)).replace(day=1) - timedelta(days=1)
        管理項目_instance = 管理項目.objects.get(管理項目コード='210000')
        支払先_instance = 支払先.objects.get(支払先コード='A21000')
        

        new_data = 費用.objects.create(
            物件ID=bukken_instance,
            レポート日=start_date,
            支払先コード=支払先_instance,
            管理項目コード=管理項目_instance,
            当該月開始月=start_of_month,
            当該月終了月=end_of_month,
            請求書発行月=start_date,  # Adjusted field name
            請求金額=0,
            請求消費税=0,
            請求税金込=0,  # Adjusted field name
            当月支払日=end_of_month,
            備考="",
        )

        new_data.save()
    
    def export_to_csv(self, queryset):
        response = HttpResponse(content_type='text/csv', charset='utf_8_sig')
        response['Content-Disposition'] = 'attachment; filename = Expense_list.csv'

        writer = csv.writer(response, delimiter=',')

        writer.writerow(['物件ID', 'レポート日', '請求先名', '管理項目',
                         '当該月開始月', '当該月終了月', '請求書発行月', '請求金額', 
                         '請求消費税', '請求税込金', '当月支払日', '備考'
                         ])

        for obj in queryset:
            writer.writerow([
                obj.物件ID.物件名,  # Assuming 物件ID is a ForeignKey
                obj.レポート日.strftime('%Y-%m-%d'),  # Format the date as a string
                obj.支払先コード.請求先名,  # Assuming テナントID is a ForeignKey
                obj.管理項目コード.管理項目短縮名,  # Assuming 管理項目コード is a related object with a code field
                obj.当該月開始月.strftime('%Y-%m-%d') if obj.当該月開始月 else '',
                obj.当該月終了月.strftime('%Y-%m-%d') if obj.当該月終了月 else '',
                obj.請求書発行月.strftime('%Y-%m-%d') if obj.請求書発行月 else '',  # Format the date as a string
                obj.請求金額 if obj.請求金額 is not None else '',
                obj.請求消費税 if obj.請求消費税 is not None else '',
                obj.請求税金込 if obj.請求税金込 is not None else '',
                obj.当月支払日.strftime('%Y-%m-%d') if obj.当月支払日 else '',
                obj.備考 if obj.備考 else '',
            ])
        
        return response
    
    def tax_calc_def(self, selected_bukken, selected_month):
        queryset = 費用.objects.all()  # Use your model's queryset
        
        # Filter by the selected bukken if provided
        if selected_bukken:
            queryset = queryset.filter(物件ID=selected_bukken)
            
        if selected_month:
            start_date = datetime.strptime(selected_month, '%B %d, %Y')
            start_of_month = start_date.strftime('%Y-%m-01')
            end_of_month = (start_date.replace(day=28) + timedelta(days=4)).replace(day=1) - timedelta(days=1)
            
            queryset = queryset.filter(
                レポート日__gte=start_of_month,
                レポート日__lte=end_of_month
            )
            print("QUERY SET NO PRINT", queryset)
            # return queryset

        print("BEFORE QUERY SET TAX")
        for query in queryset:
            print("QUERY", query)
            print("QUERY 管理項目コード", query.管理項目コード)
            print("QUERY 管理項目コード", query.管理項目コード, type(query.管理項目コード))
            print("管理項目コード KANRI CODE", query.管理項目コード)
            query.請求消費税 = int(query.請求税金込*(1-1/1.1))
            print("請求消費税 KANRI CODE", query.請求消費税)
            query.請求金額 = query.請求税金込 - query.請求消費税
            query.save()

###　ステータスを設定する
###  テンプレートはステータス_input.html  ルートはステータス-input
###  DBはステータス, Form:  ステータスInputForm/ステータスInputFormSet
class ステータスView(TemplateResponseMixin, View):
    template_name = 'ステータス_input.html'

    def get_queryset(self):
        queryset = ステータス.objects.all()  # Use your model's queryset
        
        # Get selected bukken and month from GET parameters
        selected_bukken = self.request.GET.get('bukken')
        selected_month = self.request.GET.get('months')
   
        # Filter by the selected bukken if provided
        if selected_bukken:
            print(f"Filtered by bukken ID: {selected_bukken}")
            queryset = queryset.filter(物件ID_id=selected_bukken)
        
        if selected_month:
            start_date = datetime.strptime(selected_month, '%B %d, %Y')
            start_of_month = start_date.strftime('%Y-%m-01')
            end_of_month = (start_date.replace(day=28) + timedelta(days=4)).replace(day=1) - timedelta(days=1)
            
            queryset = queryset.filter(
                レポート日__gte=start_of_month,
                レポート日__lte=end_of_month
            )

        return queryset 
    
    def get_queryset_for_csv(self, selected_bukken=None, selected_month=None):
        queryset = ステータス.objects.all()  # Use your model's queryset
        
        if selected_bukken:
            queryset = queryset.filter(物件ID_id=selected_bukken)
        
        if selected_month:
            start_date = datetime.strptime(selected_month, '%B %d, %Y')
            start_of_month = start_date.strftime('%Y-%m-01')
            end_of_month = (start_date.replace(day=28) + timedelta(days=4)).replace(day=1) - timedelta(days=1)
            
            queryset = queryset.filter(
                レポート日__gte=start_of_month,
                レポート日__lte=end_of_month
            )
        return queryset 
    
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        print("queryset", queryset)
        context = self.get_context_data()

        if not queryset:
            context['message'] = 'No data found. Would you like to create a new dataset?'
            context['show_create_button'] = True
        else:        
            formset = ステータスInputFormSet(queryset=self.get_queryset())
            context['formset'] = formset

            selected_bukken = request.POST.get('bukken', None)
            selected_month = request.POST.get('months', None)

            if selected_bukken and selected_month:
                url = reverse('solitonRE:ステータス-input')  # This gets the URL pattern for '売上-input'
                query_params = f'?bukken={selected_bukken}&months={selected_month}'
                redirect_url = f'{url}{query_params}'
                return HttpResponseRedirect(redirect_url)
        
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        # Get values from POST data
        selected_bukken = request.POST.get('bukken', None)
        selected_month = request.POST.get('months', None)


        if 'create_new_ステータス' in request.POST:
            # Call the create_new_dataset method
            self.create_new_ステータス(request, selected_bukken, selected_month)
            # After dataset creation, redirect to the input page
            url = reverse('solitonRE:ステータス-input')
            query_params = f'?bukken={selected_bukken}&months={selected_month}'
            redirect_url = f'{url}{query_params}'
            return HttpResponseRedirect(redirect_url)
        
        if 'export_csv' in request.POST:
            queryset = self.get_queryset_for_csv(selected_bukken, selected_month)
            if queryset is not None:
                return self.export_to_csv(queryset)
            else:
                return HttpResponse("No data available to export.", content_type="text/plain")

        # Handle formset validation and saving
        formset = ステータスInputFormSet(self.request.POST, queryset=self.get_queryset())

        if formset.is_valid():
            formset.save()
            # Redirect after saving
            url = reverse('solitonRE:ステータス-input')
            query_params = f'?bukken={selected_bukken}&months={selected_month}'
            redirect_url = f'{url}{query_params}'
            return HttpResponseRedirect(redirect_url)
        
        for form in formset:
            print(form.errors)
        # Handle formset errors or other conditions here
        return self.render_to_response(self.get_context_data(formset=formset))

    def get_context_data(self, **kwargs):
        context = {}

        # Get the selected values from GET parameters
        selected_bukken = self.request.GET.get('bukken')
        selected_month = self.request.GET.get('months')

        context['bukkens'] = 物件.objects.all()  # Assuming 物件 is your model name
        context['months'] = MonthSelect.objects.all()  # Replace with your actual month model
        context['selected_bukken'] = selected_bukken  # Selected bukken value
        context['selected_month'] = selected_month  # Selected month value

        context.update(kwargs)  # Include formset in the context
        return context
    
    def create_new_ステータス(self, request, selected_bukken, selected_month):
        bukken_instance = 物件.objects.get(id=selected_bukken)
        start_date = datetime.strptime(selected_month, '%B %d, %Y')
        レポート日 = start_date.strftime('%Y-%m-01')

        new_status = ステータス.objects.create(
            レポート日=レポート日,  # Replace with the desired date
            物件ID=bukken_instance
        )

        print(new_status)
    
    def export_to_csv(self, queryset):
        response = HttpResponse(
            content_type="text/csv",
            headers={"Content-Disposition": 'attachment; filename="status_list.csv"'},
            charset='utf_8_sig'
        )

        writer = csv.writer(response, delimiter=',')

        writer.writerow(['レポート日', '物件ID', '新テナント', 'テナント関連',
                         '遅延状況', '検査情報', 'メンテナンス', 'その他', 
                         '特別項目', 
                         ])

        for obj in queryset:
            writer.writerow([
                obj.レポート日.strftime('%Y-%m-%d'),  # Format the date as a string
                obj.物件ID.物件名,  # Assuming 物件ID is a ForeignKey
                obj.新テナント if obj.新テナント else '',
                obj.テナント関連 if obj.テナント関連 else '',
                obj.遅延状況 if obj.遅延状況 else '',  # Format the date as a string
                obj.検査情報 if obj.検査情報 is not None else '',
                obj.メンテナンス if obj.メンテナンス is not None else '',
                obj.その他 if obj.その他 is not None else '',
                obj.特別項目 if obj.特別項目 else '',
            ])
        
        return response

###　契約項目を設定する
###  テンプレートは契約_input.html  ルートは契約-input
###  DBは契約, Form:  ContractInputForm/ContractInputFormSet
class 契約View(View):
    template_name = '契約_input.html'

    def get(self, request, *args, **kwargs):
        bukken_id = request.GET.get('bukken')  
        print("bukken_id data:", bukken_id)
        bukkens = 物件.objects.all()
        months = MonthSelect.objects.all() 
        selected_bukken = request.GET.get('bukken', None)
        
        if bukken_id:
            formset = ContractInputFormSet(
                queryset=契約.objects.filter(物件ID_id=bukken_id).order_by('部屋番号')
                )

        else:
            formset = ContractInputFormSet(queryset=契約.objects.none())
        return render(request, self.template_name, {
            'formset': formset, 
            'bukken_id': bukken_id, 
            'bukkens':bukkens, 
            'months':months, 
            'selected_bukken': selected_bukken
            })

    def post(self, request, *args, **kwargs):
        print("kwargs print", kwargs)
        bukken_id = request.POST.get('form-0-物件ID')
        if kwargs:
            bukken_id = kwargs.get['pk']
            selected_bukken = bukken_id
            print("request data pk", bukken_id)
        else:
            bukken_id = request.POST.get('bukken') 
            selected_bukken = request.POST.get('bukken', None)

        if 'export_csv' in request.POST:
            bukken_id = request.POST.get('form-0-物件ID')
            print("export_csv request data pk", bukken_id)
            queryset=契約.objects.filter(物件ID_id=bukken_id)
            if queryset is not None:
                return self.export_to_csv(queryset)
            else:
                return HttpResponse("No data available to export.", content_type="text/plain")

        bukkens = 物件.objects.all()
        months = MonthSelect.objects.all() 

        if not bukken_id:
            bukken_id = request.POST.get('form-0-物件ID')
            selected_bukken = bukken_id
            print("bukken_id print", bukken_id)
        elif not request.POST.get('form-0-物件ID'):
            formset = ContractInputFormSet(queryset=契約.objects.none())
            return render(request, self.template_name, {'formset': formset})
        
        cleaned_post_data = request.POST.copy()
        for key, value in cleaned_post_data.items():
            cleaned_post_data[key] = value.replace(',', '')
        
        # formset = ContractInputFormSet(request.POST, queryset=契約.objects.filter(物件ID_id=bukken_id))
        formset = ContractInputFormSet(cleaned_post_data, queryset=契約.objects.filter(物件ID_id=bukken_id))
        if formset.is_valid():
            formset.save()
            formset = ContractInputFormSet(queryset=契約.objects.filter(物件ID_id=bukken_id).order_by('部屋番号'))
            return render(request, self.template_name, {
            'formset': formset, 
            'bukken_id': bukken_id,
            'bukkens':bukkens, 
            'months':months, 
            'selected_bukken': selected_bukken
            })
        else:
            print("error",formset.errors)
        return render(request, self.template_name, {
            'formset': formset, 
            'bukken_id': bukken_id,
            'bukkens':bukkens, 
            'months':months, 
            'selected_bukken': selected_bukken
            })
    
    def export_to_csv(self, queryset):
        response = HttpResponse(
            content_type="text/csv",
            headers={"Content-Disposition": 'attachment; filename="contract_list.csv"'},
            charset='utf_8_sig'
        )

        writer = csv.writer(response, delimiter=',')

        writer.writerow(['契約ID', 'テナントID', '物件ID', '部屋番号','契約日', '当初開始日', 
                         '当初終了日', '現在契約開始日', '現在契約終了日', '賃料金額','共益費', '契約種類', 
                         '自動更新', '契約年数', '更新料有無', '更新料金額','解約通知期間', '居室タイプ', 
                         '平米数', '坪数', '保証金金額', '保証金月数','保証有無', '保証会社', 
                         'フリーレント', '備考',
                         ])

        for obj in queryset:
            writer.writerow([
                obj.契約ID,  # Format the date as a string
                obj.テナントID.テナント短縮名,  # Assuming 物件ID is a ForeignKey
                obj.物件ID.物件名,  # Assuming 物件ID is a ForeignKey
                obj.部屋番号 if obj.部屋番号 else '',
                obj.契約日.strftime('%Y-%m-%d') if obj.契約日 else '',
                obj.当初開始日.strftime('%Y-%m-%d') if obj.当初開始日 is not None else '',  # Format the date as a string
                obj.現在契約開始日.strftime('%Y-%m-%d') if obj.現在契約開始日 is not None else '',
                obj.現在契約終了日.strftime('%Y-%m-%d') if obj.現在契約終了日 is not None else '',
                obj.賃料金額 if obj.賃料金額 is not None else '',
                obj.共益費 if obj.共益費 is not None else '',
                obj.契約種類 if obj.契約種類 is not None else '',
                obj.自動更新 if obj.自動更新 is not None else '',
                obj.契約年数 if obj.契約年数 is not None else '',
                obj.更新料有無 if obj.更新料有無 is not None else '',
                obj.更新料金額 if obj.更新料金額 is not None else '',
                obj.解約通知期間 if obj.解約通知期間 is not None else '',
                obj.居室タイプ if obj.居室タイプ is not None else '',
                obj.平米数 if obj.平米数 is not None else '',
                obj.坪数 if obj.坪数 is not None else '',
                obj.保証金金額 if obj.保証金金額 is not None else '',
                obj.保証金月数 if obj.保証金月数 is not None else '',
                obj.保証有無 if obj.保証有無 is not None else '',
                obj.保証会社コード.保証会社名 if obj.保証会社コード.保証会社名 is not None else '',
                obj.フリーレント if obj.フリーレント is not None else '',
                obj.備考 if obj.備考 is not None else '',
            ])
        
        return response

###　物件設定を設定する
###  テンプレートは物件_input.html  ルートは物件-input
###  DBは契約, Form:  物件InputForm/物件InputFormSet
class 物件View(View):
    template_name = '物件_input.html'

    def get(self, request, *args, **kwargs):
        bukken_id = request.GET.get('bukken')  
        print("bukken_id data:", bukken_id)
        bukkens = 物件.objects.all()
        months = MonthSelect.objects.all() 
        selected_bukken = request.GET.get('bukken', None)
        
        formset = 物件InputFormSet(queryset=物件.objects.all())
        return render(request, self.template_name, {
            'formset': formset, 
            'bukken_id': bukken_id, 
            'bukkens':bukkens, 
            'months':months, 
            'selected_bukken': selected_bukken
            })

    def post(self, request, *args, **kwargs):
        print("kwargs print", kwargs)
        if kwargs:
            bukken_id = kwargs.get['pk']
            selected_bukken = bukken_id
            print("request data pk", bukken_id)
        else:
            bukken_id = request.POST.get('bukken') 
            selected_bukken = request.POST.get('bukken', None)
        print("request data", request.POST)  # Print POST data for debugging

        bukkens = 物件.objects.all()
        months = MonthSelect.objects.all() 

        if not bukken_id:
            bukken_id = request.POST.get('form-0-物件ID')
            selected_bukken = bukken_id
            print("bukken_id print", bukken_id)
        elif not request.POST.get('form-0-物件ID'):
            formset = 物件InputFormSet(queryset=物件.objects.none())
            return render(request, self.template_name, {'formset': formset})
        
        cleaned_post_data = request.POST.copy()
        for key, value in cleaned_post_data.items():
            cleaned_post_data[key] = value.replace(',', '')
        
        # formset = 物件InputFormSet(request.POST, queryset=物件.objects.all())
        formset = 物件InputFormSet(cleaned_post_data, queryset=物件.objects.all())
        if formset.is_valid():
            formset.save()
            formset = 物件InputFormSet(queryset=物件.objects.all())
            return render(request, self.template_name, {
            'formset': formset, 
            'bukken_id': bukken_id,
            'bukkens':bukkens, 
            'months':months, 
            'selected_bukken': selected_bukken
            })
        else:
            print("error",formset.errors)
        return render(request, self.template_name, {
            'formset': formset, 
            'bukken_id': bukken_id,
            'bukkens':bukkens, 
            'months':months, 
            'selected_bukken': selected_bukken
            })

###　テナント設定を設定する
###  テンプレートはテナント_input.html  ルートはテナント-input
###  DBはテナント, Form:  テナントInputForm/テナントInputFormSet
class テナントView(View):
    template_name = 'テナント_input.html'

    def get(self, request, *args, **kwargs):
        bukken_id = request.GET.get('bukken')  
        print("bukken_id data:", bukken_id)
        bukkens = 物件.objects.all()
        months = MonthSelect.objects.all() 
        selected_bukken = request.GET.get('bukken', None)
        
        formset = テナントInputFormSet(queryset=テナント.objects.all())
        return render(request, self.template_name, {
            'formset': formset, 
            'bukken_id': bukken_id, 
            'bukkens':bukkens, 
            'months':months, 
            'selected_bukken': selected_bukken
            })

    def post(self, request, *args, **kwargs):
        print("kwargs print", kwargs)
        if kwargs:
            bukken_id = kwargs.get['pk']
            selected_bukken = bukken_id
            print("request data pk", bukken_id)
        else:
            bukken_id = request.POST.get('bukken') 
            selected_bukken = request.POST.get('bukken', None)
        print("request data", request.POST)  # Print POST data for debugging

        bukkens = 物件.objects.all()
        months = MonthSelect.objects.all() 

        if not bukken_id:
            bukken_id = request.POST.get('form-0-物件ID')
            selected_bukken = bukken_id
            print("bukken_id print", bukken_id)
        elif not request.POST.get('form-0-物件ID'):
            formset = テナントInputFormSet(queryset=テナント.objects.none())
            return render(request, self.template_name, {'formset': formset})
        
        cleaned_post_data = request.POST.copy()
        for key, value in cleaned_post_data.items():
            cleaned_post_data[key] = value.replace(',', '')
        
        # formset = テナントInputFormSet(request.POST, queryset=物件.objects.all())
        formset = テナントInputFormSet(cleaned_post_data, queryset=テナント.objects.all())
        if formset.is_valid():
            formset.save()
            formset = テナントInputFormSet(queryset=テナント.objects.all())
            return render(request, self.template_name, {
            'formset': formset, 
            'bukken_id': bukken_id,
            'bukkens':bukkens, 
            'months':months, 
            'selected_bukken': selected_bukken
            })
        else:
            print("error",formset.errors)
        return render(request, self.template_name, {
            'formset': formset, 
            'bukken_id': bukken_id,
            'bukkens':bukkens, 
            'months':months, 
            'selected_bukken': selected_bukken
            })

###　敷金保証金を設定する
###  テンプレートは敷金保証金_input.html  ルートは: 敷金保証金-input
###  DBは敷金保証金, Form:  敷金保証金InputForm/敷金保証金InputFormSet
class 敷金保証金View(View):
    template_name = '敷金保証金_input.html'

    def get(self, request, *args, **kwargs):
        bukken_id = request.GET.get('bukken')  
        print("bukken_id data:", bukken_id)
        bukkens = 物件.objects.all()
        months = MonthSelect.objects.all() 
        selected_bukken = request.GET.get('bukken', None)
        
        if bukken_id:
            formset = 敷金保証金InputFormSet(
                queryset=敷金保証金.objects.filter(物件ID_id=bukken_id).order_by('契約番号')
                )

        else:
            formset = 敷金保証金InputFormSet(queryset=敷金保証金.objects.none())
        return render(request, self.template_name, {
            'formset': formset, 
            'bukken_id': bukken_id, 
            'bukkens':bukkens, 
            'months':months, 
            'selected_bukken': selected_bukken
            })

    def post(self, request, *args, **kwargs):
        print("request", request)
        bukken_id = request.POST.get('form-0-物件ID')
        if kwargs:
            bukken_id = kwargs.get['pk']
            selected_bukken = bukken_id
            print("request data pk", bukken_id)
        else:
            bukken_id = request.POST.get('bukken') 
            selected_bukken = request.POST.get('bukken', None)
        print("request data", request.POST)  # Print POST data for debugging

        if 'export_csv' in request.POST:
            bukken_id = request.POST.get('form-0-物件ID')
            print("export_csv request data pk", bukken_id)
            queryset=敷金保証金.objects.filter(物件ID_id=bukken_id)
            if queryset is not None:
                return self.export_to_csv(queryset)
            else:
                return HttpResponse("No data available to export.", content_type="text/plain")

        bukkens = 物件.objects.all()
        months = MonthSelect.objects.all() 

        if not bukken_id:
            bukken_id = request.POST.get('form-0-物件ID')
            selected_bukken = bukken_id
            print("bukken_id print", bukken_id)
        elif not request.POST.get('form-0-物件ID'):
            formset = 敷金保証金InputFormSet(queryset=敷金保証金.objects.none())
            return render(request, self.template_name, {'formset': formset})
        
        cleaned_post_data = request.POST.copy()
        for key, value in cleaned_post_data.items():
            cleaned_post_data[key] = value.replace(',', '')
        
        # formset = 敷金保証金InputFormSet(request.POST, queryset=敷金保証金.objects.filter(物件ID_id=bukken_id))
        formset = 敷金保証金InputFormSet(cleaned_post_data, queryset=敷金保証金.objects.filter(物件ID_id=bukken_id))
        if formset.is_valid():
            formset.save()
            formset = 敷金保証金InputFormSet(queryset=敷金保証金.objects.filter(物件ID_id=bukken_id))
            return render(request, self.template_name, {
            'formset': formset, 
            'bukken_id': bukken_id,
            'bukkens':bukkens, 
            'months':months, 
            'selected_bukken': selected_bukken
            })
        else:
            print("error",formset.errors)
        return render(request, self.template_name, {
            'formset': formset, 
            'bukken_id': bukken_id,
            'bukkens':bukkens, 
            'months':months, 
            'selected_bukken': selected_bukken
            })
    
    def export_to_csv(self, queryset):
        response = HttpResponse(
            content_type="text/csv",
            headers={"Content-Disposition": 'attachment; filename="deposit_list.csv"'},
            charset='utf_8_sig'
        )

        writer = csv.writer(response, delimiter=',')

        writer.writerow(['契約番号', '物件ID', 'テナントID', '契約区画','定借区分', '種類', 
                         '前月末残高', '当月増額', '当月減少', '今月末残高','移動予定日', '保証会社コード', 
                         '備考', 
                         ])

        for obj in queryset:
            writer.writerow([
                obj.契約番号.契約ID,  # Format the date as a string
                obj.物件ID.物件名,  # Assuming 物件ID is a ForeignKey
                obj.テナントID.テナント短縮名,  # Assuming 物件ID is a ForeignKey
                obj.契約区画 if obj.契約区画 is not None else '',
                obj.定借区分 if obj.定借区分 is not None else '',
                obj.種類 if obj.種類 is not None else '',
                obj.前月末残高 if obj.前月末残高 is not None else '',
                obj.当月増額 if obj.当月増額 is not None else '',
                obj.当月減少 if obj.当月減少 is not None else '',
                obj.今月末残高 if obj.今月末残高 is not None else '',
                obj.移動予定日.strftime('%Y-%m-%d') if obj.移動予定日 else '',
                obj.保証会社コード.保証会社名 if obj.保証会社コード.保証会社名 is not None else '',
                obj.備考 if obj.備考 is not None else '',
            ])
        
        return response

###　管理項目設定を設定する
###  テンプレートは管理項目_input.html  ルートは管理項目-input
###  DBは管理項目, Form:  管理項目InputForm/管理項目InputFormSet
class 管理項目View(View):
    template_name = '管理項目_input.html'

    def get(self, request, *args, **kwargs):
        bukken_id = request.GET.get('bukken')  
        print("bukken_id data:", bukken_id)
        bukkens = 物件.objects.all()
        months = MonthSelect.objects.all() 
        selected_bukken = request.GET.get('bukken', None)
        
        formset = 管理項目InputFormSet(queryset=管理項目.objects.all())
        return render(request, self.template_name, {
            'formset': formset, 
            'bukken_id': bukken_id, 
            'bukkens':bukkens, 
            'months':months, 
            'selected_bukken': selected_bukken
            })

    def post(self, request, *args, **kwargs):
        print("kwargs print", kwargs)
        if kwargs:
            bukken_id = kwargs.get['pk']
            selected_bukken = bukken_id
            print("request data pk", bukken_id)
        else:
            bukken_id = request.POST.get('bukken') 
            selected_bukken = request.POST.get('bukken', None)
        print("request data", request.POST)  # Print POST data for debugging

        bukkens = 物件.objects.all()
        months = MonthSelect.objects.all() 

        if not bukken_id:
            bukken_id = request.POST.get('form-0-物件ID')
            selected_bukken = bukken_id
            print("bukken_id print", bukken_id)
        elif not request.POST.get('form-0-物件ID'):
            formset = 管理項目InputFormSet(queryset=管理項目.objects.none())
            return render(request, self.template_name, {'formset': formset})
        
        cleaned_post_data = request.POST.copy()
        for key, value in cleaned_post_data.items():
            cleaned_post_data[key] = value.replace(',', '')
        
        formset = 管理項目InputFormSet(cleaned_post_data, queryset=管理項目.objects.all())
        if formset.is_valid():
            formset.save()
            formset = 管理項目InputFormSet(queryset=管理項目.objects.all())
            return render(request, self.template_name, {
            'formset': formset, 
            'bukken_id': bukken_id,
            'bukkens':bukkens, 
            'months':months, 
            'selected_bukken': selected_bukken
            })
        else:
            print("error",formset.errors)
        return render(request, self.template_name, {
            'formset': formset, 
            'bukken_id': bukken_id,
            'bukkens':bukkens, 
            'months':months, 
            'selected_bukken': selected_bukken
            })

###　保証会社設定を設定する
###  テンプレートは保証会社_input.html  ルートは保証会社-input
###  DBは保証会社, Form:  保証会社InputForm/保証会社InputFormSet   
class 保証会社View(View):
    template_name = '保証会社_input.html'

    def get(self, request, *args, **kwargs):
        bukken_id = request.GET.get('bukken')  
        print("bukken_id data:", bukken_id)
        bukkens = 物件.objects.all()
        months = MonthSelect.objects.all() 
        selected_bukken = request.GET.get('bukken', None)
        
        formset = 保証会社InputFormSet(queryset=保証会社.objects.all())
        return render(request, self.template_name, {
            'formset': formset, 
            'bukken_id': bukken_id, 
            'bukkens':bukkens, 
            'months':months, 
            'selected_bukken': selected_bukken
            })

    def post(self, request, *args, **kwargs):
        print("kwargs print", kwargs)
        if kwargs:
            bukken_id = kwargs.get['pk']
            selected_bukken = bukken_id
            print("request data pk", bukken_id)
        else:
            bukken_id = request.POST.get('bukken') 
            selected_bukken = request.POST.get('bukken', None)
        print("request data", request.POST)  # Print POST data for debugging

        bukkens = 物件.objects.all()
        months = MonthSelect.objects.all() 

        if not bukken_id:
            bukken_id = request.POST.get('form-0-物件ID')
            selected_bukken = bukken_id
            print("bukken_id print", bukken_id)
        elif not request.POST.get('form-0-物件ID'):
            formset = 保証会社InputFormSet(queryset=保証会社.objects.none())
            return render(request, self.template_name, {'formset': formset})
        
        cleaned_post_data = request.POST.copy()
        for key, value in cleaned_post_data.items():
            cleaned_post_data[key] = value.replace(',', '')
        
        formset = 保証会社InputFormSet(cleaned_post_data, queryset=保証会社.objects.all())
        if formset.is_valid():
            formset.save()
            formset = 保証会社InputFormSet(queryset=保証会社.objects.all())
            return render(request, self.template_name, {
            'formset': formset, 
            'bukken_id': bukken_id,
            'bukkens':bukkens, 
            'months':months, 
            'selected_bukken': selected_bukken
            })
        else:
            print("error",formset.errors)
        return render(request, self.template_name, {
            'formset': formset, 
            'bukken_id': bukken_id,
            'bukkens':bukkens, 
            'months':months, 
            'selected_bukken': selected_bukken
            })

###　支払先設定を設定する
###  テンプレートは支払先_input.html  ルートは支払先-input
###  DBは支払先, Form:  支払先InputForm/支払先InputFormSet 
class 支払先View(View):
    template_name = '支払先_input.html'

    def get(self, request, *args, **kwargs):
        bukken_id = request.GET.get('bukken')  
        print("bukken_id data:", bukken_id)
        bukkens = 物件.objects.all()
        months = MonthSelect.objects.all() 
        selected_bukken = request.GET.get('bukken', None)
        
        formset = 支払先InputFormSet(queryset=支払先.objects.all())
        return render(request, self.template_name, {
            'formset': formset, 
            'bukken_id': bukken_id, 
            'bukkens':bukkens, 
            'months':months, 
            'selected_bukken': selected_bukken
            })

    def post(self, request, *args, **kwargs):
        print("kwargs print", kwargs)
        if kwargs:
            bukken_id = kwargs.get['pk']
            selected_bukken = bukken_id
            print("request data pk", bukken_id)
        else:
            bukken_id = request.POST.get('bukken') 
            selected_bukken = request.POST.get('bukken', None)
        print("request data", request.POST)  # Print POST data for debugging

        bukkens = 物件.objects.all()
        months = MonthSelect.objects.all() 

        if not bukken_id:
            bukken_id = request.POST.get('form-0-物件ID')
            selected_bukken = bukken_id
            print("bukken_id print", bukken_id)
        elif not request.POST.get('form-0-物件ID'):
            formset = 支払先InputFormSet(queryset=支払先.objects.none())
            return render(request, self.template_name, {'formset': formset})
        
        cleaned_post_data = request.POST.copy()
        for key, value in cleaned_post_data.items():
            cleaned_post_data[key] = value.replace(',', '')
        
        formset = 支払先InputFormSet(cleaned_post_data, queryset=支払先.objects.all())
        if formset.is_valid():
            formset.save()
            formset = 支払先InputFormSet(queryset=支払先.objects.all())
            return render(request, self.template_name, {
            'formset': formset, 
            'bukken_id': bukken_id,
            'bukkens':bukkens, 
            'months':months, 
            'selected_bukken': selected_bukken
            })
        else:
            print("error",formset.errors)
        return render(request, self.template_name, {
            'formset': formset, 
            'bukken_id': bukken_id,
            'bukkens':bukkens, 
            'months':months, 
            'selected_bukken': selected_bukken
            })

def backup_database(request):
    try:
        call_command('backup_db')  # Replace 'backup_db' with the name of your command
        return HttpResponse("Backup created successfully.")
    except Exception as e:
        return HttpResponse(f"Error creating backup: {e}", status=500)

###　BM入力を設定する（物件ソート）
###  テンプレートはBMinput_field.html  ルートはbminput_field_view
###  DBはBMInputField, Form:  BMInputFieldForm/BMInputFieldFormSet
class BMInputFieldView(View):
    template_name = 'BMinput_field.html'

    def get(self, request, *args, **kwargs):
        bukken_id = request.GET.get('bukken')  
        print("bukken_id data:", bukken_id)
        bukkens = 物件.objects.all()
        months = MonthSelect.objects.all() 
        selected_bukken = request.GET.get('bukken', None)
        
        if bukken_id:
            formset = BMInputFieldFormSet(
                queryset=BMInputField.objects.filter(物件ID_id=bukken_id).order_by('BM項目__BM項目CD')
                )
        else:
            formset = BMInputFieldFormSet(queryset=BMInputField.objects.none())
        return render(request, self.template_name, {
            'formset': formset, 
            'bukken_id': bukken_id, 
            'bukkens':bukkens, 
            'months':months, 
            'selected_bukken': selected_bukken
            })

    def post(self, request, *args, **kwargs):
        print("kwargs print", kwargs)
        if kwargs:
            bukken_id = kwargs.get['pk']
            selected_bukken = bukken_id
            print("request data pk", bukken_id)
        else:
            bukken_id = request.POST.get('bukken') 
            selected_bukken = request.POST.get('bukken', None)
        print("request data", request.POST)  # Print POST data for debugging

        bukkens = 物件.objects.all()
        months = MonthSelect.objects.all() 

        if not bukken_id:
            bukken_id = request.POST.get('form-0-物件ID')
            selected_bukken = bukken_id
            print("bukken_id print", bukken_id)
        elif not request.POST.get('form-0-物件ID'):
            formset = BMInputFieldFormSet(queryset=BMInputField.objects.none())
            return render(request, self.template_name, {'formset': formset})
        
        formset = BMInputFieldFormSet(request.POST, queryset=BMInputField.objects.filter(物件ID_id=bukken_id))
        if formset.is_valid():
            formset.save()
            formset = BMInputFieldFormSet(queryset=BMInputField.objects.filter(物件ID_id=bukken_id))
            return render(request, self.template_name, {
            'formset': formset, 
            'bukken_id': bukken_id,
            'bukkens':bukkens, 
            'months':months, 
            'selected_bukken': selected_bukken
            })
        else:
            print("error",formset.errors)
        return render(request, self.template_name, {
            'formset': formset, 
            'bukken_id': bukken_id,
            'bukkens':bukkens, 
            'months':months, 
            'selected_bukken': selected_bukken
            })

###　BM項目設定を設定する（ソートはなし。ただ項目を設定するのみ。）
###  テンプレートはBM_item_input.html  ルートはbm_item_field_view
###  DBはBMItems, Form:  BMItemForm/BMItemFormSet
class BMItemView(View):
    template_name = 'BM_item_input.html'

   
    def get(self, request, *args, **kwargs):
        bukken_id = request.GET.get('bukken')  
        print("bukken_id data:", bukken_id)
        bukkens = 物件.objects.all()
        months = MonthSelect.objects.all() 
        selected_bukken = request.GET.get('bukken', None)
        
        formset = BMItemFormSet(queryset=BMItems.objects.all())
        return render(request, self.template_name, {
            'formset': formset, 
            'bukken_id': bukken_id, 
            'bukkens':bukkens, 
            'months':months, 
            'selected_bukken': selected_bukken
            })

    def post(self, request, *args, **kwargs):
        print("kwargs print", kwargs)
        if kwargs:
            bukken_id = kwargs.get['pk']
            selected_bukken = bukken_id
            print("request data pk", bukken_id)
        else:
            bukken_id = request.POST.get('bukken') 
            selected_bukken = request.POST.get('bukken', None)
        print("request data", request.POST)  # Print POST data for debugging

        bukkens = 物件.objects.all()
        months = MonthSelect.objects.all() 

        if not bukken_id:
            bukken_id = request.POST.get('form-0-物件ID')
            selected_bukken = bukken_id
            print("bukken_id print", bukken_id)
        elif not request.POST.get('form-0-物件ID'):
            formset = BMItemFormSet(queryset=BMItems.objects.none())
            return render(request, self.template_name, {'formset': formset})
        
        cleaned_post_data = request.POST.copy()
        for key, value in cleaned_post_data.items():
            cleaned_post_data[key] = value.replace(',', '')
        
        formset = BMItemFormSet(cleaned_post_data, queryset=BMItems.objects.all())
        if formset.is_valid():
            formset.save()
            formset = BMItemFormSet(queryset=BMItems.objects.all())
            return render(request, self.template_name, {
            'formset': formset, 
            'bukken_id': bukken_id,
            'bukkens':bukkens, 
            'months':months, 
            'selected_bukken': selected_bukken
            })
        else:
            print("error",formset.errors)
        return render(request, self.template_name, {
            'formset': formset, 
            'bukken_id': bukken_id,
            'bukkens':bukkens, 
            'months':months, 
            'selected_bukken': selected_bukken
            })

###　BM報告を設定する（物件及び年月でソート）
###  テンプレートはBM_input_view.html  ルートはbm_view
###  DBはBM入力フォーム, Form:  BMForm/BMFormSet
class BMView(View):
    template_name = 'BM_input_view.html'

    def get_queryset(self):
        queryset = BM入力フォーム.objects.all()  # Use your model's queryset
        
        # Get selected bukken and month from GET parameters
        selected_bukken = self.request.GET.get('bukken')
        selected_month = self.request.GET.get('months')
   
        # Filter by the selected bukken if provided
        if selected_bukken:
            queryset = queryset.filter(物件ID=selected_bukken)
        
        if selected_month:
            start_date = datetime.strptime(selected_month, '%B %d, %Y')
            start_of_month = start_date.strftime('%Y-%m-01')
            end_of_month = (start_date.replace(day=28) + timedelta(days=4)).replace(day=1) - timedelta(days=1)
            
            queryset = queryset.filter(
                レポート日__gte=start_of_month,
                レポート日__lte=end_of_month
            )

            queryset = queryset.select_related('BM項目').order_by(
                'BM項目__BM項目CD'
            )

        return queryset if queryset.exists() else None
    
    def get(self, request, *args, **kwargs):
        print("now passing def get")
        queryset = self.get_queryset()
        if queryset is None:
            context = self.get_context_data()
            context['message'] = 'No data found. Would you like to create a new dataset?'
            context['show_create_button'] = True
            return render(request, self.template_name, context)
        
        formset = BMFormSet(queryset=self.get_queryset())
        context = self.get_context_data(formset=formset)
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        print("now passing def POST")
        selected_bukken = request.POST.get('bukken', None)
        selected_month = request.POST.get('months', None)

        if 'create_new_dataset' in request.POST:
            print("now passing  create_new_dataset")
            # Call the create_new_dataset method
            selected_bukken = request.POST.get('bukken', None)
            selected_month = request.POST.get('months', None)
            self.create_new_dataset(request, selected_bukken, selected_month)
            # After dataset creation, redirect to the input page
            url = reverse('solitonRE:bm_view')  # This gets the URL pattern for 'bm_view'
            query_params = f'?bukken={selected_bukken}&months={selected_month}'
            redirect_url = f'{url}{query_params}'
            return HttpResponseRedirect(redirect_url)

        if 'tax_calc' in request.POST:
            print("tax_calc PASSING!!")
            # Call the create_new_dataset method
            selected_bukken = request.POST.get('bukken', None)
            selected_month = request.POST.get('months', None)
            self.tax_calc_def(selected_bukken, selected_month)
            # After dataset creation, redirect to the input page
            url = reverse('solitonRE:bm_view')  # This gets the URL pattern for 'bm_view'
            query_params = f'?bukken={selected_bukken}&months={selected_month}'
            redirect_url = f'{url}{query_params}'
            return HttpResponseRedirect(redirect_url)
        
        print("this part of post is now passing through")
        cleaned_post_data = request.POST.copy()
        for key, value in cleaned_post_data.items():
            cleaned_post_data[key] = value.replace(',', '')
            
        formset = BMFormSet(cleaned_post_data, queryset=self.get_queryset())   
        
        if formset.is_valid():
            formset.save()
            selected_bukken = request.POST.get('bukken')
            selected_month = request.POST.get('months')
            query_params = f'?bukken={selected_bukken}&months={selected_month}'
            url = reverse('solitonRE:bm_view')
            redirect_url = f'{url}{query_params}'
            return HttpResponseRedirect(redirect_url)
        else:
            print("formerror", formset.errors)
            context = self.get_context_data(formset=formset)
            return render(request, self.template_name, context)

    def get_context_data(self, **kwargs):
        context = {}

        # Get the selected values from GET parameters
        selected_bukken = self.request.GET.get('bukken')
        selected_month = self.request.GET.get('months')

        context['bukkens'] = 物件.objects.all()  # Assuming 物件 is your model name
        context['months'] = MonthSelect.objects.all()  # Replace with your actual month model
        context['selected_bukken'] = selected_bukken  # Selected bukken value
        context['selected_month'] = selected_month  # Selected month value

        context.update(kwargs)  # Include formset in the context
        return context
    
    def create_new_dataset(self, request, selected_bukken, selected_month):
        bukken_instance = 物件.objects.get(id=selected_bukken)
        start_date = datetime.strptime(selected_month, '%B %d, %Y')
        # Get selected_info from InputField
        print("selected bukken create new data", selected_bukken[0])
        selected_info = BMInputField.objects.filter(物件ID_id=selected_bukken)
        print("selected info in create new dataset", selected_info)
        input_BM = [bm_input for bm_input in selected_info]
        print("///////////// INPUT BM ///////////////////", input_BM)
        
        if not selected_info:
            print("No selected_info found.")
            # Handle the case where no data is found
            return  # or raise an error

            # Create new dataset
        for item in input_BM:
            new_data = BM入力フォーム.objects.create(
                物件ID=bukken_instance,
                レポート日=start_date,  # Assuming this should be the start date of the selected month
                BM項目=item.BM項目,
                BM回数=item.BM回数,
                BM予定数=item.BM予定数,
            )

            new_data.save()


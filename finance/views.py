# Ficheiro: finance/views.py

from django.views.generic import ListView, UpdateView, View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import permission_required
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.db import transaction
from django.http import HttpResponse, JsonResponse
import json
import csv
from decimal import Decimal
from django.utils import timezone
from dateutil.relativedelta import relativedelta
from django.db.models import Sum

from .models import FinancialRecord, Installment, Sale
from .forms import FinancialRecordForm, MonthlyReportForm

class FinancialRecordListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = FinancialRecord
    template_name = 'finance/financial_record_list.html'
    context_object_name = 'records'
    queryset = FinancialRecord.objects.select_related('sale__customer').order_by('status', '-created_at')

    def test_func(self):
        return self.request.user.has_perm('finance.view_financialrecord')

class FinancialRecordUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = FinancialRecord
    form_class = FinancialRecordForm
    template_name = 'finance/financial_record_form.html'
    
    def test_func(self):
        return self.request.user.has_perm('finance.change_financialrecord')

    def get_success_url(self):
        return reverse_lazy('finance:record_list')

    def form_valid(self, form):
        with transaction.atomic():
            self.object = form.save() 
            if 'installments' in form.changed_data:
                self.object.installments_list.all().delete()
                num_installments = self.object.installments
                total_value = self.object.sale.total_value
                if num_installments > 0:
                    installment_value = round(total_value / Decimal(num_installments), 2)
                    for i in range(1, num_installments + 1):
                        due_date = (self.object.sale.sale_date or timezone.now().date()) + relativedelta(months=i)
                        Installment.objects.create(
                            financial_record=self.object, installment_number=i,
                            value=installment_value, due_date=due_date, status='PENDENTE'
                        )
                messages.success(self.request, "Número de parcelas alterado e novas parcelas geradas!")
            else:
                messages.success(self.request, "Registro financeiro atualizado com sucesso!")
        return redirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = f"Gerir Venda #{self.object.sale.pk}"
        context['installments'] = self.object.installments_list.order_by('installment_number')
        return context

class ManageInstallmentView(LoginRequiredMixin, View):
    def get(self, request, pk, *args, **kwargs):
        installment = get_object_or_404(Installment, pk=pk)
        data = { 'id': installment.pk, 'due_date': installment.due_date.strftime('%Y-%m-%d') if installment.due_date else '', 'paid_value': str(installment.paid_value) if installment.paid_value is not None else '', 'paid_at': installment.paid_at.strftime('%Y-%m-%d') if installment.paid_at else '', 'status': installment.status, }
        return JsonResponse(data)
        
    def post(self, request, pk, *args, **kwargs):
        try:
            installment = get_object_or_404(Installment, pk=pk)
            data = json.loads(request.body)
            installment.due_date = data.get('due_date') or installment.due_date
            paid_value = data.get('paid_value')
            installment.paid_value = Decimal(paid_value) if paid_value else None
            paid_at = data.get('paid_at')
            installment.paid_at = paid_at if paid_at else None
            installment.status = data.get('status', installment.status)
            installment.save()
            return JsonResponse({'status': 'success', 'message': 'Parcela atualizada!'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

@permission_required('finance.view_financialrecord', raise_exception=True)
def monthly_report_view(request):
    form = MonthlyReportForm(request.GET or None)
    context = {'form': form}

    if form.is_valid():
        year = int(form.cleaned_data['year'])
        month = int(form.cleaned_data['month'])
    else:
        today = timezone.now()
        year = today.year
        month = today.month
        form.initial = {'year': year, 'month': month}

    paid_records = FinancialRecord.objects.filter(
        status='PAGO', sale__sale_date__year=year, sale__sale_date__month=month
    ).select_related('sale__customer')

    if request.GET.get('export') == 'csv':
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="relatorio_{year}-{month}.csv"'
        writer = csv.writer(response)
        writer.writerow(['ID Venda', 'Cliente', 'Data', 'Valor (R$)'])
        for record in paid_records:
            writer.writerow([
                record.sale.pk, record.sale.customer.name,
                record.sale.sale_date.strftime('%d/%m/%Y'),
                f"{record.sale.total_value:.2f}".replace('.', ',')
            ])
        return response

    total_revenue = paid_records.aggregate(total=Sum('sale__total_value'))['total'] or Decimal('0.00')
    num_sales = paid_records.count()
    ticket_medio = total_revenue / num_sales if num_sales > 0 else Decimal('0.00')

    context.update({
        'selected_year': year, 'selected_month': month, 'records': paid_records,
        'total_revenue': total_revenue, 'ticket_medio': ticket_medio,
    })

    return render(request, 'finance/monthly_report.html', context)
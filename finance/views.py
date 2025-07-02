# Ficheiro: finance/views.py

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, UpdateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.db import transaction
from decimal import Decimal
from django.utils import timezone
from dateutil.relativedelta import relativedelta
import json

from .models import FinancialRecord, Installment
from .forms import FinancialRecordForm

# A ListView continua igual
class FinancialRecordListView(LoginRequiredMixin, ListView):
    model = FinancialRecord
    template_name = 'finance/financial_record_list.html'
    context_object_name = 'records'
    queryset = FinancialRecord.objects.select_related('sale__customer').order_by('status', '-created_at')

# A UpdateView agora fica MAIS SIMPLES
class FinancialRecordUpdateView(LoginRequiredMixin, UpdateView):
    model = FinancialRecord
    form_class = FinancialRecordForm
    template_name = 'finance/financial_record_form.html'
    
    def get_success_url(self):
        return reverse_lazy('finance:record_update', kwargs={'pk': self.object.pk})

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
        
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = f"Gerir Venda #{self.object.sale.pk}"
        context['installments'] = self.object.installments_list.order_by('installment_number')
        return context

# ==========================================================
# ========= NOVA VIEW PARA GERENCIAR O MODAL (API) =========
# ==========================================================
class ManageInstallmentView(LoginRequiredMixin, View):

    def get(self, request, pk, *args, **kwargs):
        # Esta parte busca os dados de uma parcela e os devolve como JSON
        installment = get_object_or_404(Installment, pk=pk)
        data = {
            'id': installment.pk,
            'due_date': installment.due_date.strftime('%Y-%m-%d') if installment.due_date else '',
            'paid_value': str(installment.paid_value) if installment.paid_value is not None else '',
            'paid_at': installment.paid_at.strftime('%Y-%m-%d') if installment.paid_at else '',
            'status': installment.status,
        }
        return JsonResponse(data)

    def post(self, request, pk, *args, **kwargs):
        # Esta parte recebe os dados do modal e os salva
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
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import FinancialTransaction
from django.utils.crypto import get_random_string
from decimal import Decimal, InvalidOperation
import logging

logger = logging.getLogger(__name__)

@login_required
def transaction_list(request):
    transactions = FinancialTransaction.objects.all().order_by('-date')
    return render(request, 'transactions/list.html', {'transactions': transactions})

@login_required
def transaction_add(request):
    if request.method == 'POST':
        # Log the POST data for debugging
        logger.info(f"POST data: {request.POST}")
        
        # Generate a unique reference number
        reference_number = f"TRX-{get_random_string(8).upper()}"
        
        try:
            # Get form data
            transaction_type = request.POST.get('type')
            amount_str = request.POST.get('amount')
            date = request.POST.get('date')
            description = request.POST.get('description')
            payment_method = request.POST.get('payment_method')
            
            # Validate amount
            try:
                amount = Decimal(amount_str)
                if amount <= 0:
                    raise ValueError("Amount must be greater than 0")
            except (InvalidOperation, ValueError) as e:
                raise ValueError(f"Invalid amount: {str(e)}")
            
            # Validate transaction type
            if transaction_type not in dict(FinancialTransaction.TRANSACTION_TYPES):
                raise ValueError("Invalid transaction type")
            
            # Validate payment method
            if payment_method not in dict(FinancialTransaction.PAYMENT_METHOD_CHOICES):
                raise ValueError("Invalid payment method")
            
            logger.info(f"Creating transaction with: type={transaction_type}, amount={amount}, "
                       f"date={date}, payment_method={payment_method}")
            
            transaction = FinancialTransaction.objects.create(
                transaction_type=transaction_type,
                amount=amount,
                date=date,
                description=description,
                payment_method=payment_method,
                reference_number=reference_number
            )
            messages.success(request, 'Transaction added successfully.')
            return redirect('transactions:transaction_list')
        except Exception as e:
            logger.error(f"Error creating transaction: {str(e)}")
            messages.error(request, f'Error creating transaction: {str(e)}')
            # Return the form with the submitted data for correction
            return render(request, 'transactions/form.html', {
                'action': 'Add',
                'error': str(e),
                'transaction': {
                    'transaction_type': transaction_type,
                    'amount': amount_str,
                    'date': date,
                    'description': description,
                    'payment_method': payment_method
                }
            })
    
    return render(request, 'transactions/form.html', {'action': 'Add'})

@login_required
def transaction_edit(request, pk):
    transaction = get_object_or_404(FinancialTransaction, pk=pk)
    
    if request.method == 'POST':
        try:
            # Get form data
            transaction_type = request.POST.get('type')
            amount_str = request.POST.get('amount')
            date = request.POST.get('date')
            description = request.POST.get('description')
            payment_method = request.POST.get('payment_method')
            
            # Validate amount
            try:
                amount = Decimal(amount_str)
                if amount <= 0:
                    raise ValueError("Amount must be greater than 0")
            except (InvalidOperation, ValueError) as e:
                raise ValueError(f"Invalid amount: {str(e)}")
            
            # Validate transaction type
            if transaction_type not in dict(FinancialTransaction.TRANSACTION_TYPES):
                raise ValueError("Invalid transaction type")
            
            # Validate payment method
            if payment_method not in dict(FinancialTransaction.PAYMENT_METHOD_CHOICES):
                raise ValueError("Invalid payment method")
            
            transaction.transaction_type = transaction_type
            transaction.amount = amount
            transaction.date = date
            transaction.description = description
            transaction.payment_method = payment_method
            transaction.save()
            
            messages.success(request, 'Transaction updated successfully.')
            return redirect('transactions:transaction_list')
        except Exception as e:
            messages.error(request, f'Error updating transaction: {str(e)}')
            return render(request, 'transactions/form.html', {
                'action': 'Edit',
                'transaction': transaction,
                'error': str(e)
            })
    
    return render(request, 'transactions/form.html', {
        'action': 'Edit',
        'transaction': transaction
    })

@login_required
def transaction_delete(request, pk):
    transaction = get_object_or_404(FinancialTransaction, pk=pk)
    
    if request.method == 'POST':
        try:
            transaction.delete()
            messages.success(request, 'Transaction deleted successfully.')
            return redirect('transactions:transaction_list')
        except Exception as e:
            messages.error(request, f'Error deleting transaction: {str(e)}')
    
    return render(request, 'transactions/delete.html', {'transaction': transaction})

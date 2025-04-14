import React, { useEffect, useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import {
  fetchTransactions,
  fetchProjects,
  fetchExpenseCategories,
  selectTransactions,
  selectProjects,
  selectExpenseCategories,
  selectIsLoading,
  selectError,
} from '../../store/slices/transactionSlice';
import {
  PlusIcon,
  FunnelIcon,
  DocumentDownloadIcon,
  CurrencyRupeeIcon,
} from '@heroicons/react/24/outline';
import TransactionForm from './TransactionForm';
import TransactionFilters from './TransactionFilters';

const Transactions = () => {
  const dispatch = useDispatch();
  const transactions = useSelector(selectTransactions);
  const projects = useSelector(selectProjects);
  const expenseCategories = useSelector(selectExpenseCategories);
  const isLoading = useSelector(selectIsLoading);
  const error = useSelector(selectError);

  const [isFormOpen, setIsFormOpen] = useState(false);
  const [isFiltersOpen, setIsFiltersOpen] = useState(false);
  const [selectedTransaction, setSelectedTransaction] = useState(null);
  const [filters, setFilters] = useState({
    startDate: '',
    endDate: '',
    type: '',
    project: '',
    category: '',
    minAmount: '',
    maxAmount: '',
  });

  useEffect(() => {
    dispatch(fetchTransactions(filters));
    dispatch(fetchProjects());
    dispatch(fetchExpenseCategories());
  }, [dispatch, filters]);

  const handleFilterChange = (newFilters) => {
    setFilters(newFilters);
  };

  const calculateTotals = () => {
    return transactions.reduce(
      (acc, transaction) => {
        if (transaction.transaction_type === 'income') {
          acc.income += transaction.amount;
        } else if (transaction.transaction_type === 'expense') {
          acc.expense += transaction.amount;
        }
        return acc;
      },
      { income: 0, expense: 0 }
    );
  };

  const { income, expense } = calculateTotals();

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-full">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-primary-600"></div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="sm:flex sm:items-center sm:justify-between">
        <h1 className="text-2xl font-semibold text-gray-900">Transactions</h1>
        <div className="mt-4 sm:mt-0 flex space-x-3">
          <button
            onClick={() => setIsFiltersOpen(true)}
            className="btn-secondary flex items-center"
          >
            <FunnelIcon className="h-5 w-5 mr-2" />
            Filters
          </button>
          <button
            onClick={() => setIsFormOpen(true)}
            className="btn-primary flex items-center"
          >
            <PlusIcon className="h-5 w-5 mr-2" />
            New Transaction
          </button>
        </div>
      </div>

      {error && (
        <div className="rounded-md bg-red-50 p-4">
          <div className="flex">
            <div className="ml-3">
              <h3 className="text-sm font-medium text-red-800">{error}</h3>
            </div>
          </div>
        </div>
      )}

      {/* Summary Cards */}
      <div className="grid grid-cols-1 gap-5 sm:grid-cols-3">
        <div className="bg-white overflow-hidden shadow rounded-lg">
          <div className="p-5">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <CurrencyRupeeIcon className="h-6 w-6 text-green-500" />
              </div>
              <div className="ml-5 w-0 flex-1">
                <dl>
                  <dt className="text-sm font-medium text-gray-500 truncate">
                    Total Income
                  </dt>
                  <dd className="text-lg font-semibold text-green-600">
                    PKR {income.toLocaleString()}
                  </dd>
                </dl>
              </div>
            </div>
          </div>
        </div>

        <div className="bg-white overflow-hidden shadow rounded-lg">
          <div className="p-5">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <CurrencyRupeeIcon className="h-6 w-6 text-red-500" />
              </div>
              <div className="ml-5 w-0 flex-1">
                <dl>
                  <dt className="text-sm font-medium text-gray-500 truncate">
                    Total Expenses
                  </dt>
                  <dd className="text-lg font-semibold text-red-600">
                    PKR {expense.toLocaleString()}
                  </dd>
                </dl>
              </div>
            </div>
          </div>
        </div>

        <div className="bg-white overflow-hidden shadow rounded-lg">
          <div className="p-5">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <CurrencyRupeeIcon className="h-6 w-6 text-blue-500" />
              </div>
              <div className="ml-5 w-0 flex-1">
                <dl>
                  <dt className="text-sm font-medium text-gray-500 truncate">
                    Net Balance
                  </dt>
                  <dd className={`text-lg font-semibold ${
                    income - expense >= 0 ? 'text-blue-600' : 'text-red-600'
                  }`}>
                    PKR {(income - expense).toLocaleString()}
                  </dd>
                </dl>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Transactions Table */}
      <div className="bg-white shadow-sm rounded-lg">
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Date
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Description
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Type
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Category
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Project
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Amount
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Payment Method
                </th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {transactions.map((transaction) => (
                <tr
                  key={transaction.id}
                  className="hover:bg-gray-50 cursor-pointer"
                  onClick={() => {
                    setSelectedTransaction(transaction);
                    setIsFormOpen(true);
                  }}
                >
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {new Date(transaction.date).toLocaleDateString()}
                  </td>
                  <td className="px-6 py-4 text-sm text-gray-900">
                    {transaction.description}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span
                      className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                        transaction.transaction_type === 'income'
                          ? 'bg-green-100 text-green-800'
                          : 'bg-red-100 text-red-800'
                      }`}
                    >
                      {transaction.transaction_type.charAt(0).toUpperCase() +
                        transaction.transaction_type.slice(1)}
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {transaction.category?.name || '-'}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {transaction.project?.name || '-'}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                    <span
                      className={
                        transaction.transaction_type === 'income'
                          ? 'text-green-600'
                          : 'text-red-600'
                      }
                    >
                      PKR {transaction.amount.toLocaleString()}
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {transaction.payment_method}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Transaction Form Modal */}
      {isFormOpen && (
        <div className="fixed inset-0 z-50 overflow-y-auto">
          <div className="flex items-center justify-center min-h-screen px-4">
            <div className="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity"></div>
            <div className="relative bg-white rounded-lg max-w-2xl w-full">
              <TransactionForm
                transaction={selectedTransaction}
                projects={projects}
                categories={expenseCategories}
                onClose={() => {
                  setIsFormOpen(false);
                  setSelectedTransaction(null);
                }}
              />
            </div>
          </div>
        </div>
      )}

      {/* Filters Modal */}
      {isFiltersOpen && (
        <div className="fixed inset-0 z-50 overflow-y-auto">
          <div className="flex items-center justify-center min-h-screen px-4">
            <div className="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity"></div>
            <div className="relative bg-white rounded-lg max-w-lg w-full">
              <TransactionFilters
                filters={filters}
                projects={projects}
                categories={expenseCategories}
                onApply={handleFilterChange}
                onClose={() => setIsFiltersOpen(false)}
              />
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Transactions;

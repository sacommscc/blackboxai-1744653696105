import React from 'react';
import { useDispatch } from 'react-redux';
import { Formik, Form, Field } from 'formik';
import * as Yup from 'yup';
import { XMarkIcon } from '@heroicons/react/24/outline';
import { addTransaction, updateTransaction } from '../../store/slices/transactionSlice';

const transactionSchema = Yup.object().shape({
  transaction_type: Yup.string()
    .oneOf(['income', 'expense', 'transfer'], 'Invalid transaction type')
    .required('Required'),
  amount: Yup.number()
    .min(0.01, 'Amount must be greater than 0')
    .required('Required'),
  date: Yup.date()
    .max(new Date(), 'Cannot record future transactions')
    .required('Required'),
  description: Yup.string()
    .min(5, 'Too Short!')
    .required('Required'),
  payment_method: Yup.string()
    .oneOf(['cash', 'easypaisa', 'jazzcash', 'bank'], 'Invalid payment method')
    .required('Required'),
  transaction_id: Yup.string()
    .when('payment_method', {
      is: (method) => method !== 'cash',
      then: Yup.string().required('Transaction ID required for non-cash payments'),
    }),
  project: Yup.string(),
  category: Yup.string(),
  reference_number: Yup.string()
    .required('Required'),
});

const TransactionForm = ({ transaction, projects, categories, onClose }) => {
  const dispatch = useDispatch();

  const initialValues = {
    transaction_type: transaction?.transaction_type || 'expense',
    amount: transaction?.amount || '',
    date: transaction?.date || new Date().toISOString().split('T')[0],
    description: transaction?.description || '',
    payment_method: transaction?.payment_method || 'cash',
    transaction_id: transaction?.transaction_id || '',
    project: transaction?.project?.id || '',
    category: transaction?.category?.id || '',
    reference_number: transaction?.reference_number || '',
  };

  const handleSubmit = async (values, { setSubmitting }) => {
    try {
      if (transaction) {
        await dispatch(updateTransaction({ id: transaction.id, data: values })).unwrap();
      } else {
        await dispatch(addTransaction(values)).unwrap();
      }
      onClose();
    } catch (error) {
      console.error('Error:', error);
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="p-6">
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-xl font-semibold text-gray-900">
          {transaction ? 'Edit Transaction' : 'New Transaction'}
        </h2>
        <button
          onClick={onClose}
          className="text-gray-400 hover:text-gray-500"
        >
          <XMarkIcon className="h-6 w-6" />
        </button>
      </div>

      <Formik
        initialValues={initialValues}
        validationSchema={transactionSchema}
        onSubmit={handleSubmit}
      >
        {({ isSubmitting, touched, errors, values }) => (
          <Form className="space-y-6">
            <div className="grid grid-cols-1 gap-6 sm:grid-cols-2">
              <div>
                <label htmlFor="transaction_type" className="form-label">
                  Transaction Type
                </label>
                <Field
                  as="select"
                  name="transaction_type"
                  id="transaction_type"
                  className="input-field"
                >
                  <option value="expense">Expense</option>
                  <option value="income">Income</option>
                  <option value="transfer">Transfer</option>
                </Field>
                {touched.transaction_type && errors.transaction_type && (
                  <p className="mt-2 text-sm text-red-600">{errors.transaction_type}</p>
                )}
              </div>

              <div>
                <label htmlFor="amount" className="form-label">
                  Amount (PKR)
                </label>
                <Field
                  type="number"
                  name="amount"
                  id="amount"
                  className="input-field"
                  min="0.01"
                  step="0.01"
                />
                {touched.amount && errors.amount && (
                  <p className="mt-2 text-sm text-red-600">{errors.amount}</p>
                )}
              </div>

              <div>
                <label htmlFor="date" className="form-label">
                  Date
                </label>
                <Field
                  type="date"
                  name="date"
                  id="date"
                  className="input-field"
                  max={new Date().toISOString().split('T')[0]}
                />
                {touched.date && errors.date && (
                  <p className="mt-2 text-sm text-red-600">{errors.date}</p>
                )}
              </div>

              <div>
                <label htmlFor="payment_method" className="form-label">
                  Payment Method
                </label>
                <Field
                  as="select"
                  name="payment_method"
                  id="payment_method"
                  className="input-field"
                >
                  <option value="cash">Cash</option>
                  <option value="easypaisa">Easypaisa</option>
                  <option value="jazzcash">JazzCash</option>
                  <option value="bank">Bank Transfer</option>
                </Field>
                {touched.payment_method && errors.payment_method && (
                  <p className="mt-2 text-sm text-red-600">{errors.payment_method}</p>
                )}
              </div>

              {values.payment_method !== 'cash' && (
                <div>
                  <label htmlFor="transaction_id" className="form-label">
                    Transaction ID
                  </label>
                  <Field
                    type="text"
                    name="transaction_id"
                    id="transaction_id"
                    className="input-field"
                  />
                  {touched.transaction_id && errors.transaction_id && (
                    <p className="mt-2 text-sm text-red-600">{errors.transaction_id}</p>
                  )}
                </div>
              )}

              <div>
                <label htmlFor="project" className="form-label">
                  Project
                </label>
                <Field
                  as="select"
                  name="project"
                  id="project"
                  className="input-field"
                >
                  <option value="">Select Project</option>
                  {projects.map((project) => (
                    <option key={project.id} value={project.id}>
                      {project.name}
                    </option>
                  ))}
                </Field>
                {touched.project && errors.project && (
                  <p className="mt-2 text-sm text-red-600">{errors.project}</p>
                )}
              </div>

              <div>
                <label htmlFor="category" className="form-label">
                  Category
                </label>
                <Field
                  as="select"
                  name="category"
                  id="category"
                  className="input-field"
                >
                  <option value="">Select Category</option>
                  {categories.map((category) => (
                    <option key={category.id} value={category.id}>
                      {category.name}
                    </option>
                  ))}
                </Field>
                {touched.category && errors.category && (
                  <p className="mt-2 text-sm text-red-600">{errors.category}</p>
                )}
              </div>

              <div>
                <label htmlFor="reference_number" className="form-label">
                  Reference Number
                </label>
                <Field
                  type="text"
                  name="reference_number"
                  id="reference_number"
                  className="input-field"
                />
                {touched.reference_number && errors.reference_number && (
                  <p className="mt-2 text-sm text-red-600">{errors.reference_number}</p>
                )}
              </div>
            </div>

            <div>
              <label htmlFor="description" className="form-label">
                Description
              </label>
              <Field
                as="textarea"
                name="description"
                id="description"
                rows={3}
                className="input-field"
              />
              {touched.description && errors.description && (
                <p className="mt-2 text-sm text-red-600">{errors.description}</p>
              )}
            </div>

            <div className="flex justify-end space-x-3">
              <button
                type="button"
                onClick={onClose}
                className="btn-secondary"
              >
                Cancel
              </button>
              <button
                type="submit"
                disabled={isSubmitting}
                className="btn-primary"
              >
                {isSubmitting ? 'Saving...' : transaction ? 'Update Transaction' : 'Add Transaction'}
              </button>
            </div>
          </Form>
        )}
      </Formik>
    </div>
  );
};

export default TransactionForm;

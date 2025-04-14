import React from 'react';
import { useDispatch } from 'react-redux';
import { Formik, Form, Field } from 'formik';
import * as Yup from 'yup';
import { XMarkIcon } from '@heroicons/react/24/outline';
import { addLabourer, updateLabourer } from '../../store/slices/labourSlice';

const labourSchema = Yup.object().shape({
  name: Yup.string()
    .min(2, 'Too Short!')
    .max(200, 'Too Long!')
    .required('Required'),
  cnic: Yup.string()
    .matches(/^\d{5}-\d{7}-\d{1}$/, 'CNIC must be in format XXXXX-XXXXXXX-X')
    .required('Required'),
  phone: Yup.string()
    .matches(/^[0-9+\-\s]+$/, 'Invalid phone number')
    .required('Required'),
  address: Yup.string()
    .required('Required'),
  labour_type: Yup.string()
    .required('Required'),
  daily_wage: Yup.number()
    .min(0, 'Must be greater than 0')
    .required('Required'),
  emergency_contact: Yup.string()
    .min(2, 'Too Short!')
    .max(100, 'Too Long!'),
  emergency_phone: Yup.string()
    .matches(/^[0-9+\-\s]+$/, 'Invalid phone number'),
  skills: Yup.array()
    .of(Yup.string())
    .min(1, 'Select at least one skill'),
});

const LabourForm = ({ labourer, labourTypes, onClose }) => {
  const dispatch = useDispatch();

  const initialValues = {
    name: labourer?.name || '',
    cnic: labourer?.cnic || '',
    phone: labourer?.phone || '',
    address: labourer?.address || '',
    labour_type: labourer?.labour_type.id || '',
    daily_wage: labourer?.daily_wage || '',
    emergency_contact: labourer?.emergency_contact || '',
    emergency_phone: labourer?.emergency_phone || '',
    skills: labourer?.skills.map(s => s.id) || [],
    is_active: labourer?.is_active ?? true,
  };

  const handleSubmit = async (values, { setSubmitting }) => {
    try {
      if (labourer) {
        await dispatch(updateLabourer({ id: labourer.id, data: values })).unwrap();
      } else {
        await dispatch(addLabourer(values)).unwrap();
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
          {labourer ? 'Edit Labourer' : 'Add New Labourer'}
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
        validationSchema={labourSchema}
        onSubmit={handleSubmit}
      >
        {({ isSubmitting, touched, errors, values }) => (
          <Form className="space-y-6">
            <div className="grid grid-cols-1 gap-6 sm:grid-cols-2">
              <div>
                <label htmlFor="name" className="form-label">
                  Full Name
                </label>
                <Field
                  type="text"
                  name="name"
                  id="name"
                  className="input-field"
                />
                {touched.name && errors.name && (
                  <p className="mt-2 text-sm text-red-600">{errors.name}</p>
                )}
              </div>

              <div>
                <label htmlFor="cnic" className="form-label">
                  CNIC (XXXXX-XXXXXXX-X)
                </label>
                <Field
                  type="text"
                  name="cnic"
                  id="cnic"
                  className="input-field"
                  placeholder="12345-1234567-1"
                />
                {touched.cnic && errors.cnic && (
                  <p className="mt-2 text-sm text-red-600">{errors.cnic}</p>
                )}
              </div>

              <div>
                <label htmlFor="phone" className="form-label">
                  Phone Number
                </label>
                <Field
                  type="text"
                  name="phone"
                  id="phone"
                  className="input-field"
                />
                {touched.phone && errors.phone && (
                  <p className="mt-2 text-sm text-red-600">{errors.phone}</p>
                )}
              </div>

              <div>
                <label htmlFor="labour_type" className="form-label">
                  Labour Type
                </label>
                <Field
                  as="select"
                  name="labour_type"
                  id="labour_type"
                  className="input-field"
                >
                  <option value="">Select a type</option>
                  {labourTypes.map((type) => (
                    <option key={type.id} value={type.id}>
                      {type.name}
                    </option>
                  ))}
                </Field>
                {touched.labour_type && errors.labour_type && (
                  <p className="mt-2 text-sm text-red-600">{errors.labour_type}</p>
                )}
              </div>

              <div>
                <label htmlFor="daily_wage" className="form-label">
                  Daily Wage (PKR)
                </label>
                <Field
                  type="number"
                  name="daily_wage"
                  id="daily_wage"
                  className="input-field"
                  min="0"
                  step="0.01"
                />
                {touched.daily_wage && errors.daily_wage && (
                  <p className="mt-2 text-sm text-red-600">{errors.daily_wage}</p>
                )}
              </div>

              <div>
                <label htmlFor="emergency_contact" className="form-label">
                  Emergency Contact Name
                </label>
                <Field
                  type="text"
                  name="emergency_contact"
                  id="emergency_contact"
                  className="input-field"
                />
                {touched.emergency_contact && errors.emergency_contact && (
                  <p className="mt-2 text-sm text-red-600">{errors.emergency_contact}</p>
                )}
              </div>

              <div>
                <label htmlFor="emergency_phone" className="form-label">
                  Emergency Contact Phone
                </label>
                <Field
                  type="text"
                  name="emergency_phone"
                  id="emergency_phone"
                  className="input-field"
                />
                {touched.emergency_phone && errors.emergency_phone && (
                  <p className="mt-2 text-sm text-red-600">{errors.emergency_phone}</p>
                )}
              </div>
            </div>

            <div>
              <label htmlFor="address" className="form-label">
                Address
              </label>
              <Field
                as="textarea"
                name="address"
                id="address"
                rows={3}
                className="input-field"
              />
              {touched.address && errors.address && (
                <p className="mt-2 text-sm text-red-600">{errors.address}</p>
              )}
            </div>

            <div>
              <div className="flex items-center">
                <Field
                  type="checkbox"
                  name="is_active"
                  id="is_active"
                  className="h-4 w-4 rounded border-gray-300 text-primary-600 focus:ring-primary-500"
                />
                <label htmlFor="is_active" className="ml-2 block text-sm text-gray-900">
                  Active Status
                </label>
              </div>
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
                {isSubmitting ? 'Saving...' : labourer ? 'Update Labourer' : 'Add Labourer'}
              </button>
            </div>
          </Form>
        )}
      </Formik>
    </div>
  );
};

export default LabourForm;

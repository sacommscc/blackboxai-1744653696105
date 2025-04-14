import React from 'react';
import { useDispatch } from 'react-redux';
import { Formik, Form, Field } from 'formik';
import * as Yup from 'yup';
import { XMarkIcon } from '@heroicons/react/24/outline';
import { addWorkLog } from '../../store/slices/labourSlice';

const workLogSchema = Yup.object().shape({
  work_date: Yup.date()
    .max(new Date(), 'Cannot log future work')
    .required('Required'),
  hours_worked: Yup.number()
    .min(0.5, 'Must work at least 30 minutes')
    .max(24, 'Cannot exceed 24 hours')
    .required('Required'),
  tasks_performed: Yup.array()
    .min(1, 'Select at least one task')
    .required('Required'),
  description: Yup.string()
    .min(10, 'Description too short')
    .required('Required'),
});

const WorkLogForm = ({ labourer, onClose }) => {
  const dispatch = useDispatch();

  const initialValues = {
    work_date: new Date().toISOString().split('T')[0],
    hours_worked: 8,
    tasks_performed: [],
    description: '',
  };

  const handleSubmit = async (values, { setSubmitting }) => {
    try {
      const workLogData = {
        ...values,
        labourer: labourer.id,
      };
      await dispatch(addWorkLog(workLogData)).unwrap();
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
        <div>
          <h2 className="text-xl font-semibold text-gray-900">
            Add Work Log
          </h2>
          <p className="mt-1 text-sm text-gray-500">
            Recording work for: {labourer.name}
          </p>
        </div>
        <button
          onClick={onClose}
          className="text-gray-400 hover:text-gray-500"
        >
          <XMarkIcon className="h-6 w-6" />
        </button>
      </div>

      <Formik
        initialValues={initialValues}
        validationSchema={workLogSchema}
        onSubmit={handleSubmit}
      >
        {({ isSubmitting, touched, errors, setFieldValue, values }) => (
          <Form className="space-y-6">
            <div className="grid grid-cols-1 gap-6 sm:grid-cols-2">
              <div>
                <label htmlFor="work_date" className="form-label">
                  Work Date
                </label>
                <Field
                  type="date"
                  name="work_date"
                  id="work_date"
                  className="input-field"
                  max={new Date().toISOString().split('T')[0]}
                />
                {touched.work_date && errors.work_date && (
                  <p className="mt-2 text-sm text-red-600">{errors.work_date}</p>
                )}
              </div>

              <div>
                <label htmlFor="hours_worked" className="form-label">
                  Hours Worked
                </label>
                <Field
                  type="number"
                  name="hours_worked"
                  id="hours_worked"
                  className="input-field"
                  min="0.5"
                  max="24"
                  step="0.5"
                />
                {touched.hours_worked && errors.hours_worked && (
                  <p className="mt-2 text-sm text-red-600">{errors.hours_worked}</p>
                )}
              </div>
            </div>

            <div>
              <label className="form-label">Tasks Performed</label>
              <div className="mt-2 grid grid-cols-2 gap-2">
                {labourer.skills.map((skill) => (
                  <label
                    key={skill.id}
                    className="inline-flex items-center"
                  >
                    <input
                      type="checkbox"
                      className="rounded border-gray-300 text-primary-600 shadow-sm focus:border-primary-500 focus:ring-primary-500"
                      checked={values.tasks_performed.includes(skill.id)}
                      onChange={(e) => {
                        const tasks = e.target.checked
                          ? [...values.tasks_performed, skill.id]
                          : values.tasks_performed.filter(id => id !== skill.id);
                        setFieldValue('tasks_performed', tasks);
                      }}
                    />
                    <span className="ml-2 text-sm text-gray-700">
                      {skill.name}
                    </span>
                  </label>
                ))}
              </div>
              {touched.tasks_performed && errors.tasks_performed && (
                <p className="mt-2 text-sm text-red-600">{errors.tasks_performed}</p>
              )}
            </div>

            <div>
              <label htmlFor="description" className="form-label">
                Work Description
              </label>
              <Field
                as="textarea"
                name="description"
                id="description"
                rows={4}
                className="input-field"
                placeholder="Describe the work performed..."
              />
              {touched.description && errors.description && (
                <p className="mt-2 text-sm text-red-600">{errors.description}</p>
              )}
            </div>

            <div className="mt-4 flex justify-end space-x-3">
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
                {isSubmitting ? 'Saving...' : 'Record Work Log'}
              </button>
            </div>

            {/* Daily Wage Information */}
            <div className="mt-6 bg-gray-50 p-4 rounded-md">
              <h3 className="text-sm font-medium text-gray-900">Wage Calculation</h3>
              <div className="mt-2 text-sm text-gray-500">
                <p>Daily Rate: PKR {labourer.daily_wage.toLocaleString()}</p>
                <p>Hours Worked: {values.hours_worked}</p>
                <p className="font-medium text-gray-900">
                  Estimated Pay: PKR {((labourer.daily_wage / 8) * values.hours_worked).toLocaleString()}
                </p>
                <p className="text-xs mt-1">
                  *Based on standard 8-hour workday
                </p>
              </div>
            </div>
          </Form>
        )}
      </Formik>
    </div>
  );
};

export default WorkLogForm;

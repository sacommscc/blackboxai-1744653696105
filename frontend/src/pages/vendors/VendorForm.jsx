import React, { useEffect, useState } from 'react';
import { useDispatch } from 'react-redux';
import { Formik, Form, Field } from 'formik';
import * as Yup from 'yup';
import { XMarkIcon } from '@heroicons/react/24/outline';
import { addVendor, updateVendor } from '../../store/slices/vendorSlice';

const vendorSchema = Yup.object().shape({
  name: Yup.string()
    .min(2, 'Too Short!')
    .max(200, 'Too Long!')
    .required('Required'),
  contact_person: Yup.string()
    .min(2, 'Too Short!')
    .max(100, 'Too Long!')
    .required('Required'),
  phone: Yup.string()
    .matches(/^[0-9+\-\s]+$/, 'Invalid phone number')
    .required('Required'),
  email: Yup.string()
    .email('Invalid email')
    .required('Required'),
  address: Yup.string()
    .required('Required'),
  material_types: Yup.array()
    .min(1, 'Select at least one material type')
    .required('Required'),
});

const materialTypes = [
  { id: 1, name: 'Cement' },
  { id: 2, name: 'Steel' },
  { id: 3, name: 'Bricks' },
  { id: 4, name: 'Sand' },
  { id: 5, name: 'Aggregate' },
  { id: 6, name: 'Wood' },
  { id: 7, name: 'Paint' },
  { id: 8, name: 'Glass' },
  { id: 9, name: 'Tiles' },
  { id: 10, name: 'Electrical' },
  { id: 11, name: 'Plumbing' },
];

const VendorForm = ({ vendor, onClose }) => {
  const dispatch = useDispatch();
  const [selectedMaterials, setSelectedMaterials] = useState(
    vendor ? vendor.material_types.map(t => t.id) : []
  );

  const initialValues = {
    name: vendor?.name || '',
    contact_person: vendor?.contact_person || '',
    phone: vendor?.phone || '',
    email: vendor?.email || '',
    address: vendor?.address || '',
    material_types: vendor?.material_types.map(t => t.id) || [],
  };

  const handleSubmit = async (values, { setSubmitting }) => {
    try {
      if (vendor) {
        await dispatch(updateVendor({ id: vendor.id, data: values })).unwrap();
      } else {
        await dispatch(addVendor(values)).unwrap();
      }
      onClose();
    } catch (error) {
      console.error('Error:', error);
    } finally {
      setSubmitting(false);
    }
  };

  const handleMaterialToggle = (materialId) => {
    setSelectedMaterials(prev => {
      if (prev.includes(materialId)) {
        return prev.filter(id => id !== materialId);
      }
      return [...prev, materialId];
    });
  };

  return (
    <div className="p-6">
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-xl font-semibold text-gray-900">
          {vendor ? 'Edit Vendor' : 'Add New Vendor'}
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
        validationSchema={vendorSchema}
        onSubmit={handleSubmit}
      >
        {({ isSubmitting, touched, errors, setFieldValue }) => (
          <Form className="space-y-6">
            <div>
              <label htmlFor="name" className="form-label">
                Vendor Name
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
              <label htmlFor="contact_person" className="form-label">
                Contact Person
              </label>
              <Field
                type="text"
                name="contact_person"
                id="contact_person"
                className="input-field"
              />
              {touched.contact_person && errors.contact_person && (
                <p className="mt-2 text-sm text-red-600">{errors.contact_person}</p>
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
              <label htmlFor="email" className="form-label">
                Email Address
              </label>
              <Field
                type="email"
                name="email"
                id="email"
                className="input-field"
              />
              {touched.email && errors.email && (
                <p className="mt-2 text-sm text-red-600">{errors.email}</p>
              )}
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
              <label className="form-label">Material Types</label>
              <div className="mt-2 grid grid-cols-2 gap-2">
                {materialTypes.map((material) => (
                  <label
                    key={material.id}
                    className="inline-flex items-center"
                  >
                    <input
                      type="checkbox"
                      className="rounded border-gray-300 text-primary-600 shadow-sm focus:border-primary-500 focus:ring-primary-500"
                      checked={selectedMaterials.includes(material.id)}
                      onChange={() => {
                        handleMaterialToggle(material.id);
                        setFieldValue('material_types', 
                          selectedMaterials.includes(material.id)
                            ? selectedMaterials.filter(id => id !== material.id)
                            : [...selectedMaterials, material.id]
                        );
                      }}
                    />
                    <span className="ml-2 text-sm text-gray-700">
                      {material.name}
                    </span>
                  </label>
                ))}
              </div>
              {touched.material_types && errors.material_types && (
                <p className="mt-2 text-sm text-red-600">{errors.material_types}</p>
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
                {isSubmitting ? 'Saving...' : vendor ? 'Update Vendor' : 'Add Vendor'}
              </button>
            </div>
          </Form>
        )}
      </Formik>
    </div>
  );
};

export default VendorForm;

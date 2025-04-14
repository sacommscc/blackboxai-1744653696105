import React, { useEffect, useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import {
  fetchLabourers,
  fetchLabourTypes,
  selectLabourers,
  selectLabourTypes,
  selectIsLoading,
  selectError,
} from '../../store/slices/labourSlice';
import { PlusIcon, PencilIcon, TrashIcon, ClockIcon } from '@heroicons/react/24/outline';
import LabourForm from './LabourForm';
import WorkLogForm from './WorkLogForm';

const LabourManagement = () => {
  const dispatch = useDispatch();
  const labourers = useSelector(selectLabourers);
  const labourTypes = useSelector(selectLabourTypes);
  const isLoading = useSelector(selectIsLoading);
  const error = useSelector(selectError);
  
  const [isLabourFormOpen, setIsLabourFormOpen] = useState(false);
  const [isWorkLogFormOpen, setIsWorkLogFormOpen] = useState(false);
  const [selectedLabourer, setSelectedLabourer] = useState(null);

  useEffect(() => {
    dispatch(fetchLabourers());
    dispatch(fetchLabourTypes());
  }, [dispatch]);

  const handleEdit = (labourer) => {
    setSelectedLabourer(labourer);
    setIsLabourFormOpen(true);
  };

  const handleAddWorkLog = (labourer) => {
    setSelectedLabourer(labourer);
    setIsWorkLogFormOpen(true);
  };

  const handleCloseLabourForm = () => {
    setSelectedLabourer(null);
    setIsLabourFormOpen(false);
  };

  const handleCloseWorkLogForm = () => {
    setSelectedLabourer(null);
    setIsWorkLogFormOpen(false);
  };

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
        <h1 className="text-2xl font-semibold text-gray-900">Labour Management</h1>
        <div className="mt-4 sm:mt-0">
          <button
            onClick={() => setIsLabourFormOpen(true)}
            className="btn-primary flex items-center"
          >
            <PlusIcon className="h-5 w-5 mr-2" />
            Add Labourer
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

      <div className="bg-white shadow-sm rounded-lg">
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Name
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  CNIC
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Labour Type
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Daily Wage (PKR)
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Status
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Actions
                </th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {labourers.map((labourer) => (
                <tr key={labourer.id} className="hover:bg-gray-50">
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="flex items-center">
                      <div>
                        <div className="text-sm font-medium text-gray-900">
                          {labourer.name}
                        </div>
                        <div className="text-sm text-gray-500">
                          {labourer.phone}
                        </div>
                      </div>
                    </div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {labourer.cnic}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                      {labourer.labour_type.name}
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {labourer.daily_wage.toLocaleString()}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span
                      className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                        labourer.is_active
                          ? 'bg-green-100 text-green-800'
                          : 'bg-red-100 text-red-800'
                      }`}
                    >
                      {labourer.is_active ? 'Active' : 'Inactive'}
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    <div className="flex space-x-2">
                      <button
                        onClick={() => handleAddWorkLog(labourer)}
                        className="text-primary-600 hover:text-primary-900"
                        title="Add Work Log"
                      >
                        <ClockIcon className="h-5 w-5" />
                      </button>
                      <button
                        onClick={() => handleEdit(labourer)}
                        className="text-primary-600 hover:text-primary-900"
                        title="Edit"
                      >
                        <PencilIcon className="h-5 w-5" />
                      </button>
                      <button
                        className="text-red-600 hover:text-red-900"
                        title="Delete"
                      >
                        <TrashIcon className="h-5 w-5" />
                      </button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Labour Form Modal */}
      {isLabourFormOpen && (
        <div className="fixed inset-0 z-50 overflow-y-auto">
          <div className="flex items-center justify-center min-h-screen px-4">
            <div className="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity"></div>
            <div className="relative bg-white rounded-lg max-w-2xl w-full">
              <LabourForm
                labourer={selectedLabourer}
                labourTypes={labourTypes}
                onClose={handleCloseLabourForm}
              />
            </div>
          </div>
        </div>
      )}

      {/* Work Log Form Modal */}
      {isWorkLogFormOpen && (
        <div className="fixed inset-0 z-50 overflow-y-auto">
          <div className="flex items-center justify-center min-h-screen px-4">
            <div className="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity"></div>
            <div className="relative bg-white rounded-lg max-w-2xl w-full">
              <WorkLogForm
                labourer={selectedLabourer}
                onClose={handleCloseWorkLogForm}
              />
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default LabourManagement;

import React from 'react';
import { Routes, Route } from 'react-router-dom';
import Layout from './components/layout/Layout';
import Dashboard from './pages/Dashboard';
import VendorManagement from './pages/vendors/VendorManagement';
import LabourManagement from './pages/labour/LabourManagement';
import Transactions from './pages/transactions/Transactions';
import Reports from './pages/reports/Reports';
import Login from './pages/auth/Login';
import PrivateRoute from './components/auth/PrivateRoute';

function App() {
  return (
    <Routes>
      <Route path="/login" element={<Login />} />
      
      <Route element={<PrivateRoute />}>
        <Route element={<Layout />}>
          <Route path="/" element={<Dashboard />} />
          <Route path="/vendors/*" element={<VendorManagement />} />
          <Route path="/labour/*" element={<LabourManagement />} />
          <Route path="/transactions/*" element={<Transactions />} />
          <Route path="/reports/*" element={<Reports />} />
        </Route>
      </Route>
    </Routes>
  );
}

export default App;

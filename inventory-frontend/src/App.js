import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import LoginPage from './pages/LoginPage';
import Dashboard from './pages/Dashboard';
import ItemDetail from './pages/ItemDetail';
import CreateItemPage from './pages/CreateItemPage';
import EditItemPage from './pages/EditItemPage';
import TransferItemPage from './pages/TransferItemPage';
import BulkTransferPage from './pages/BulkTransferPage';
import LocationReportPage from './pages/LocationReportPage';
import InventoryStatsPage from './pages/InventoryStatsPage';
import CSVImportPage from './pages/CSVImportPage';  // Импорт новой страницы
import ProtectedRoute from './ProtectedRoute';
import Navbar from './components/Navbar';

function App() {
  const isAuthenticated = !!localStorage.getItem('access_token');

  return (
    <BrowserRouter>
      {isAuthenticated && <Navbar />}
      <Routes>
        <Route path="/login" element={<LoginPage />} />
        <Route element={<ProtectedRoute isAuthenticated={isAuthenticated} />}>
          <Route path="/" element={<Dashboard />} />
          <Route path="/item/:id" element={<ItemDetail />} />
          <Route path="/create-item" element={<CreateItemPage />} />
          <Route path="/edit-item/:id" element={<EditItemPage />} />
          <Route path="/transfer-item/:id" element={<TransferItemPage />} />
          <Route path="/bulk-transfer" element={<BulkTransferPage />} />
          <Route path="/reports/location" element={<LocationReportPage />} />
          <Route path="/reports/stats" element={<InventoryStatsPage />} />
          <Route path="/import-csv" element={<CSVImportPage />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;

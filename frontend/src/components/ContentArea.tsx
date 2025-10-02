import { Routes, Route, Navigate } from 'react-router-dom';
import ProtectedRoute from './ProtectedRoute';
import Dashboard from '../pages/Dashboard';
import Unauthorized from '../pages/Unauthorized';
import AuditLog from '../pages/AuditLog';
import UserProfile from '../pages/UserProfile';
import Settings from '../pages/Settings';
import QRManagement from '../pages/QRManagement';

// RRHH Pages
import RRHHDashboard from '../pages/rrhh/RRHHDashboard';
import FuncionariosList from '../pages/rrhh/FuncionariosList';
import DepartamentosCargos from '../pages/rrhh/DepartamentosCargos';
import PresencasList from '../pages/rrhh/PresencasList';
import LicencasList from '../pages/rrhh/LicencasList';
import AvaliacoesList from '../pages/rrhh/AvaliacoesList';
import FolhaSalarialList from '../pages/rrhh/FolhaSalarialList';
import BeneficiosList from '../pages/rrhh/BeneficiosList';
import ComponentShowcase from '../pages/rrhh/ComponentShowcase';
import RRHHSimple from '../pages/rrhh/RRHHSimple';
import StatusChecker from '../components/rrhh/StatusChecker';
import PassesList from '../pages/rrhh/PassesList';
import PassesConfig from '../pages/rrhh/PassesConfig';

const ContentArea = () => {
  return (
    <Routes>
      <Route
        path="/dashboard"
        element={
          <ProtectedRoute>
            <Dashboard />
          </ProtectedRoute>
        }
      />
      <Route
        path="/qrcode"
        element={
          <ProtectedRoute>
            <QRManagement />
          </ProtectedRoute>
        }
      />
      <Route
        path="/perfil"
        element={
          <ProtectedRoute>
            <UserProfile />
          </ProtectedRoute>
        }
      />
      <Route
        path="/auditoria"
        element={
          <ProtectedRoute>
            <AuditLog />
          </ProtectedRoute>
        }
      />
      <Route
        path="/settings"
        element={
          <ProtectedRoute>
            <Settings />
          </ProtectedRoute>
        }
      />
      
      {/* RRHH Routes */}
      <Route
        path="/rrhh/dashboard"
        element={
          <ProtectedRoute>
            <RRHHDashboard />
          </ProtectedRoute>
        }
      />
      <Route
        path="/rrhh/funcionarios"
        element={
          <ProtectedRoute>
            <FuncionariosList />
          </ProtectedRoute>
        }
      />
      <Route
        path="/rrhh/departamentos"
        element={
          <ProtectedRoute>
            <DepartamentosCargos />
          </ProtectedRoute>
        }
      />
      <Route
        path="/rrhh/presencas"
        element={
          <ProtectedRoute>
            <PresencasList />
          </ProtectedRoute>
        }
      />
      <Route
        path="/rrhh/licencas"
        element={
          <ProtectedRoute>
            <LicencasList />
          </ProtectedRoute>
        }
      />
      <Route
        path="/rrhh/avaliacoes"
        element={
          <ProtectedRoute>
            <AvaliacoesList />
          </ProtectedRoute>
        }
      />
      <Route
        path="/rrhh/folha-salarial"
        element={
          <ProtectedRoute>
            <FolhaSalarialList />
          </ProtectedRoute>
        }
      />
      <Route
        path="/rrhh/beneficios"
        element={
          <ProtectedRoute>
            <BeneficiosList />
          </ProtectedRoute>
        }
      />
      <Route
        path="/rrhh/showcase"
        element={
          <ProtectedRoute>
            <ComponentShowcase />
          </ProtectedRoute>
        }
      />
      <Route
        path="/rrhh/simple"
        element={
          <ProtectedRoute>
            <RRHHSimple />
          </ProtectedRoute>
        }
      />
      <Route
        path="/rrhh/status-checker"
        element={
          <ProtectedRoute>
            <StatusChecker />
          </ProtectedRoute>
        }
      />
      <Route
        path="/rrhh/passes"
        element={
          <ProtectedRoute>
            <PassesList />
          </ProtectedRoute>
        }
      />
      <Route
        path="/rrhh/passes/configuracao"
        element={
          <ProtectedRoute>
            <PassesConfig />
          </ProtectedRoute>
        }
      />
      
      <Route path="/nao-autorizado" element={<Unauthorized />} />
      <Route
        path="*"
        element={
          <ProtectedRoute>
            <Navigate to="/dashboard" />
          </ProtectedRoute>
        }
      />
    </Routes>
  );
};

export default ContentArea;
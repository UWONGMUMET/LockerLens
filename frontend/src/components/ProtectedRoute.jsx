import { Navigate, useLocation } from 'react-router-dom';

import { useAuth } from '../context/AuthContext.jsx';

export default function ProtectedRoute({ children }) {
  const { isAuthenticated, checkingSession } = useAuth();
  const location = useLocation();

  if (checkingSession) {
    return (
      <div className="page-shell py-16">
        <div className="card p-6 text-sm text-zinc-600">Memeriksa sesi...</div>
      </div>
    );
  }

  if (!isAuthenticated) {
    return <Navigate to="/login" replace state={{ from: location }} />;
  }

  return children;
}

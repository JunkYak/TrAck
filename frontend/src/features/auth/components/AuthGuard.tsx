import { Navigate, Outlet } from 'react-router-dom';

function parseJwt(token: string) {
  try {
    return JSON.parse(atob(token.split('.')[1]));
  } catch (e) {
    return null;
  }
}

export const AuthGuard = () => {
  const token = localStorage.getItem('track_auth_token');

  // Check 1: Token exists?
  if (!token) {
    return <Navigate to="/login" replace />;
  }

  // Check 2: Token expired?
  const decoded = parseJwt(token);
  if (!decoded || !decoded.exp) {
    localStorage.removeItem('track_auth_token');
    return <Navigate to="/login" replace />;
  }

  const nowInSeconds = Math.floor(Date.now() / 1000);
  if (decoded.exp < nowInSeconds) {
    localStorage.removeItem('track_auth_token');
    return <Navigate to="/login" replace />;
  }

  // Check 3: Token Valid -> Allow access
  return <Outlet />;
};

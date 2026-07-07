import { useEffect, useState } from 'react';
import { useLocation, useSearchParams } from 'react-router-dom';

import AuthLayout from '../components/AuthLayout.jsx';
import LoginForm from '../components/LoginForm.jsx';
import RegisterForm from '../components/RegisterForm.jsx';

export default function LoginPage() {
  const [searchParams, setSearchParams] = useSearchParams();
  const location = useLocation();
  const [mode, setMode] = useState(searchParams.get('mode') === 'register' ? 'register' : 'login');
  const [notice, setNotice] = useState(location.state?.registered ? 'Akun berhasil dibuat. Silakan masuk.' : '');

  useEffect(() => {
    setMode(searchParams.get('mode') === 'register' ? 'register' : 'login');
  }, [searchParams]);

  function switchMode(nextMode) {
    setNotice('');
    setMode(nextMode);
    setSearchParams(nextMode === 'register' ? { mode: 'register' } : {}, { replace: true });
  }

  const isRegister = mode === 'register';

  return (
    <AuthLayout
      title={isRegister ? 'Buat akun LokerLens' : 'Masuk ke LokerLens'}
      subtitle={
        isRegister
          ? 'Buat akun untuk menyimpan hasil scan dan membuka riwayat analisis.'
          : 'Masuk untuk menyimpan hasil scan lowongan dan melihat riwayat analisis kamu.'
      }
    >
      {isRegister ? (
        <RegisterForm
          onSwitchMode={() => switchMode('login')}
          onRegistered={() => {
            setMode('login');
            setSearchParams({}, { replace: true });
            setNotice('Akun berhasil dibuat. Silakan masuk.');
          }}
        />
      ) : (
        <LoginForm onSwitchMode={() => switchMode('register')} notice={notice} />
      )}
    </AuthLayout>
  );
}

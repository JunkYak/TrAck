export const LoginPage = () => {
  const handleGoogleLogin = () => {
    // Vite uses VITE_API_URL instead of BACKEND_URL generally, but let's default to what env variables specify
    // If not set, fallback to localhost:8000
    const backendUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000';
    window.location.href = `${backendUrl}/auth/google/login`;
  };

  return (
    <div className="min-h-screen bg-[#0A0A0A] flex flex-col items-center justify-center p-4">
      <div className="w-full max-w-md text-center space-y-8">
        <div>
          <h1 className="text-5xl font-black tracking-tighter text-amber-500">
            trAck
          </h1>
          <p className="mt-4 text-gray-400 font-bold">
            Sign in to track your nutrition, training, and health.
          </p>
        </div>

        <button
          onClick={handleGoogleLogin}
          className="w-full bg-white hover:bg-gray-100 text-black font-bold py-4 px-6 rounded-xl transition-colors flex items-center justify-center space-x-3"
        >
          <svg className="w-6 h-6" viewBox="0 0 48 48">
            <title>Google Logo</title>
            <clipPath id="g">
              <path d="M44.5 20H24v8.5h11.8C34.7 33.9 30.1 37 24 37c-7.2 0-13-5.8-13-13s5.8-13 13-13c3.1 0 5.9 1.1 8.1 2.9l6.4-6.4C34.6 4.1 29.6 2 24 2 11.8 2 2 11.8 2 24s9.8 22 22 22c11 0 21-8 21-22 0-1.3-.2-2.7-.5-4z"/>
            </clipPath>
            <g className="colors" clipPath="url(#g)">
              <path fill="#FBBC05" d="M0 37V11l17 13z"/>
              <path fill="#EA4335" d="M0 11l17 13 7-6.1L48 14V0H0z"/>
              <path fill="#34A853" d="M0 37l30-23 7.9 1L48 0v48H0z"/>
              <path fill="#4285F4" d="M48 48L17 24l-4-3 35-10z"/>
            </g>
          </svg>
          <span className="text-lg">Sign In With Google</span>
        </button>

        <p className="text-sm text-gray-600 font-medium">
          By signing in, you agree to our Terms of Service and Privacy Policy.
        </p>
      </div>
    </div>
  );
};

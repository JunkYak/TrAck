interface ErrorStateProps {
  message?: string;
}

export const ErrorState = ({ message = 'Failed to load data. Please try again.' }: ErrorStateProps) => {
  return (
    <div className="flex flex-col items-center justify-center h-64 text-red-400 bg-red-950/20 border border-red-900/50 rounded-lg p-6 text-center">
      <svg className="w-10 h-10 mb-4 text-red-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
      </svg>
      <h3 className="text-lg font-bold text-red-500 mb-2">Something went wrong</h3>
      <p className="text-sm">{message}</p>
    </div>
  );
};

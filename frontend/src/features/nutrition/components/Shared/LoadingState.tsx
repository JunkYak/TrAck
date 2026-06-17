export const LoadingState = () => {
  return (
    <div className="flex flex-col items-center justify-center h-64 text-gray-400">
      <div className="w-8 h-8 border-2 border-amber-500 border-t-transparent rounded-full animate-spin mb-4"></div>
      <p className="text-sm font-medium">Loading...</p>
    </div>
  );
};

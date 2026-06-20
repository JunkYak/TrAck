export const formatPace = (decimalPace: number): string => {
  if (!decimalPace || decimalPace <= 0) return '-:--/km';
  const mins = Math.floor(decimalPace);
  const secs = Math.round((decimalPace - mins) * 60);
  // Handle edge case where rounding seconds hits 60
  if (secs === 60) {
    return `${mins + 1}:00/km`;
  }
  return `${mins}:${secs.toString().padStart(2, '0')}/km`;
};

export const formatRunType = (runType: string): string => {
  switch (runType) {
    case 'EASY': return 'Easy Run';
    case 'TEMPO_INTERVAL': return 'Tempo Run';
    case 'LONG': return 'Long Run';
    default: return runType;
  }
};

export const formatDuration = (minutes: number): string => {
  if (minutes < 60) return `${Math.round(minutes)} min`;
  const hrs = Math.floor(minutes / 60);
  const mins = Math.round(minutes % 60);
  if (mins === 0) return `${hrs} hr`;
  return `${hrs} hr ${mins} min`;
};

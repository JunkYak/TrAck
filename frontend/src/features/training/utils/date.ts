export const getStartOfWeekDate = (date: Date = new Date()): string => {
  const d = new Date(date);
  const day = d.getDay();
  // day is 0 (Sun) to 6 (Sat). We want Monday to be 0.
  const diff = d.getDate() - day + (day === 0 ? -6 : 1); 
  d.setDate(diff);
  d.setHours(0, 0, 0, 0);
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`;
};

export const getWeekNumber = (dateString: string): string => {
  const d = new Date(dateString + 'T00:00:00');
  const year = d.getFullYear();
  const startDate = new Date(year, 0, 1);
  const days = Math.floor((d.getTime() - startDate.getTime()) / (24 * 60 * 60 * 1000));
  const weekNumber = Math.ceil((d.getDay() + 1 + days) / 7);
  return `Week ${weekNumber}`;
};

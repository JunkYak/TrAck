import axios from 'axios';

async function test() {
  try {
    const res = await axios.post('http://localhost:8000/api/v1/cardio', {
      run_type: 'TEMPO_INTERVAL',
      distance_km: 10,
      duration_minutes: 58,
      notes: undefined,
      performed_at: '2026-06-18T00:00:00.000Z'
    }, {
      headers: { 'Authorization': 'Bearer mock' }
    });
    console.log('Success:', res.data);
  } catch (err: any) {
    console.error('Error:', err.response?.data);
  }
}

test();

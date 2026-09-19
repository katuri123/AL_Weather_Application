const form = document.querySelector('#search-form');
const message = document.querySelector('#message');
const result = document.querySelector('#result');
const set = (id, value) => document.querySelector(id).textContent = value ?? 'Unavailable';

form.addEventListener('submit', async (event) => {
  event.preventDefault();
  const button = form.querySelector('button');
  const city = form.city.value.trim();
  message.textContent = 'Getting current conditions…'; result.hidden = true; button.disabled = true;
  try {
    const response = await fetch('/api/weather', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({city})});
    const data = await response.json();
    if (!response.ok) throw new Error(data.error || 'Something went wrong.');
    const w = data.weather;
    set('#place', [w.location, w.country].filter(Boolean).join(', ')); set('#condition', w.condition);
    set('#temp', `${w.temperature}${w.temperature_unit}`); set('#description', w.description);
    set('#feels', `${w.feels_like ?? 'Unavailable'}${w.feels_like == null ? '' : w.temperature_unit}`); set('#humidity', w.humidity == null ? null : `${w.humidity}%`);
    set('#wind', [w.wind_speed == null ? null : `${w.wind_speed} ${w.wind_unit}`, w.wind_direction].filter(Boolean).join(' · '));
    set('#timestamp', `Observed ${new Date(w.observed_at).toLocaleString()}`); set('#explanation', data.ai_explanation || data.ai_error);
    set('#source', `Source: ${w.source} · Retrieved ${new Date(w.retrieved_at).toLocaleTimeString()}`); message.textContent = ''; result.hidden = false;
  } catch (error) { message.textContent = error.message; }
  finally { button.disabled = false; }
});

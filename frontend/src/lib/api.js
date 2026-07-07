const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8010';
const TOKEN_KEY = 'lokerlens_access_token';
const USER_KEY = 'lokerlens_user';

async function request(path, options = {}) {
  const token = getAccessToken();
  const { headers: optionHeaders = {}, ...fetchOptions } = options;
  const response = await fetch(`${API_BASE_URL}${path}`, {
    ...fetchOptions,
    headers: {
      'Content-Type': 'application/json',
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
      ...optionHeaders,
    },
  });

  const data = await response.json().catch(() => ({}));

  if (!response.ok) {
    const detail = Array.isArray(data.detail)
      ? data.detail.map((item) => item.msg || item.message || JSON.stringify(item)).join(', ')
      : data.detail;
    throw new Error(detail || 'Request gagal diproses.');
  }

  return data;
}

export function getAccessToken() {
  return localStorage.getItem(TOKEN_KEY);
}

export function getStoredUser() {
  const raw = localStorage.getItem(USER_KEY);
  if (!raw) return null;
  try {
    return JSON.parse(raw);
  } catch {
    return null;
  }
}

export function storeAuthSession({ access_token, user }) {
  localStorage.setItem(TOKEN_KEY, access_token);
  localStorage.setItem(USER_KEY, JSON.stringify(user));
}

export function clearAuthSession() {
  localStorage.removeItem(TOKEN_KEY);
  localStorage.removeItem(USER_KEY);
}

export function registerUser(payload) {
  return request('/auth/register', {
    method: 'POST',
    body: JSON.stringify(payload),
  });
}

export function loginUser(payload) {
  return request('/auth/login', {
    method: 'POST',
    body: JSON.stringify(payload),
  });
}

export function fetchMe() {
  return request('/auth/me');
}

export function fetchProfile() {
  return request('/auth/profile');
}

export function scanJob(payload) {
  return request('/scan', {
    method: 'POST',
    body: JSON.stringify(payload),
  });
}

export function fetchScanHistory() {
  return request('/scan/history');
}

export function fetchScanHistoryDetail(id) {
  return request(`/scan/history/${id}`);
}

export function deleteScanHistoryItem(id) {
  return request(`/scan/history/${id}`, {
    method: 'DELETE',
  });
}

export function sendContactMessage(payload) {
  return request('/contact', {
    method: 'POST',
    body: JSON.stringify(payload),
  });
}

export { API_BASE_URL };

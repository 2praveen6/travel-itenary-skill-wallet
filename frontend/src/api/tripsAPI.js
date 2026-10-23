import { api } from "./client";

export const tripsAPI = {
  list: (token) => api("/api/trips", { token }),
  get: (id, token) => api(`/api/trips/${id}`, { token }),
  create: (body, token) => api("/api/trips", { method: "POST", body, token }),
  update: (id, body, token) => api(`/api/trips/${id}`, { method: "PUT", body, token }),
  remove: (id, token) => api(`/api/trips/${id}`, { method: "DELETE", token }),
  generate: (id, token) => api(`/api/trips/${id}/generate`, { method: "POST", token }),
  export: (id, format, token) => api(`/api/trips/${id}/export?format=${format}`, { token }),
  addActivity: (id, dayId, body, token) =>
    api(`/api/trips/${id}/days/${dayId}/activities`, { method: "POST", body, token }),
  removeActivity: (id, activityId, token) =>
    api(`/api/trips/${id}/activities/${activityId}`, { method: "DELETE", token }),
  refine: (id, body, token) => api(`/api/trips/${id}/refine`, { method: "POST", body, token }),
  share: (id, token) => api(`/api/trips/${id}/share`, { method: "POST", token }),
  getShared: (tokenId) => api(`/api/share/${tokenId}`),
};

export const templatesAPI = {
  list: () => api("/api/templates"),
  get: (id) => api(`/api/templates/${id}`),
  clone: (id, body, token) => api(`/api/templates/${id}/clone`, { method: "POST", body: body || {}, token }),
};

export const prefsAPI = {
  get: (token) => api("/api/preferences", { token }),
  save: (body, token) => api("/api/preferences", { method: "PUT", body, token }),
  recommend: (body, token) => api("/api/recommendations", { method: "POST", body: body || {}, token }),
};

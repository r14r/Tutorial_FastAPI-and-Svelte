import axios from "axios";
import { get } from "svelte/store";
import { token } from "../stores/auth";

const client = axios.create({
  baseURL: "/api",
  headers: {
    "Content-Type": "application/json"
  }
});

client.interceptors.request.use((config) => {
  const authToken = get(token);
  if (authToken) {
    config.headers.Authorization = `Bearer ${authToken}`;
  }
  return config;
});

export async function registerUser(payload) {
  const response = await client.post("/auth/register", payload);
  return response.data;
}

export async function loginUser(payload) {
  const params = new URLSearchParams();
  params.append("username", payload.email);
  params.append("password", payload.password);
  const response = await client.post("/auth/token", params, {
    headers: { "Content-Type": "application/x-www-form-urlencoded" }
  });
  return response.data;
}

export async function getProfile() {
  const response = await client.get("/users/me");
  return response.data;
}

export async function getItems() {
  const response = await client.get("/items");
  return response.data;
}

export async function createItem(payload) {
  const response = await client.post("/items", payload);
  return response.data;
}

export async function updateItem(id, payload) {
  const response = await client.put(`/items/${id}`, payload);
  return response.data;
}

export async function deleteItem(id) {
  await client.delete(`/items/${id}`);
}

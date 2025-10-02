import { writable } from "svelte/store";
import { browser } from "./app/environment.js";

const FALLBACK_URL = "http://localhost/";

function createUrl() {
  if (!browser) {
    return new URL(FALLBACK_URL);
  }
  return new URL(window.location.href);
}

const pageStore = writable({ url: createUrl() });

function syncWithLocation() {
  pageStore.set({ url: createUrl() });
}

if (browser) {
  const update = () => syncWithLocation();
  window.addEventListener("popstate", update);
  window.addEventListener("hashchange", update);
}

export const page = {
  subscribe: pageStore.subscribe
};

export function navigate(path, options = {}) {
  if (!browser) {
    return Promise.resolve();
  }

  const target = new URL(path, window.location.origin);
  if (options.replaceState) {
    history.replaceState({}, "", target);
  } else {
    history.pushState({}, "", target);
  }
  syncWithLocation();
  return Promise.resolve();
}

export function syncPage() {
  syncWithLocation();
}

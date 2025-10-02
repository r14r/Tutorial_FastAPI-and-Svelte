import { browser } from "$app/environment";
import { writable } from "svelte/store";

const storedToken = browser ? localStorage.getItem("token") : null;
const storedUser = browser ? localStorage.getItem("user") : null;

export const token = writable(storedToken);
export const currentUser = writable(storedUser ? JSON.parse(storedUser) : null);

if (browser) {
  token.subscribe((value) => {
    if (value) {
      localStorage.setItem("token", value);
    } else {
      localStorage.removeItem("token");
    }
  });

  currentUser.subscribe((value) => {
    if (value) {
      localStorage.setItem("user", JSON.stringify(value));
    } else {
      localStorage.removeItem("user");
    }
  });
}

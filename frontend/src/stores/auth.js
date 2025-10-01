import { writable } from "svelte/store";

const storedToken = typeof localStorage !== "undefined" ? localStorage.getItem("token") : null;
const storedUser = typeof localStorage !== "undefined" ? localStorage.getItem("user") : null;

export const token = writable(storedToken);
export const currentUser = writable(storedUser ? JSON.parse(storedUser) : null);

if (typeof localStorage !== "undefined") {
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

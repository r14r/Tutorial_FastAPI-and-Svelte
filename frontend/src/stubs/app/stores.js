import { page as pageStore } from "../router.js";

export const page = pageStore;

export function getStores() {
  return { page: pageStore };
}

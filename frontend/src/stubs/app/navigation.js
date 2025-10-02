import { navigate } from "../router.js";

export function goto(path, options) {
  return navigate(path, options);
}

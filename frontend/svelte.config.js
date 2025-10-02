import adapter from "@sveltejs/adapter-auto";
import { vitePreprocess } from "@sveltejs/kit/vite";

const config = {
  preprocess: vitePreprocess(),
  kit: {
    adapter,
    alias: {
      $stores: "src/lib/stores"
    }
  }
};

export default config;

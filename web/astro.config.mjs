import { defineConfig } from 'astro/config';
import react from '@astrojs/react';
import mdx from '@astrojs/mdx';
import sitemap from '@astrojs/sitemap';
import tailwind from '@astrojs/tailwind';

export default defineConfig({
  site: 'https://resanalyze.vercel.app',
  integrations: [
    react(),
    mdx(),
    tailwind({
      configFile: './tailwind.config.cjs',
    }),
  ],
  vite: {
    optimizeDeps: {
      include: ['react-reconciler', 'scheduler', 'its-fine', 'react-use-measure', 'zustand'],
    },
    ssr: {
      noExternal: ['three', '@react-three/drei', '@react-three/fiber', 'react-three-fiber'],
    },
  },
});

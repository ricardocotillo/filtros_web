const { resolve } = require('path');

module.exports = {
  root: resolve('./src'),
  base: '/static/',
  server: {
    host: '0.0.0.0',
    port: 5173,
    open: false,
    watch: {
      usePolling: true,
      disableGlobbing: false,
    },
  },
  resolve: {
    extensions: ['.js', '.json'],
  },
  build: {
    outDir: resolve('./dist'),
    assetsDir: '',
    manifest: 'manifest.json',
    emptyOutDir: true,
    target: 'es2015',
    rollupOptions: {
      input: {
        main: resolve('./src/js/main.js'),
      },
      output: {
        chunkFileNames: undefined,
      },
    },
  },
};
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
    emptyOutDir: true,
    target: 'es2017',
    rollupOptions: {
      input: {
        main: resolve('./src/js/main.js'),
      },
      output: {
        entryFileNames: 'js/[name].js',
        chunkFileNames: '[ext]/[name].[ext]',
        assetFileNames: '[ext]/[name].[ext]',
      },
    },
  },
};
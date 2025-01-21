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
    cssCodeSplit: true,
  },
  plugins: [
    {
      name: 'manifest-css-entry',
      enforce: 'post',
      generateBundle(_, bundle) {
        const manifest = {};
        for (const [fileName, chunk] of Object.entries(bundle)) {
          if (chunk.type === 'chunk') {
            if (chunk.isEntry) {
              manifest[chunk.fileName] = {
                file: chunk.fileName,
                name: chunk.name,
                src: chunk.facadeModuleId ? chunk.facadeModuleId.replace(process.cwd(), '') : '',
                isEntry: true,
                css: chunk.viteMetadata?.importedCss || [],
              };
            }
          } else if (chunk.type === 'asset' && chunk.fileName.endsWith('.css')) {
            manifest[chunk.fileName] = {
              file: chunk.fileName,
              name: chunk.fileName.replace(/\.css$/, ''),
              src: chunk.fileName,
              isEntry: true,
            };
          }
        }
        this.emitFile({
          type: 'asset',
          fileName: 'manifest.json',
          source: JSON.stringify(manifest, null, 2),
        });
      },
    },
  ],
};
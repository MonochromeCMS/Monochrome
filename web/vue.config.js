const path = require('path');
const XMLPlugin = require('xml-webpack-plugin');

const protocol = process.env.VUE_APP_PROTOCOL || 'http';
const domainName = process.env.VUE_APP_DOMAIN_NAME || 'localhost';
const title = process.env.VUE_APP_TITLE || 'Monochrome';
const url = `${protocol}://${domainName}/`;

const XMLFiles = [
  {
    template: path.join(__dirname, './src/opensearch.ejs'),
    filename: 'opensearch.xml',
    data: {
      url,
      title,
    },
  },
];

const metaArgs = {
  title,
  url,
  description: process.env.VUE_APP_DESCRIPTION || 'A website for reading manga',
};

/** @type {import('@vue/cli-service').ProjectOptions} */
module.exports = {
  transpileDependencies: ['vuetify'],
  devServer: {
    port: 80,
  },
  pwa: {
    name: title,
    themeColor: '#212121',
    workboxOptions: {
      cleanupOutdatedCaches: true,
      skipWaiting: true,
    },
  },
  chainWebpack: (config) => {
    config.plugin('html').tap((args) => {
      args[0] = { ...args[0], ...metaArgs };
      return args;
    });
    config.plugins.delete('fork-ts-checker');
  },
  configureWebpack: {
    plugins: [
      new XMLPlugin({
        files: XMLFiles,
      }),
    ],
  },
};

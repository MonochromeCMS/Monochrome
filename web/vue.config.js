const path = require("path");
const os = require("os");
const XMLPlugin = require("xml-webpack-plugin");

const protocol = process.env.VUE_APP_PROTOCOL || "http";
const domainName = process.env.VUE_APP_DOMAIN_NAME || "localhost";
const title = process.env.VUE_APP_TITLE || "Monochrome";
const url = `${protocol}://${domainName}/`;

const XMLFiles = [
  {
    template: path.join(__dirname, "./src/opensearch.ejs"),
    filename: "opensearch.xml",
    data: {
      url,
      title,
    },
  },
];

const metaArgs = {
  title,
  url,
  description: process.env.VUE_APP_DESCRIPTION || "A website for reading manga",
};

module.exports = {
  transpileDependencies: ["vuetify"],
  pwa: {
    name: title,
    themeColor: "#212121",
    workboxOptions: {
      cleanupOutdatedCaches: true,
      skipWaiting: true,
    },
  },
  chainWebpack: (config) => {
    config.plugin("html").tap((args) => {
      args[0] = { ...args[0], ...metaArgs };
      return args;
    });
    config.plugin("fork-ts-checker").tap((args) => {
      let totalmem = Math.floor(os.totalmem() / 1024 / 1024); //get OS mem size
      let allowUseMem = totalmem > 2500 ? 2048 : 1000;
      args[0].memoryLimit = allowUseMem;
      return args;
    });
  },
  configureWebpack: {
    plugins: [
      new XMLPlugin({
        files: XMLFiles,
      }),
    ],
  },
};

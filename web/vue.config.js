const path = require("path");
const XMLPlugin = require("xml-webpack-plugin");

const protocol = process.env.VUE_APP_PROTOCOL || "http";
const domainName = process.env.VUE_APP_DOMAIN_NAME || "localhost";
const title = process.env.VUE_APP_TITLE || "Monochrome";

const XMLFiles = [
  {
    template: path.join(__dirname, "./src/opensearch.ejs"),
    filename: "opensearch.xml",
    data: {
      domainName,
      protocol,
    },
  },
];

const metaArgs = {
  title,
  url: `${protocol}://${domainName}/`,
  description: process.env.VUE_APP_DESCRIPTION || "A website for reading manga",
};

module.exports = {
  transpileDependencies: ["vuetify"],
  pwa: {
    name: title,
    themeColor: "#212121",
  },
  chainWebpack: config => {
    config.plugin('html').tap((args) => {
      args[0] = {...args[0], ...metaArgs};
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

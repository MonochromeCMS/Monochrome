const path = require("path");
const XMLPlugin = require("xml-webpack-plugin");

const XMLFiles = [
  {
    template: path.join(__dirname, "./src/opensearch.ejs"),
    filename: "opensearch.xml",
    data: {
      domainName: process.env.VUE_APP_DOMAIN_NAME,
      protocol: process.env.VUE_APP_PROTOCOL,
    },
  },
];

module.exports = {
  transpileDependencies: ["vuetify"],
  configureWebpack: {
    plugins: [
      new XMLPlugin({
        files: XMLFiles,
      }),
    ],
  },
};

import Vue from "vue";
import Vuetify from "vuetify/lib/framework";

import colors from "vuetify/lib/util/colors";

Vue.use(Vuetify);

export default new Vuetify({
  theme: {
    themes: {
      light: {
        primary: colors.shades.black,
        secondary: colors.grey.darken3,
        accent: colors.purple.accent1,
        background: colors.grey.lighten3,
        backgroundAlt: colors.shades.white,
      },
      dark: {
        primary: colors.shades.white,
        secondary: colors.grey.lighten3,
        accent: colors.purple.accent4,
        background: colors.shades.black,
        backgroundAlt: colors.grey.darken4,
      },
    },
  },
});

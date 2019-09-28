import Vue from 'vue';
import Vuetify from 'vuetify/lib';
import ru from 'vuetify/src/locale/ru';

Vue.use(Vuetify);

// primary new: 5100d3
// primary old: 4a76a8
// vk messages background: d6e7f9

export default new Vuetify({
  theme: {
    themes: {
      light: {
        primary: '#5100d3',
        secondary: '#424242',
        accent: '#82B1FF',
        error: '#FF5252',
        info: '#2196F3',
        success: '#4CAF50',
        warning: '#FFC107',
      },
      // options: {
      //   customProperties: true,
      // },
    },
  },
  lang: {
    locales: { ru },
    current: 'ru',
  },
  icons: {
    iconfont: 'mdi',
  },
});

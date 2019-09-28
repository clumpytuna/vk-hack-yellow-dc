import Vue from 'vue';
import Vuetify from 'vuetify/lib';
import ru from 'vuetify/src/locale/ru';

Vue.use(Vuetify);

let a = {
  'primary': '#4a76a8',
  'messages': '#d6e7f9',
};

export default new Vuetify({
  theme: {
    themes: {
      light: {
        primary: '#4a76a8',
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

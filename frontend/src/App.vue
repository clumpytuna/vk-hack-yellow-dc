<template>
  <v-app id="app" :class="{'increased-font': increasedFont}">
    <v-navigation-drawer v-model="drawer" app>
      <v-list dense>
        <v-list-item to="/">
          <v-list-item-action>
            <v-icon>mdi-home</v-icon>
          </v-list-item-action>
          <v-list-item-content>
            <v-list-item-title>Home</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </v-list>

      <v-switch
        v-model="increasedFont"
        label="Версия с увеличенным шрифтом"
        class="ml-4 mt-12"
      />
    </v-navigation-drawer>

    <v-app-bar app color="primary" dark>
      <v-app-bar-nav-icon @click.stop="drawer = !drawer"></v-app-bar-nav-icon>
      <v-toolbar-title>Пушкинский музей</v-toolbar-title>
    </v-app-bar>

    <v-content>
      <v-container fill-height fluid>
        <router-view :increasedFont="increasedFont" />
      </v-container>
    </v-content>
  </v-app>
</template>

<style>
  #app {
    font-family: GMTypewriter, 'Avenir', Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    background: white !important;
  }

  * {
    box-sizing: border-box !important;
  }

  @font-face {
    font-family: 'GMText';
    font-weight: 400;
    font-style: normal;

    src: url('/fonts/GMTextRegular.woff');
  }

  @font-face {
    font-family: 'GMTypewriter';
    font-weight: 400;
    font-style: normal;

    src: url('/fonts/GMTypewriterRegular.woff');
  }
</style>

<script>
  export default {
    data: () => ({
      drawer: false,
      increasedFont: false,
    }),
    watch: {
      increasedFont(newValue, oldValue) {
        if (newValue === true && oldValue === false) {
          this.drawer = false;
        }
      },
    },
  };
</script>

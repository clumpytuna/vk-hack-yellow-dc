<template>
  <v-app id="app">
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
        <v-list-item to="/about">
          <v-list-item-action>
            <v-icon>mdi-contact-mail</v-icon>
          </v-list-item-action>
          <v-list-item-content>
            <v-list-item-title>About</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>

    <v-app-bar app color="primary" dark>
      <v-app-bar-nav-icon @click.stop="drawer = !drawer"></v-app-bar-nav-icon>
      <v-toolbar-title>Пушкинский музей</v-toolbar-title>
    </v-app-bar>

    <v-content>
      <v-container fill-height fluid>
        <!--        <v-row align="center" justify="center"></v-row>-->
        <router-view />
      </v-container>
    </v-content>
  </v-app>
</template>

<style>
  #app {
    font-family: 'Avenir', Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    background: white !important;
  }

  * {
    box-sizing: border-box !important;
  }
</style>

<script>
  export default {
    data: () => ({
      drawer: null,
    }),
  };
</script>

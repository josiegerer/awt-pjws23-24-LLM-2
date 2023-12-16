<template>
  <div id="app">
    <TestNavbar />
    <!-- <LoginPage /> -->
    <!-- <UserChats />  -->
    <router-view></router-view>
  </div>
</template>

<script>
import TestNavbar from './components/TestNavbar.vue'
// import LoginPage from './components/LoginPage.vue'
// import UserChats from './components/UserChats.vue';

export default {
  name: 'App',
  components: {
    TestNavbar,
  //   LoginPage,
  //   UserChats
  }
}
</script>

<style>

</style>

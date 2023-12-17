<template>
  <div id="app">
    <TestNavbar />
    <!-- <LoginPage />-->
    <!-- <UserChats />  -->
    <router-view></router-view>
  </div>

</template>

<script>
import TestNavbar from './components/TestNavbar.vue'
//import LoginPage from './components/LoginPage.vue'
// import UserChats from './components/UserChats.vue';

export default {
  name: 'App',
  components: {
    TestNavbar,
  //LoginPage,
  //   UserChats
  }
}
</script>


<style>
@import url('https://fonts.googleapis.com/css?family=IBM Plex Mono');

html, body{
  font-family: 'IBM Plex Mono', monospace;
  color:#353839;
  height: 100%;
  width: 100%;
  overflow-x: hidden;
  padding: 0;
  margin: 0;
}

#app{
  font-family: 'IBM Plex Mono', monospace;
  background:#f9f9f9;
    height: 100%;
  width: 100%;

}


</style>

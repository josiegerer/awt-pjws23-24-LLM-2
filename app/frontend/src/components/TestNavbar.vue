<template>
  <nav class="navbar navbar-expand-lg stroke">
  <!-- <h1>This is our navbar.</h1> -->
  <!--<a class="navbar-brand" href="/">Navbar</a>-->
  <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNavAltMarkup" aria-controls="navbarNavAltMarkup" aria-expanded="false" aria-label="Toggle navigation">
    <span class="navbar-toggler-icon"></span>
  </button>
  <div class="collapse navbar-collapse" id="navbarNavAltMarkup">
    <div class="navbar-nav ms-auto">
      <router-link to="/" exact class="nav-item nav-link active">Home</router-link>
      <router-link class="nav-item nav-link" to="/ChatWindow">Chats</router-link>
      <a class="nav-item nav-link" href="#">Features</a>
      <a class="nav-item nav-link" href="#">Profile</a>
      <a class="nav-item nav-link nav-logout" href="#">Logout</a>
      <a class="nav-item nav-link" href="#"></a>
      <div class="logo-container">
          <span class="logo-text">langchatAI</span>
          <img class="logo" :src="require('@/assets/logo.png')" alt="Logo">
      </div>
    </div>
  </div>
  </nav>
</template>

<script>
export default {
}
</script>

<style>
/* NAVIGATION */
nav{
  width: 100%;
  margin: 0;
  background:#f9f9f9;
  padding-left: 0;
  position:fixed;
  top: 0;
  left: 0;
  font-family: 'IBM Plex Mono', monospace;
}
nav a{
  display: inline-block;
  text-decoration: none;
  color: #a9a9a9; 
  font-weight: 400;
  font-size: 16px;
  text-transform: uppercase;
  margin: 0 30px;
  font-style: normal;
}

.nav-logout{
  margin-left: 70px;
  margin-right: -30px;
  border: #003EC6 1px solid;
}

nav img.logo {
  width: 50px;
  height: auto;
  margin-right: 20px;
  margin-left: 10px;
}

nav .logo-text {
  font-weight: 800;
  color: #444;
}

nav, nav button{
  list-style: none;
  text-align: left;
  align-items: center;
  display: flex;
  padding-left: 20px;
}

/* hightlight current */
nav a.active, nav a.stroke{
  color: #003EC6;
}

  /* sliding in */
  nav a,
  nav a:after,
  nav a:before {
    transition: all 0.75s;
  }

  nav a:hover, nav a button:hover, nav a button {
    color:#353839;
  }

  /* stroke */
  nav.stroke a{
    position: relative;
  }

  /* normal nav */
  nav.stroke a:after
 {
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    margin: auto;
    width: 0%;
    content: '.';
    color: transparent;
    background: #003EC6;
    height: 1px;
  }

  nav.stroke a:hover:after  {
    width: 100%;
  }

nav ul li img.logo {
    width: 50px; 
    height: auto;
    margin-right: auto;
}

nav ul li .logo-text {
    display: inline-block;
    vertical-align: middle;
    margin-right: 0;
    padding-right: 10px;
    font-weight: 800;
    color: #444;
    margin-right: auto;
}

</style>
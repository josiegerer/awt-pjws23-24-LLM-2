<template>
  <form @submit.prevent="submitForm">
    <input class="create-user-name" type="text" v-model="username" required placeholder="Enter Username">
    <button type="submit" class="btn btn-dark">
      Create User
    </button>
  </form>
</template>

<script>
export default {
  data() {
    return {
      showModal: false,
      username: "",
    };
  },
  methods: {
    submitForm() {
      // Call the backend to create a new user
      this.$emit("createUser", this.username);
      this.showModal = false;
    },
  },
};
</script>

<style>
button.btn-dark{
  margin: 50px 30px;
  height: 40px;
  background-color: #888888; 
  color: #fff;
  border: transparent;
}

button.btn-dark:hover{
  background-color: #003EC6;
  color: #fff;
  border: transparent;
}

input.create-user-name{
  height: 40px;
  margin-top: 50px;
}

</style>
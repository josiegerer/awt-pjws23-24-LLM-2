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
  border-radius: 5px;
}

button.btn-dark:hover{
  background-color: #003EC6;
  color: #fff;
  border: transparent;
  border-radius: 5x;
}

input.create-user-name{
  height: 40px;
  margin-top: 50px;
  border-radius: 5px;
  border: #888 solid 1px;
}

.user-box {
  border-radius: 5px !important;
  border: #888 solid 1px !important;
  height: 4rem !important;
  width: 10rem !important;
  padding: 1rem !important;
  text-align: center !important;
}

.user-box:hover{
  background-color: #003EC6  !important;
  color: #fff;
}

</style>
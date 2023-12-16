<template>
  <form @submit.prevent="submitForm">
    <input type="text" v-model="username" required placeholder="Enter Username">
    <button type="submit" class="btn btn-dark">Create User</button>
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

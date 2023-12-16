<template>
  <div>
    <div v-if="users.length > 0">
      <router-link
        v-for="user in users" 
        :key="user.id" 
        class="user-box" 
        :to="'/user_chats/' + (user.id)"
      >
        {{ user.username }}
    </router-link>
    </div>
    <div v-else>
      <hr>
      <p>No user is <span>registered</span></p>
    </div>
    <user-create-modal @createUser="createUser" />
  </div>
</template>

<script>
import axios from 'axios';
import UserCreateModal from './UserCreateModal.vue';

export default {
  components: {
    UserCreateModal,
  },
  props: ["user"],
  data() {
    return {
      users: [],
    };
  },
  mounted() {
    this.fetchUsers();
  },
  methods: {
    async fetchUsers() {
      try {
        const response = await axios.get('http://localhost:5000/get_users');
        this.users = response.data;
      } catch (error) {
        console.error('Error fetching users:', error);
      }
    },
    createUser(username) {
      axios.post('http://localhost:5000/add_user', {username})
      .then(response => {
        console.log(response.data);
        this.fetchUsers();
      })
      .catch(error => {
        console.error("Error creating user", error);
      })
    },
    navigateToUserChats(userID) {
      console.log('Navigating to UserChats for user ID:', userID);
      this.$router.push({ name: "user-chats", params: { id: userID } });
    }
  },
};
</script>

<style>
.user-box {
  display: inline-block;
  margin: 10px;
  padding: 10px;
  border-radius: 50%;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  background-color: #ffffff;
  text-align: center;
  text-decoration: none;
  color: #333;
  cursor: pointer;
  transition: background-color 0.3s;
}

.user-box:hover {
  background-color: #f0f0f0;
}

</style>

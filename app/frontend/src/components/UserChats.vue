<template>
  <div>
    <h3>Chat Names</h3>
    <ul>
      <li v-for="chat in chats" :key="chat.chat_id">{{ chat.chat_name }}</li>
    </ul>
  </div>
</template>
  
<script>
import axios from 'axios';

export default {
  props: ["chat"],
  data() {
    return {
      chats: [],
    };
  },
  created() {
    console.log('UserChats component mounted. User ID:', this.$route.params.id);
    this.fetchChats();
  },
  mounted() {
    console.log('UserChats component mounted. User ID:', this.$route.params.id);
    // The fetchChats method might be called here as well, depending on your needs.
  },
  methods: {
    async fetchChats() {
      try {
        console.log(`${this.$route.params.id}`)
        const response = await axios.get(`http://localhost:5000/user_chats/${this.$route.params.id}`);
        this.chats = response.data;
      } catch (error) {
        console.error('Error fetching chats:', error);
      }
    },
  },
};
</script>
  
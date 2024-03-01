<template>
  <v-text-field v-model="title" label="Type new your task and hit enter to add it" @keyup.enter="addTodo" />
</template>

<script>
export default {
  data() {
    return {
      title: '',
    };
  },
  methods: {
    addTodo() {
      if (this.title.trim() !== '') {
        this.$emit('add', { title: this.title, description: this.title, priority: 3 });
        this.title = '';
      }
    },
  },
};
</script>

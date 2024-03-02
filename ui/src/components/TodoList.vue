<template>
  <v-list subheader two-line flat>
    <TodoItem v-for="todo in todos" :key="todo.id" :todo="todo" @delete="onDelete" @complete="onComplete" />
  </v-list>
</template>

<script>
import TodoItem from './TodoItem.vue';

export default {
  props: {
    todos: Array,
  },
  components: {
    TodoItem,
  },
  methods: {
    onDelete(id) {
      this.$emit('delete', id);
    },
    onComplete(id, completed) {
      this.$emit('complete', id, completed);
    }
  },
};
</script>

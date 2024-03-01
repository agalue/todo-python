<template>
  <v-list subheader two-line flat>
    <v-list-item-group>
      <TodoItem v-for="todo in todos" :key="todo.id" :todo="todo" @delete="onDelete" />
    </v-list-item-group>
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
  },
};
</script>

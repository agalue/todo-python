<template>
  <v-list-item>
    <v-list-item-content>
      <v-list-item-title>{{ todo.title }}</v-list-item-title>
      <v-list-item-subtitle>{{ new Date(todo.created_at) }}</v-list-item-subtitle>
    </v-list-item-content>
    <template v-slot:append>
      <v-btn color="danger" @click="onDelete()">Delete</v-btn>
    </template>
  </v-list-item>
</template>

<script>
export default {
  props: {
    todo: Object,
  },
  methods: {
    onDelete() {
      this.$emit('delete', this.todo.id);
    },
  },
};
</script>

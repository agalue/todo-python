<template>
  <v-list-item>
    <template v-slot:prepend>
      <v-list-item-action start>
        <v-checkbox v-model="completed" @click="onComplete"/>
      </v-list-item-action>
    </template>
    <v-list-item-title :class="{done: completed}">{{ todo.title }}</v-list-item-title>
    <v-list-item-subtitle>{{ new Date(todo.created_at) }}</v-list-item-subtitle>
    <template v-slot:append v-if="completed">
      <v-btn class="ma-2" color="red" icon="mdi-close" @click="onDelete"/>
    </template>
  </v-list-item>
</template>

<script>
export default {
  data() {
    return {
      completed: this.todo.completed,
    };
  },
  props: {
    todo: Object,
  },
  methods: {
    onDelete() {
      this.$emit('delete', this.todo.id);
    },
    onComplete() {
      this.$emit('complete', this.todo.id, !this.completed);
    }
  },
};
</script>

<style>
.done {
  text-decoration: line-through;
}
</style>
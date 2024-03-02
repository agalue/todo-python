<template>
  <v-text-field v-model="title" label="Type new your task and hit enter to add it" @keyup.enter="addTodo" />
</template>

<script setup>
import { ref, defineEmits } from 'vue';

const title = ref("")

const emit = defineEmits(['add'])

const addTodo = () => {
  emit('add', { title: title.value, priority: 3 })
  title.value = "";
}
</script>

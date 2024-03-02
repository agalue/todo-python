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

<script setup>
import { ref, defineProps, defineEmits, toRefs, onMounted } from 'vue';

const completed = ref(false)

const emit = defineEmits(['delete', 'complete'])

const props = defineProps({
  todo: Object
});

const { todo } = toRefs(props)

const onDelete = () => {
  emit('delete', todo.value.id);
};

const onComplete = () => {
  emit('complete', todo.value.id, !completed.value);
};

onMounted(() => completed.value = todo.value.completed)
</script>

<style>
.done {
  text-decoration: line-through;
}
</style>
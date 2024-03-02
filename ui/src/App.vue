<template>
  <v-app>
    <v-container>
      <v-row justify="center">
        <v-col>
          <v-card>
            <v-toolbar color="blue">
              <v-icon icon="mdi-checkbox-marked-circle-plus-outline" end></v-icon>
              <v-toolbar-title class="headline">TODO Application</v-toolbar-title>
            </v-toolbar>
            <AddTodoForm @add="onAdd" />
            <TodoList :todos="todos" @delete="onDelete" @complete="onComplete" />
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </v-app>
</template>

<script setup>
import TodoList from './components/TodoList.vue';
import AddTodoForm from './components/AddTodoForm.vue';

import { ref, onMounted } from 'vue';
import axios from 'axios';

const todos = ref([
  // {id: 100, title: "Learn VueJS 3", priority: 1, created_at: new Date().toString(), completed: false },
  // {id: 101, title: "Learn Vuetify", priority: 2, created_at: new Date().toString(), completed: true }
]);

const apiBaseURL = 'http://localhost:8080/todos/';

const fetchTodos = async () => {
  try {
    const response = await axios.get(apiBaseURL);
    todos.value = response.data;
  } catch (error) {
    console.error('Error fetching todos:', error);
  }
}

const onAdd = async (newTodo) => {
  try {
    const response = await axios.post(apiBaseURL, newTodo);
    todos.value.push(response.data);
  } catch (error) {
    console.error('Error adding todo:', error);
  }
}

const onDelete = async (id) => {
  try {
    await axios.delete(`${apiBaseURL}${id}`);
    todos.value = todos.value.filter((todo) => todo.id !== id);
  } catch (error) {
    console.error('Error deleting todo:', error);
  }
}

const onComplete = async (id, completed) => {
  try {
    await axios.put(`${apiBaseURL}${id}`, {completed});
    todos.value.find((todo) => todo.id == id).completed = completed
  } catch (error) {
    console.error('Error marking todo as complete:', error);
  }
}

onMounted(fetchTodos);
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
  margin-top: 60px;
}
</style>

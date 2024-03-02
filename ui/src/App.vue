<template>
  <v-app>
    <v-main>
      <v-theme-provider>
        <v-container>
          <v-row justify="center" class="ma-5">
            <v-col xs="12" sm="8">
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
      </v-theme-provider>
    </v-main>
  </v-app>
</template>

<script>
import TodoList from './components/TodoList.vue';
import AddTodoForm from './components/AddTodoForm.vue';
import axios from 'axios';

const apiBaseURL = 'http://localhost:8080/todos/'

export default {
  data() {
    return {
      todos: [
        // {id: 100, title: "Learn VueJS 3", priority: 1, created_at: new Date().toString(), completed: false },
        // {id: 101, title: "Learn Vuetify", priority: 2, created_at: new Date().toString(), completed: true }
      ],
    };
  },
  methods: {
    async fetchTodos() {
      try {
        const response = await axios.get(apiBaseURL);
        this.todos = response.data;
      } catch (error) {
        console.error('Error fetching todos:', error);
      }
    },
    async onAdd(newTodo) {
      try {
        const response = await axios.post(apiBaseURL, newTodo);
        this.todos.push(response.data);
      } catch (error) {
        console.error('Error adding todo:', error);
      }
    },
    async onDelete(id) {
      try {
        await axios.delete(`${apiBaseURL}${id}`);
        this.todos = this.todos.filter((todo) => todo.id !== id);
      } catch (error) {
        console.error('Error deleting todo:', error);
      }
    },
    async onComplete(id, completed) {
      try {
        await axios.put(`${apiBaseURL}${id}`, {completed});
        this.todos.find((todo) => todo.id == id).completed = completed
      } catch (error) {
        console.error('Error marking todo as complete:', error);
      }
    },
  },
  created() {
    this.fetchTodos();
  },
  components: {
    TodoList,
    AddTodoForm,
  },
};
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

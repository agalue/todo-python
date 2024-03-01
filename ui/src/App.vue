<template>
  <div id="app">
  <v-app>
    <v-main>
      <v-theme-provider theme="light">
        <v-container>
          <v-row justify="center" class="ma-5">
            <v-col xs="12" sm="8">
              <v-card>
                <v-toolbar color="blue">
                  <v-toolbar-title class="headline">TODO Application</v-toolbar-title>
                </v-toolbar>
                <AddTodoForm @add="onAdd" />
                <TodoList :todos="todos" @delete="onDelete" />
              </v-card>
            </v-col>
          </v-row>
        </v-container>
      </v-theme-provider>
    </v-main>
  </v-app>
</div>

</template>

<script>
import TodoList from './components/TodoList.vue';
import AddTodoForm from './components/AddTodoForm.vue';
import axios from 'axios';

const apiBaseURL = 'http://localhost:8080/todos/'

export default {
  data() {
    return {
      isDark: true,
      todos: [],
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

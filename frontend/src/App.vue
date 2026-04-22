<template>
  <div class="page">
    <div class="container">
      <header class="hero">
        <p class="eyebrow">Vue + FastAPI + MongoDB</p>
        <h1>Task Manager</h1>
        <p class="subtitle">
          A full-stack task app with proper frontend/backend separation.
        </p>
      </header>

      <section class="panel">
        <h2>Create a new task</h2>
        <TaskForm @create-task="handleCreateTask" />
      </section>

      <section class="panel">
        <div class="panel-header">
          <h2>Your tasks</h2>
          <button class="refresh-btn" @click="loadTasks" :disabled="loading">
            {{ loading ? 'Refreshing...' : 'Refresh' }}
          </button>
        </div>

        <div class="filters">
          <button
            :class="{ active: filter === 'all' }"
            @click="filter = 'all'"
          >
            All
          </button>
          <button
            :class="{ active: filter === 'pending' }"
            @click="filter = 'pending'"
          >
            Pending
          </button>
          <button
            :class="{ active: filter === 'completed' }"
            @click="filter = 'completed'"
          >
            Completed
          </button>
        </div>

        <p v-if="loading" class="info-message">Loading tasks...</p>
        <p v-if="error" class="error-message">{{ error }}</p>

        <TaskList
          v-if="!loading"
          :tasks="filteredTasks"
          @toggle-task="handleToggleTask"
          @delete-task="handleDeleteTask"
          @edit-task="handleEditTask"
        />
      </section>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue';
import TaskForm from './components/TaskForm.vue';
import TaskList from './components/TaskList.vue';
import {
  createTask,
  deleteTask,
  fetchTasks,
  updateTask
} from './services/api';

const tasks = ref([]);
const loading = ref(false);
const error = ref('');
const filter = ref('all');

const filteredTasks = computed(() => {
  if (filter.value === 'completed') {
    return tasks.value.filter((task) => task.completed);
  }

  if (filter.value === 'pending') {
    return tasks.value.filter((task) => !task.completed);
  }

  return tasks.value;
});

async function loadTasks() {
  loading.value = true;
  error.value = '';

  try {
    tasks.value = await fetchTasks();
  } catch (err) {
    error.value = err.message || 'An error occurred while loading tasks';
  } finally {
    loading.value = false;
  }
}

async function handleCreateTask(taskData) {
  error.value = '';

  try {
    const newTask = await createTask(taskData);
    tasks.value.unshift(newTask);
  } catch (err) {
    error.value = err.message || 'An error occurred while creating the task';
  }
}

async function handleToggleTask(task) {
  error.value = '';

  try {
    const updatedTask = await updateTask(task.id, {
      completed: !task.completed
    });

    tasks.value = tasks.value.map((currentTask) =>
      currentTask.id === task.id ? updatedTask : currentTask
    );
  } catch (err) {
    error.value = err.message || 'An error occurred while updating the task';
  }
}

async function handleEditTask(payload) {
  error.value = '';

  try {
    const updatedTask = await updateTask(payload.id, payload.data);

    tasks.value = tasks.value.map((currentTask) =>
      currentTask.id === payload.id ? updatedTask : currentTask
    );
  } catch (err) {
    error.value = err.message || 'An error occurred while editing the task';
  }
}

async function handleDeleteTask(taskId) {
  error.value = '';

  try {
    await deleteTask(taskId);
    tasks.value = tasks.value.filter((task) => task.id !== taskId);
  } catch (err) {
    error.value = err.message || 'An error occurred while deleting the task';
  }
}

onMounted(() => {
  loadTasks();
});
</script>

<style scoped>
:global(*) {
  box-sizing: border-box;
}

:global(body) {
  margin: 0;
  font-family: Arial, Helvetica, sans-serif;
  background: linear-gradient(180deg, #f8fbff 0%, #eef4ff 100%);
  color: #1f2937;
}

.page {
  min-height: 100vh;
  padding: 32px 16px;
}

.container {
  width: 100%;
  max-width: 900px;
  margin: 0 auto;
}

.hero {
  text-align: center;
  margin-bottom: 28px;
}

.eyebrow {
  text-transform: uppercase;
  letter-spacing: 0.08em;
  font-size: 0.85rem;
  color: #6b7280;
  margin-bottom: 8px;
}

h1 {
  font-size: 3rem;
  margin: 0 0 12px;
}

.subtitle {
  font-size: 1.05rem;
  color: #4b5563;
  max-width: 650px;
  margin: 0 auto;
}

.panel {
  background: white;
  border-radius: 18px;
  padding: 24px;
  margin-bottom: 20px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.06);
}

.panel h2 {
  margin-top: 0;
  margin-bottom: 18px;
}

.panel-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 12px;
  flex-wrap: wrap;
  margin-bottom: 18px;
}

.refresh-btn {
  background: #111827;
  color: white;
  border: none;
  border-radius: 10px;
  padding: 10px 14px;
  cursor: pointer;
}

.refresh-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.filters {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
  margin-bottom: 18px;
}

.filters button {
  border: 1px solid #d1d5db;
  background: white;
  padding: 10px 14px;
  border-radius: 999px;
  cursor: pointer;
}

.filters button.active {
  background: #2563eb;
  color: white;
  border-color: #2563eb;
}

.info-message {
  color: #374151;
}

.error-message {
  color: #b91c1c;
  background: #fee2e2;
  padding: 12px;
  border-radius: 10px;
  margin-bottom: 14px;
}

@media (max-width: 700px) {
  h1 {
    font-size: 2.2rem;
  }

  .panel {
    padding: 18px;
  }
}
</style>
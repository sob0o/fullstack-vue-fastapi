<template>
  <form class="task-form" @submit.prevent="handleSubmit">
    <div class="form-group">
      <input
        v-model="title"
        type="text"
        placeholder="Enter a task title"
        required
      />
    </div>

    <div class="form-group">
      <textarea
        v-model="description"
        placeholder="Enter a description (optional)"
        rows="3"
      ></textarea>
    </div>

    <button type="submit">Add Task</button>
  </form>
</template>

<script setup>
import { ref } from 'vue';

const emit = defineEmits(['create-task']);

const title = ref('');
const description = ref('');

function handleSubmit() {
  if (!title.value.trim()) {
    return;
  }

  emit('create-task', {
    title: title.value.trim(),
    description: description.value.trim(),
    completed: false
  });

  title.value = '';
  description.value = '';
}
</script>

<style scoped>
.task-form {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.form-group {
  width: 100%;
}

input,
textarea {
  width: 100%;
  padding: 12px 14px;
  border: 1px solid #d1d5db;
  border-radius: 10px;
  font-size: 1rem;
  outline: none;
  transition: border-color 0.2s ease;
}

input:focus,
textarea:focus {
  border-color: #2563eb;
}

button {
  align-self: flex-start;
  background: #2563eb;
  color: white;
  border: none;
  padding: 12px 18px;
  border-radius: 10px;
  cursor: pointer;
  font-size: 0.95rem;
}

button:hover {
  background: #1d4ed8;
}
</style>
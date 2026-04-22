<template>
  <div class="task-item" :class="{ completed: task.completed }">
    <div class="task-main">
      <template v-if="isEditing">
        <div class="edit-form">
          <input v-model="editedTitle" type="text" />
          <textarea v-model="editedDescription" rows="3"></textarea>

          <div class="edit-actions">
            <button class="save-btn" @click="saveEdit">Save</button>
            <button class="cancel-btn" @click="cancelEdit">Cancel</button>
          </div>
        </div>
      </template>

      <template v-else>
        <div class="task-header">
          <h3>{{ task.title }}</h3>
          <span class="status">
            {{ task.completed ? 'Completed' : 'Pending' }}
          </span>
        </div>

        <p v-if="task.description" class="description">
          {{ task.description }}
        </p>

        <small class="date">
          Created: {{ formatDate(task.created_at) }}
        </small>
      </template>
    </div>

    <div v-if="!isEditing" class="task-actions">
      <button class="toggle-btn" @click="$emit('toggle-task', task)">
        {{ task.completed ? 'Mark Pending' : 'Mark Done' }}
      </button>

      <button class="edit-btn" @click="startEdit">
        Edit
      </button>

      <button class="delete-btn" @click="$emit('delete-task', task.id)">
        Delete
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';

const props = defineProps({
  task: {
    type: Object,
    required: true
  }
});

const emit = defineEmits(['toggle-task', 'delete-task', 'edit-task']);

const isEditing = ref(false);
const editedTitle = ref('');
const editedDescription = ref('');

function formatDate(dateString) {
  return new Date(dateString).toLocaleString();
}

function startEdit() {
  editedTitle.value = props.task.title;
  editedDescription.value = props.task.description || '';
  isEditing.value = true;
}

function cancelEdit() {
  isEditing.value = false;
  editedTitle.value = '';
  editedDescription.value = '';
}

function saveEdit() {
  if (!editedTitle.value.trim()) {
    return;
  }

  emit('edit-task', {
    id: props.task.id,
    data: {
      title: editedTitle.value.trim(),
      description: editedDescription.value.trim()
    }
  });

  isEditing.value = false;
}
</script>

<style scoped>
.task-item {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 16px;
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 14px;
  padding: 18px;
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.04);
}

.task-item.completed {
  opacity: 0.9;
  border-left: 5px solid #10b981;
}

.task-main {
  flex: 1;
}

.task-header {
  display: flex;
  align-items: center;
  gap: 12px;
  flex-wrap: wrap;
}

.task-header h3 {
  margin: 0;
  font-size: 1.1rem;
}

.status {
  font-size: 0.85rem;
  padding: 4px 10px;
  border-radius: 999px;
  background: #eef2ff;
  color: #3730a3;
}

.description {
  margin: 10px 0;
  color: #4b5563;
}

.date {
  color: #6b7280;
}

.task-actions {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.task-actions button,
.edit-actions button {
  border: none;
  border-radius: 10px;
  padding: 10px 14px;
  cursor: pointer;
  font-size: 0.9rem;
}

.toggle-btn {
  background: #f3f4f6;
}

.edit-btn {
  background: #f59e0b;
  color: white;
}

.delete-btn {
  background: #ef4444;
  color: white;
}

.save-btn {
  background: #10b981;
  color: white;
}

.cancel-btn {
  background: #9ca3af;
  color: white;
}

.edit-form {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.edit-form input,
.edit-form textarea {
  width: 100%;
  padding: 12px 14px;
  border: 1px solid #d1d5db;
  border-radius: 10px;
  font-size: 1rem;
}

.edit-actions {
  display: flex;
  gap: 10px;
}

@media (max-width: 700px) {
  .task-item {
    flex-direction: column;
  }

  .task-actions {
    width: 100%;
    flex-direction: row;
    flex-wrap: wrap;
  }
}
</style>
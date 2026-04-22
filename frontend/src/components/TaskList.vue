<template>
  <div class="task-list">
    <p v-if="tasks.length === 0" class="empty-state">
      No tasks found for this filter.
    </p>

    <TaskItem
      v-for="task in tasks"
      :key="task.id"
      :task="task"
      @toggle-task="$emit('toggle-task', $event)"
      @delete-task="$emit('delete-task', $event)"
      @edit-task="$emit('edit-task', $event)"
    />
  </div>
</template>

<script setup>
import TaskItem from './TaskItem.vue';

defineProps({
  tasks: {
    type: Array,
    required: true
  }
});

defineEmits(['toggle-task', 'delete-task', 'edit-task']);
</script>

<style scoped>
.task-list {
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.empty-state {
  text-align: center;
  padding: 24px;
  color: #6b7280;
  background: #f9fafb;
  border: 1px dashed #d1d5db;
  border-radius: 12px;
}
</style>
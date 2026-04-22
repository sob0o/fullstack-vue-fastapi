const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

async function handleResponse(response, defaultErrorMessage) {
  if (!response.ok) {
    let errorMessage = defaultErrorMessage;

    try {
      const errorData = await response.json();
      errorMessage = errorData.detail || defaultErrorMessage;
    } catch {
      // Keep default message if response is not valid JSON
    }

    throw new Error(errorMessage);
  }

  return await response.json();
}

export async function fetchTasks() {
  const response = await fetch(`${API_BASE_URL}/tasks/`);
  return await handleResponse(response, 'Failed to fetch tasks');
}

export async function createTask(taskData) {
  const response = await fetch(`${API_BASE_URL}/tasks/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(taskData)
  });

  return await handleResponse(response, 'Failed to create task');
}

export async function updateTask(taskId, updatedData) {
  const response = await fetch(`${API_BASE_URL}/tasks/${taskId}`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(updatedData)
  });

  return await handleResponse(response, 'Failed to update task');
}

export async function deleteTask(taskId) {
  const response = await fetch(`${API_BASE_URL}/tasks/${taskId}`, {
    method: 'DELETE'
  });

  return await handleResponse(response, 'Failed to delete task');
}
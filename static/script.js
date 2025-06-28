document.addEventListener("DOMContentLoaded", function () {
  const taskForm = document.getElementById("taskForm");
  const taskList = document.getElementById("taskList");

  let tasks = JSON.parse(localStorage.getItem("tasks")) || [];
  renderTasks();

    const title = document.getElementById("title").value;
    const time = document.getElementById("time").value;
    const reminder = document.getElementById("reminder").checked;

    const task = { id: Date.now(), title, time, reminder };
    tasks.push(task);
    saveTasks();
    renderTasks();
    taskForm.reset();
  });

  function renderTasks() {
    taskList.innerHTML = "";
    tasks.forEach(task => {
      const li = document.createElement("li");
      li.innerHTML = `
        ⏰ <strong>${task.title}</strong> at ${new Date(task.time).toLocaleString()}
        <br/>
        <button onclick="deleteTask(${task.id})">🗑 Delete</button>
        <button onclick="editTask(${task.id})">✏️ Edit</button>
      `;
      taskList.appendChild(li);

      // Reminder popup
      if (task.reminder) {
        const delay = new Date(task.time).getTime() - Date.now();
        if (delay > 0) {
          setTimeout(() => {
            alert("🔔 Reminder: " + task.title);
          }, delay);
        }
      }
    });
  }

  function saveTasks() {
    localStorage.setItem("tasks", JSON.stringify(tasks));
  }

  window.deleteTask = function (id) {
    tasks = tasks.filter(task => task.id !== id);
    saveTasks();
    renderTasks();
  };

  window.editTask = function (id) {
    const task = tasks.find(t => t.id === id);
    if (task) {
      const newTitle = prompt("Edit Task Title:", task.title);
      const newTime = prompt("Edit Task Time:", task.time);

      if (newTitle && newTime) {
        task.title = newTitle;
        task.time = newTime;
        saveTasks();
        renderTasks();
      }
    }
  };
});

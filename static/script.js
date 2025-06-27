document.getElementById('taskForm').addEventListener('submit', function (e) {
  e.preventDefault();

  const title = document.getElementById('title').value;
  const time = new Date(document.getElementById('time').value).getTime();
  const reminder = document.getElementById('reminder').checked;

  const list = document.getElementById('taskList');
  const item = document.createElement('li');
  item.innerHTML = `⏰ <strong>${title}</strong> at ${new Date(time).toLocaleString()}`;
  list.appendChild(item);

  if (reminder) {
    const now = new Date().getTime();
    const delay = time - now;
    if (delay > 0) {
      setTimeout(() => {
        alert("🔔 Reminder: " + title);
      }, delay);
    }
  }

  document.getElementById('taskForm').reset();
});

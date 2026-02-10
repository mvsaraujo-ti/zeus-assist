/* ---------- THEME ---------- */
function toggleTheme() {
  document.body.classList.toggle("dark");
  localStorage.setItem(
    "theme",
    document.body.classList.contains("dark") ? "dark" : "light"
  );
}

document.addEventListener("DOMContentLoaded", () => {
  if (localStorage.getItem("theme") === "dark") {
    document.body.classList.add("dark");
  }

  const textarea = document.getElementById("question");
  textarea.addEventListener("keydown", (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      ask();
    }
  });
});

/* ---------- CHAT ---------- */
async function ask() {
  const textarea = document.getElementById("question");
  const question = textarea.value.trim();
  if (!question) return;

  addUserMessage(question);
  textarea.value = "";

  const typing = addZeusTyping();

  let answer = "Nenhuma resposta encontrada.";

  try {
    const response = await fetch("http://127.0.0.1:8000/api/v1/ask", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question }),
    });

    const data = await response.json();
    answer = data.answer || answer;
  } catch {
    typing.stop();
    typing.el.remove();
    addZeusMessage("Erro ao conectar com o backend.");
    return;
  }

  /* Delay artificial de ~1s */
  setTimeout(() => {
    typing.stop();
    typing.el.remove();
    addZeusMessageMarkdown(answer);
  }, 1000);
}

/* ---------- UI HELPERS ---------- */

function addUserMessage(text) {
  const chat = document.getElementById("chat");
  const div = document.createElement("div");
  div.className = "message user";
  div.textContent = text;
  chat.appendChild(div);
  scrollBottom();
}

function addZeusMessage(text) {
  const chat = document.getElementById("chat");
  const div = document.createElement("div");
  div.className = "message zeus";
  div.textContent = text;
  chat.appendChild(div);
  scrollBottom();
}

function addZeusMessageMarkdown(markdown) {
  const chat = document.getElementById("chat");
  const div = document.createElement("div");
  div.className = "message zeus";
  div.innerHTML = marked.parse(markdown);
  chat.appendChild(div);
  scrollBottom();
}

/* ---------- TYPING INDICATOR (3 DOTS) ---------- */

function addZeusTyping() {
  const chat = document.getElementById("chat");
  const div = document.createElement("div");
  div.className = "message zeus typing";
  div.textContent = "ZEUS está digitando";

  chat.appendChild(div);
  scrollBottom();

  let dots = 0;
  const interval = setInterval(() => {
    dots = (dots + 1) % 4;
    div.textContent = "ZEUS está digitando" + ".".repeat(dots);
  }, 400);

  return {
    el: div,
    stop() {
      clearInterval(interval);
    }
  };
}

/* ---------- UTILS ---------- */

function scrollBottom() {
  const chat = document.getElementById("chat");
  chat.scrollTop = chat.scrollHeight;
}

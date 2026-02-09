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

  const typingEl = addZeusTyping();

  try {
    const response = await fetch("http://127.0.0.1:8000/api/v1/ask", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question }),
    });

    const data = await response.json();

    typingEl.remove();
    addZeusMessageMarkdown(
      data.answer || "Nenhuma resposta encontrada."
    );
  } catch {
    typingEl.remove();
    addZeusMessage("Erro ao conectar com o backend.");
  }
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

/* ---------- TYPING INDICATOR ---------- */

function addZeusTyping() {
  const chat = document.getElementById("chat");
  const div = document.createElement("div");
  div.className = "message zeus typing";
  div.textContent = "ZEUS está digitando…";
  chat.appendChild(div);
  scrollBottom();
  return div;
}

/* ---------- UTILS ---------- */

function scrollBottom() {
  const chat = document.getElementById("chat");
  chat.scrollTop = chat.scrollHeight;
}

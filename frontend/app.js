async function ask() {
  const textarea = document.getElementById("question");
  const chat = document.getElementById("chat");

  const question = textarea.value.trim();
  if (!question) return;

  addMessage(question, "user");
  textarea.value = "";

  const loading = addMessage("Consultando o ZEUS…", "zeus");

  try {
    const response = await fetch("http://127.0.0.1:8000/api/v1/ask", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question }),
    });

    const data = await response.json();
    loading.textContent = data.answer || "Nenhuma resposta encontrada.";
  } catch (err) {
    loading.textContent = "Erro ao conectar com o backend.";
  }
}

function addMessage(text, type) {
  const chat = document.getElementById("chat");
  const div = document.createElement("div");

  div.className = `message ${type}`;
  div.textContent = text;

  chat.appendChild(div);
  chat.scrollTop = chat.scrollHeight;

  return div;
}

/* Enter envia | Shift+Enter quebra linha */
document.addEventListener("DOMContentLoaded", () => {
  const textarea = document.getElementById("question");

  textarea.addEventListener("keydown", (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      ask();
    }
  });
});

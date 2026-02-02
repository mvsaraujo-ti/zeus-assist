async function ask() {
  const question = document.getElementById("question").value;
  const answerBox = document.getElementById("answer");

  answerBox.textContent = "Consultando o ZEUS...";

  try {
    const response = await fetch("http://127.0.0.1:8000/api/v1/ask", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question }),
    });

    const data = await response.json();
    answerBox.textContent = data.answer;
  } catch (err) {
    answerBox.textContent = "Erro ao conectar com o backend.";
  }
}

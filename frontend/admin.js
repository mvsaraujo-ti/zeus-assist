const API = "http://127.0.0.1:8000/api/v1/admin/vault";

function authHeader() {
  const u = document.getElementById("user").value;
  const p = document.getElementById("pass").value;
  return "Basic " + btoa(`${u}:${p}`);
}

async function post(type, payload) {
  const res = await fetch(`${API}/${type}`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Authorization": authHeader()
    },
    body: JSON.stringify(payload)
  });

  const data = await res.json();
  document.getElementById("result").textContent =
    JSON.stringify(data, null, 2);
}

/* SYSTEM */
function saveSystem() {
  post("system", {
    id: sys("id"),
    name: sys("name"),
    keywords: split(sys("keywords")),
    description: sys("description")
  });
}

/* FLOW */
function saveFlow() {
  post("flow", {
    id: flow("id"),
    title: flow("title"),
    keywords: split(flow("keywords")),
    steps: splitLines(flow("steps"))
  });
}

/* CONTACT */
function saveContact() {
  post("contact", {
    id: ct("id"),
    name: ct("name"),
    keywords: split(ct("keywords")),
    channels: {
      email: ct("email"),
      phone: ct("phone"),
      ramal: ct("ramal")
    }
  });
}

/* Helpers */
const sys = f => document.getElementById(`sys-${f}`).value;
const flow = f => document.getElementById(`flow-${f}`).value;
const ct = f => document.getElementById(`ct-${f}`).value;

const split = v => v.split(",").map(x => x.trim()).filter(Boolean);
const splitLines = v => v.split("\n").map(x => x.trim()).filter(Boolean);

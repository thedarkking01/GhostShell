const input = document.getElementById("input");
const output = document.getElementById("output");
const terminal = document.getElementById("terminal");
const statusDot = document.getElementById("status-dot");
const statusText = document.getElementById("status-text");
const personalityLabel = document.getElementById("personality-label");

let personality = "friendly";
let history = [];

const PERSONALITIES = ["friendly", "cursed", "ancient"];
const TYPEWRITER_SPEED = { friendly: 22, cursed: 35, ancient: 18 };

document.body.classList.add("friendly");

const COMMANDS = {
  help: () => print(
    `Available commands: <span class="cmd">help</span>  <span class="cmd">clear</span>  ` +
    `<span class="cmd">summon</span>  <span class="cmd">story</span>  ` +
    `<span class="cmd">personality [friendly|cursed|ancient]</span>`
  ),
  clear: () => { output.innerHTML = ""; },
  summon: () => sendToGhost("You have just been summoned. Introduce yourself dramatically in one sentence."),
  story: () => sendToGhost("Tell a short, eerie two-sentence ghost story set inside a computer terminal."),
};

function print(html, cls = "ghost-line") {
  const div = document.createElement("div");
  div.className = cls;
  div.innerHTML = html;
  output.appendChild(div);
  output.scrollTop = output.scrollHeight;
  return div;
}

function printUser(text) {
  print(`<span class="prompt">ghostshell@localhost:~$</span> ${escapeHtml(text)}`, "user-line");
}

function escapeHtml(t) {
  return t.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
}

// typewriter effect — types text char by char into a div
function typewrite(div, text, speed) {
  return new Promise(resolve => {
    div.classList.add("typing");
    let i = 0;
    const tick = () => {
      div.textContent = `"${text.slice(0, i)}"`;
      output.scrollTop = output.scrollHeight;
      if (i++ < text.length) setTimeout(tick, speed);
      else { div.classList.remove("typing"); div.classList.add("reveal"); resolve(); }
    };
    tick();
  });
}

function triggerGlitch() {
  terminal.classList.remove("glitch");
  void terminal.offsetWidth; // reflow to restart animation
  terminal.classList.add("glitch");
  setTimeout(() => terminal.classList.remove("glitch"), 450);
}

async function checkHealth() {
  try {
    const res = await fetch("/health");
    const { status } = await res.json();
    statusDot.className = status;
    statusText.textContent = status === "online" ? "Ollama connected" : "Ollama offline";
  } catch {
    statusDot.className = "offline";
    statusText.textContent = "server unreachable";
  }
}

async function sendToGhost(message) {
  input.disabled = true;
  const thinking = print("", "ghost-line typing");

  try {
    const res = await fetch("/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message, personality, history }),
    });
    const { reply } = await res.json();
    thinking.remove();

    history.push({ role: "user", content: message });
    history.push({ role: "assistant", content: reply });
    if (history.length > 20) history = history.slice(-20);

    const replyDiv = print("", "ghost-line");
    await typewrite(replyDiv, reply, TYPEWRITER_SPEED[personality] ?? 22);
  } catch {
    thinking.remove();
    print("⚠ Lost contact with the ghost.", "error-line");
  } finally {
    input.disabled = false;
    input.focus();
  }
}

input.addEventListener("keydown", async (e) => {
  if (e.key !== "Enter" || input.disabled) return;
  const raw = input.value.trim();
  input.value = "";
  if (!raw) return;

  printUser(raw);
  const [cmd, ...args] = raw.toLowerCase().split(" ");

  if (cmd === "personality" && args[0]) {
    if (PERSONALITIES.includes(args[0])) {
      personality = args[0];
      document.body.className = personality;
      personalityLabel.textContent = `[ ${personality} ghost ]`;
      triggerGlitch();
      print(`Personality shifted to <span class="cmd">${personality}</span>.`);
    } else {
      print(`Unknown personality. Choose: ${PERSONALITIES.join(", ")}`, "error-line");
    }
    return;
  }

  if (COMMANDS[cmd]) { COMMANDS[cmd](); return; }

  await sendToGhost(raw);
});

checkHealth();
setInterval(checkHealth, 15000);

const socket = new WebSocket("ws://127.0.0.1:8000/ws");

const chat = document.getElementById("chat");

socket.onopen = () => {
    console.log("✅ WebSocket connected");
};

socket.onmessage = (event) => {

    console.log("📩 Message received:", event.data);

    const data = JSON.parse(event.data);

    addMessage(data.agent, data.message, "agent");
};

socket.onerror = (error) => {
    console.log("❌ WebSocket error:", error);
};

socket.onclose = () => {
    console.log("❌ WebSocket closed");
};

function sendMessage() {

    console.log("📤 Sending message");

    const input = document.getElementById("messageInput");

    const message = input.value;

    if (!message.trim()) return;

    addMessage("You", message, "user");

    socket.send(JSON.stringify({
        message: message
    }));

    input.value = "";
}

function addMessage(sender, text, cls) {

    const div = document.createElement("div");

    div.classList.add("message");
    div.classList.add(cls);

    const formattedText = marked.parse(text);

    div.innerHTML = `
        <div class="message-header">
            ${sender}
        </div>

        <div class="message-body">
            ${formattedText}
        </div>
    `;

    chat.appendChild(div);

    chat.scrollTop = chat.scrollHeight;
}
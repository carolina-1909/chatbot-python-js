document.getElementById("send-btn").addEventListener("click", async () => {
    const input = document.getElementById("user-input");
    const pregunta = input.value.trim();

    if (pregunta === "") return;

    const mensajesChat = document.getElementById("mensajes-chat");

    // Mostrar mensaje del usuario
    mensajesChat.innerHTML += `
        <div class="message user-message">
            <div class="message-content"><p>🙋‍♀️ ${pregunta}</p></div>
            <div class="message-time">🕒 ${new Date().toLocaleTimeString()}</div>
        </div>
    `;

    input.value = "";

    try {
        const response = await fetch("http://127.0.0.1:8000/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ pregunta: pregunta })
        });

        const data = await response.json();

        // Mostrar respuesta del bot
        mensajesChat.innerHTML += `
            <div class="message bot-message">
                <div class="message-content1">🤖 ${data.respuesta}</div>
                <div class="message-time">🕒 ${new Date().toLocaleTimeString()}</div>
            </div>
        `;

        mensajesChat.scrollTop = mensajesChat.scrollHeight;
    } catch (error) {
        mensajesChat.innerHTML += `
            <div class="message bot-message">
                <div class="message-content1"><p>❌ Hubo un error al obtener respuesta del servidor.</p></div>
                <div class="message-time">🕒 ${new Date().toLocaleTimeString()}</div>
            </div>
        `;
        console.error("❌ Error:", error);
    }
});


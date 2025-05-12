class ChatBot {
    constructor() {
        this.widget = null;
        this.messages = [];
        this.isOpen = false;
        this.createWidget();
        this.addEventListeners();
    }

    createWidget() {
        // Crear el widget del chatbot
        this.widget = document.createElement('div');
        this.widget.className = 'chatbot-widget';
        this.widget.innerHTML = `
            <div class="chatbot-button" title="Chat con VetCare">
                <i class="fas fa-comment"></i>
            </div>
            <div class="chatbot-container">
                <div class="chatbot-header">
                    <h3><i class="fas fa-paw"></i> VetCare Asistente</h3>
                    <button class="close-chat">
                        <i class="fas fa-times"></i>
                    </button>
                </div>
                <div class="chatbot-messages"></div>
                <div class="chatbot-input">
                    <input type="text" placeholder="Escribe tu mensaje...">
                    <button class="send-message">
                        <i class="fas fa-paper-plane"></i>
                    </button>
                </div>
            </div>
        `;
        document.body.appendChild(this.widget);

        // Agregar mensaje de bienvenida
        this.addMessage('bot', 'Hola 👋 ¿En qué puedo ayudarte hoy?', [
            'Quiero agendar una cita',
            'Precios de servicios',
            'Emergencia veterinaria',
            'Contactar a un veterinario'
        ]);
    }

    addEventListeners() {
        // Toggle del chat
        const chatButton = this.widget.querySelector('.chatbot-button');
        const closeButton = this.widget.querySelector('.close-chat');
        const container = this.widget.querySelector('.chatbot-container');
        const input = this.widget.querySelector('.chatbot-input input');
        const sendButton = this.widget.querySelector('.send-message');

        chatButton.addEventListener('click', () => this.toggleChat());
        closeButton.addEventListener('click', () => this.toggleChat());

        // Enviar mensaje
        const sendMessage = () => {
            const message = input.value.trim();
            if (message) {
                this.handleUserMessage(message);
                input.value = '';
            }
        };

        sendButton.addEventListener('click', sendMessage);
        input.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') sendMessage();
        });

        // Click en sugerencias
        const messagesContainer = this.widget.querySelector('.chatbot-messages');
        messagesContainer.addEventListener('click', (e) => {
            if (e.target.classList.contains('suggestion')) {
                this.handleUserMessage(e.target.textContent);
            }
        });
    }

    toggleChat() {
        const container = this.widget.querySelector('.chatbot-container');
        const button = this.widget.querySelector('.chatbot-button');
        this.isOpen = !this.isOpen;
        container.style.display = this.isOpen ? 'flex' : 'none';
        button.style.display = this.isOpen ? 'none' : 'flex';
        if (this.isOpen) {
            this.widget.querySelector('.chatbot-input input').focus();
        }
    }

    addMessage(type, text, suggestions = []) {
        const messagesContainer = this.widget.querySelector('.chatbot-messages');
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${type}-message`;
        
        // Agregar el texto del mensaje
        const textSpan = document.createElement('span');
        textSpan.textContent = text;
        messageDiv.appendChild(textSpan);

        // Agregar sugerencias si existen
        if (suggestions.length > 0) {
            const suggestionsDiv = document.createElement('div');
            suggestionsDiv.className = 'suggestions';
            suggestions.forEach(suggestion => {
                const button = document.createElement('button');
                button.className = 'suggestion';
                button.textContent = suggestion;
                suggestionsDiv.appendChild(button);
            });
            messageDiv.appendChild(suggestionsDiv);
        }

        messagesContainer.appendChild(messageDiv);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
        this.messages.push({ type, text });
    }

    handleUserMessage(message) {
        // Agregar mensaje del usuario
        this.addMessage('user', message);

        // Simular respuesta del bot
        setTimeout(() => {
            let response;
            let suggestions = [];

            // Respuestas basadas en palabras clave
            const messageLower = message.toLowerCase();
            if (messageLower.includes('cita') || messageLower.includes('agendar')) {
                response = 'Para agendar una cita, puedes llamarnos al +58 424-357-7054 o usar nuestro formulario de contacto.';
                suggestions = ['Ver horarios disponibles', 'Llamar ahora', 'Ir al formulario'];
            }
            else if (messageLower.includes('precio') || messageLower.includes('costo')) {
                response = 'Nuestros precios varían según el servicio:\n• Consulta general: $30\n• Vacunación: $25\n• Peluquería: $20';
                suggestions = ['Ver más servicios', 'Agendar cita', 'Hacer una consulta'];
            }
            else if (messageLower.includes('emergencia')) {
                response = '🚨 Para emergencias, llámanos inmediatamente al +58 424-357-7054. Atendemos 24/7.';
                suggestions = ['Llamar ahora', 'Ver dirección', 'Contactar WhatsApp'];
            }
            else if (messageLower.includes('contactar') || messageLower.includes('veterinario')) {
                response = 'Puedes contactar a nuestros veterinarios por:\n• Teléfono: +58 424-357-7054\n• Email: Thelarez24@gmail.com\n• WhatsApp: disponible 24/7';
                suggestions = ['Llamar', 'Enviar email', 'WhatsApp'];
            }
            else {
                response = 'Entiendo. ¿En qué más puedo ayudarte?';
                suggestions = ['Agendar cita', 'Ver servicios', 'Contactar veterinario'];
            }

            this.addMessage('bot', response, suggestions);
        }, 1000);
    }
}

// Inicializar el chatbot cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', () => {
    new ChatBot();
});

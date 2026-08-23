// ========================================
// MyAI — ChatGPT Clone Frontend Logic
// ========================================

// State
let chatHistory = [];
let currentChatId = null;
let isStreaming = false;

// DOM Elements
const chatContainer = document.getElementById('chatContainer');
const messagesDiv = document.getElementById('messages');
const welcomeScreen = document.getElementById('welcomeScreen');
const messageInput = document.getElementById('messageInput');
const sendBtn = document.getElementById('sendBtn');
const chatHistoryDiv = document.getElementById('chatHistory');

// ===== CHAT FUNCTIONS =====

function newChat() {
    currentChatId = Date.now().toString();
    messagesDiv.innerHTML = '';
    messagesDiv.classList.remove('active');
    welcomeScreen.style.display = 'flex';
    messageInput.value = '';
    messageInput.focus();
    
    // Close sidebar on mobile
    closeSidebar();
}

function sendSuggestion(text) {
    messageInput.value = text;
    sendMessage();
}

async function sendMessage() {
    const message = messageInput.value.trim();
    if (!message || isStreaming) return;

    // Hide welcome screen, show messages
    welcomeScreen.style.display = 'none';
    messagesDiv.classList.add('active');

    // Add user message
    addMessage('user', message);
    messageInput.value = '';
    messageInput.style.height = 'auto';

    // Save to history
    if (!currentChatId) {
        currentChatId = Date.now().toString();
    }
    saveChatHistory(message);

    // Show typing indicator
    const typingDiv = addTypingIndicator();

    // Disable input
    isStreaming = true;
    sendBtn.disabled = true;

    try {
        // Call backend API
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                message: message,
                chat_id: currentChatId
            })
        });

        // Remove typing indicator
        typingDiv.remove();

        if (response.ok) {
            const data = await response.json();
            // Add AI message with streaming effect
            await addMessageWithStreaming('ai', data.reply);
        } else {
            addMessage('ai', '⚠️ Oops! Kuch gadbad ho gayi. Phir se try karo.');
        }
    } catch (error) {
        typingDiv.remove();
        addMessage('ai', '⚠️ Server se connect nahi ho pa raha. Check karo ki backend chal raha hai.');
        console.error('Error:', error);
    }

    // Re-enable input
    isStreaming = false;
    sendBtn.disabled = false;
    messageInput.focus();
}

function addMessage(type, text) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${type}`;
    
    const avatar = type === 'user' ? '👤' : '🤖';
    
    messageDiv.innerHTML = `
        <div class="message-content">
            <div class="message-avatar">${avatar}</div>
            <div class="message-text">${formatText(text)}</div>
        </div>
    `;
    
    messagesDiv.appendChild(messageDiv);
    scrollToBottom();
    return messageDiv;
}

async function addMessageWithStreaming(type, text) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${type}`;
    
    const avatar = type === 'user' ? '👤' : '🤖';
    
    messageDiv.innerHTML = `
        <div class="message-content">
            <div class="message-avatar">${avatar}</div>
            <div class="message-text streaming"></div>
        </div>
    `;
    
    messagesDiv.appendChild(messageDiv);
    const textDiv = messageDiv.querySelector('.message-text');
    
    // Streaming effect - character by character
    let displayText = '';
    const chars = text.split('');
    const speed = Math.max(15, Math.min(40, 1500 / chars.length)); // Adaptive speed
    
    for (let i = 0; i < chars.length; i++) {
        displayText += chars[i];
        textDiv.innerHTML = formatText(displayText);
        textDiv.classList.add('streaming');
        scrollToBottom();
        await sleep(speed);
    }
    
    // Remove streaming cursor
    textDiv.classList.remove('streaming');
    return messageDiv;
}

function addTypingIndicator() {
    const div = document.createElement('div');
    div.className = 'message ai';
    div.id = 'typingIndicator';
    div.innerHTML = `
        <div class="message-content">
            <div class="message-avatar">🤖</div>
            <div class="message-text">
                <div class="typing-indicator">
                    <span></span>
                    <span></span>
                    <span></span>
                </div>
            </div>
        </div>
    `;
    messagesDiv.appendChild(div);
    scrollToBottom();
    return div;
}

// ===== UTILITY FUNCTIONS =====

function formatText(text) {
    // Basic markdown-like formatting
    text = text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
    text = text.replace(/\*(.*?)\*/g, '<em>$1</em>');
    text = text.replace(/`(.*?)`/g, '<code>$1</code>');
    text = text.replace(/\n/g, '<br>');
    return text;
}

function scrollToBottom() {
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

function autoResize(textarea) {
    textarea.style.height = 'auto';
    textarea.style.height = Math.min(textarea.scrollHeight, 120) + 'px';
}

function handleKeyDown(event) {
    if (event.key === 'Enter' && !event.shiftKey) {
        event.preventDefault();
        sendMessage();
    }
}

// ===== SIDEBAR FUNCTIONS =====

function toggleSidebar() {
    const sidebar = document.getElementById('sidebar');
    sidebar.classList.toggle('open');
    
    // Add/remove overlay
    let overlay = document.querySelector('.sidebar-overlay');
    if (!overlay) {
        overlay = document.createElement('div');
        overlay.className = 'sidebar-overlay';
        overlay.onclick = closeSidebar;
        document.body.appendChild(overlay);
    }
    overlay.classList.toggle('active');
}

function closeSidebar() {
    const sidebar = document.getElementById('sidebar');
    sidebar.classList.remove('open');
    const overlay = document.querySelector('.sidebar-overlay');
    if (overlay) overlay.classList.remove('active');
}

// ===== THEME TOGGLE =====

function toggleTheme() {
    const body = document.body;
    const btn = document.querySelector('.theme-btn');
    
    if (body.getAttribute('data-theme') === 'light') {
        body.removeAttribute('data-theme');
        btn.textContent = '🌙';
        localStorage.setItem('theme', 'dark');
    } else {
        body.setAttribute('data-theme', 'light');
        btn.textContent = '☀️';
        localStorage.setItem('theme', 'light');
    }
}

// Load saved theme
function loadTheme() {
    const saved = localStorage.getItem('theme');
    if (saved === 'light') {
        document.body.setAttribute('data-theme', 'light');
        document.querySelector('.theme-btn').textContent = '☀️';
    }
}

// ===== CHAT HISTORY =====

function saveChatHistory(firstMessage) {
    let history = JSON.parse(localStorage.getItem('chatHistory') || '[]');
    
    // Check if current chat already exists
    const existing = history.find(h => h.id === currentChatId);
    if (!existing) {
        history.unshift({
            id: currentChatId,
            title: firstMessage.substring(0, 30) + (firstMessage.length > 30 ? '...' : ''),
            timestamp: Date.now()
        });
        
        // Keep only last 20 chats
        history = history.slice(0, 20);
        localStorage.setItem('chatHistory', JSON.stringify(history));
        renderChatHistory();
    }
}

function renderChatHistory() {
    const history = JSON.parse(localStorage.getItem('chatHistory') || '[]');
    chatHistoryDiv.innerHTML = '';
    
    history.forEach(chat => {
        const item = document.createElement('div');
        item.className = `chat-history-item ${chat.id === currentChatId ? 'active' : ''}`;
        item.textContent = chat.title;
        item.onclick = () => loadChat(chat.id);
        chatHistoryDiv.appendChild(item);
    });
}

function loadChat(chatId) {
    // For now, just start a new view (full history would need backend storage)
    currentChatId = chatId;
    renderChatHistory();
    closeSidebar();
}

// ===== INITIALIZATION =====

document.addEventListener('DOMContentLoaded', () => {
    loadTheme();
    renderChatHistory();
    messageInput.focus();
});

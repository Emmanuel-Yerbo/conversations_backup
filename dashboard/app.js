let conversations = [];
let activeConvoId = null;

// Initialize Dashboard
document.addEventListener('DOMContentLoaded', () => {
    fetchConversations();
    setupSearch();
});

// Fetch main index
async function fetchConversations() {
    try {
        const response = await fetch('../data/conversations.json');
        if (!response.ok) throw new Error('Failed to load conversations index');
        conversations = await response.ok ? await response.json() : [];
        renderSidebar(conversations);
    } catch (error) {
        console.error('Error fetching conversations:', error);
        document.getElementById('conversation-list').innerHTML = `
            <div style="text-align: center; padding: 20px; color: #f43f5e;">
                Error loading conversation list. Please run the sync script first.
            </div>
        `;
    }
}

// Render conversation list in sidebar
function renderSidebar(list) {
    const listContainer = document.getElementById('conversation-list');
    listContainer.innerHTML = '';
    
    if (list.length === 0) {
        listContainer.innerHTML = '<div style="text-align: center; padding: 20px; color: var(--text-secondary);">No conversations found</div>';
        return;
    }
    
    list.forEach(convo => {
        const item = document.createElement('div');
        item.className = `conversation-item ${convo.id === activeConvoId ? 'active' : ''}`;
        item.onclick = () => selectConversation(convo.id);
        
        const dateStr = convo.updated_at.split('T')[0];
        
        item.innerHTML = `
            <div class="convo-title" title="${convo.title}">${convo.title}</div>
            <div class="convo-summary">${convo.summary || 'No summary available.'}</div>
            <div class="convo-meta">
                <div class="convo-date">
                    <svg style="width:12px;height:12px;fill:currentColor;" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M9 11H7v2h2v-2zm4 0h-2v2h2v-2zm4 0h-2v2h2v-2zm2-7h-1V2h-2v2H8V2H6v2H5c-1.11 0-1.99.9-1.99 2L3 20c0 1.1.89 2 2 2h14c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zm0 16H5V9h14v11z"/></svg>
                    <span>${dateStr}</span>
                </div>
                <span class="badge">${convo.message_count} turns</span>
            </div>
        `;
        listContainer.appendChild(item);
    });
}

// Select a conversation and load details
async function selectConversation(id) {
    activeConvoId = id;
    
    // Update active class in sidebar
    const items = document.querySelectorAll('.conversation-item');
    items.forEach(item => item.classList.remove('active'));
    
    // Refresh sidebar highlighting
    const activeItem = Array.from(items).find(item => item.innerHTML.includes(id));
    if (activeItem) activeItem.classList.add('active');
    
    // Show loading state
    document.getElementById('empty-state').style.display = 'none';
    document.getElementById('chat-header').style.display = 'none';
    document.getElementById('chat-messages').style.display = 'flex';
    document.getElementById('chat-messages').innerHTML = '<div style="text-align:center;padding:40px;color:var(--text-secondary);">Loading conversation transcript...</div>';
    
    try {
        const response = await fetch(`../data/detail/${id}.json`);
        if (!response.ok) throw new Error('Failed to load conversation details');
        const detail = await response.json();
        
        renderChat(detail);
    } catch (error) {
        console.error('Error details:', error);
        document.getElementById('chat-messages').innerHTML = `
            <div style="text-align:center;padding:40px;color:#f43f5e;">
                Error loading conversation detail. Ensure files have been generated correctly.
            </div>
        `;
    }
}

// Render messages in chat view
function renderChat(detail) {
    const meta = detail.metadata;
    const turns = detail.turns;
    
    // Render Header
    document.getElementById('chat-header').style.display = 'flex';
    document.getElementById('active-title').innerText = meta.title;
    document.getElementById('active-meta').innerText = `Last modified: ${meta.updated_at.split('T')[0]} | Messages: ${meta.message_count} | ID: ${meta.id}`;
    
    // Link raw Markdown file
    document.getElementById('view-raw-md').href = `../data/detail/${meta.id}.md`;
    
    // Render Messages
    const chatContainer = document.getElementById('chat-messages');
    chatContainer.innerHTML = '';
    
    turns.forEach(turn => {
        const wrapper = document.createElement('div');
        wrapper.className = `message-wrapper ${turn.role}`;
        
        const timestamp = turn.time ? turn.time.split('T')[0] + ' ' + turn.time.split('T')[1].substring(0,5) : '';
        const roleLabel = turn.role === 'user' ? 'Emmanuel (User)' : 'Gemini / Antigravity';
        
        let toolHtml = '';
        if (turn.tools && turn.tools.length > 0) {
            toolHtml = `
                <details class="tools-details">
                    <summary>🛠️ Executed ${turn.tools.length} Tools</summary>
                    <ul>
                        ${turn.tools.map(tool => `<li><strong>${tool.name}</strong>: <code>${escapeHtml(tool.target)}</code></li>`).join('')}
                    </ul>
                </details>
            `;
        }
        
        wrapper.innerHTML = `
            <div class="message-meta">
                <span><strong>${roleLabel}</strong></span>
                <span>${timestamp}</span>
            </div>
            <div class="message-bubble">
                ${toolHtml}
                ${parseMarkdown(turn.content)}
            </div>
        `;
        
        chatContainer.appendChild(wrapper);
    });
    
    // Scroll to top of chat
    chatContainer.scrollTop = 0;
}

// Setup search filter
function setupSearch() {
    const searchInput = document.getElementById('search-input');
    searchInput.addEventListener('input', (e) => {
        const query = e.target.value.toLowerCase().trim();
        if (!query) {
            renderSidebar(conversations);
            return;
        }
        
        const filtered = conversations.filter(convo => 
            convo.title.toLowerCase().includes(query) || 
            (convo.summary && convo.summary.toLowerCase().includes(query)) ||
            convo.id.toLowerCase().includes(query)
        );
        renderSidebar(filtered);
    });
}

// Simple HTML Escaping
function escapeHtml(text) {
    if (!text) return '';
    return text
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}

// Basic Custom Markdown Parser
function parseMarkdown(text) {
    if (!text) return '';
    
    // Escape HTML first to prevent XSS/broken layouts, but preserve code blocks
    let html = escapeHtml(text);
    
    // 1. Code blocks (```lang ... ```)
    html = html.replace(/```(?:[a-zA-Z0-9]*)\n([\s\S]*?)```/g, (match, p1) => {
        return `<pre><code>${p1}</code></pre>`;
    });
    
    // 2. Inline code (`code`)
    html = html.replace(/`([^`]+)`/g, '<code>$1</code>');
    
    // 3. Headers
    html = html.replace(/^### (.*$)/gim, '<h3>$1</h3>');
    html = html.replace(/^## (.*$)/gim, '<h2>$1</h2>');
    html = html.replace(/^# (.*$)/gim, '<h1>$1</h1>');
    
    // 4. Bold and Italic
    html = html.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');
    html = html.replace(/\*([^*]+)\*/g, '<em>$1</em>');
    
    // 5. Blockquotes
    html = html.replace(/^\&gt;\s+(.*$)/gim, '<blockquote>$1</blockquote>');
    
    // 6. Unordered lists
    // First format list items
    html = html.replace(/^\-\s+(.*$)/gim, '<li>$1</li>');
    
    // 7. Paragraphs - split by double newline
    const paragraphs = html.split(/\n\n+/);
    html = paragraphs.map(p => {
        p = p.trim();
        if (!p) return '';
        // If it starts with an HTML block element, return as is
        if (p.startsWith('<h') || p.startsWith('<pre') || p.startsWith('<blockquote') || p.startsWith('<li') || p.startsWith('<details')) {
            return p;
        }
        return `<p>${p.replace(/\n/g, '<br>')}</p>`;
    }).join('\n');
    
    return html;
}

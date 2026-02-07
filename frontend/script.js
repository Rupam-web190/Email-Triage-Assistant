const API_URL = 'http://127.0.0.1:5000';

// State
let currentUser = {
    name: 'John Manager',
    handle: '@john_m',
    avatar: 'JM'
};

// Pagination State
let currentPage = 1;
let isLoadingMore = false;
let hasMorePosts = true;

// Mode Switching
function switchMode(mode) {
    // Update Tabs
    document.querySelectorAll('.nav-item').forEach(tab => {
        tab.classList.remove('active');
        if (tab.getAttribute('data-mode') === mode) {
            tab.classList.add('active');
        }
    });

    // Update View
    document.querySelectorAll('.view-section').forEach(view => {
        view.classList.add('hidden');
    });
    
    const targetView = document.getElementById(`view-${mode}`);
    if (targetView) {
        targetView.classList.remove('hidden');
    } else {
        console.warn(`View view-${mode} not found`);
    }

    // Load data if needed
    if (mode === 'single') loadFeed(); // Reload/Check feed
    if (mode === 'dashboard') loadDashboard();
    if (mode === 'reply') loadRecentThreadsForReply();
}

// Loading Spinner
function toggleLoading(show) {
    const el = document.getElementById('loading');
    if (show) el.classList.remove('hidden');
    else el.classList.add('hidden');
}

// File Upload Trigger
function triggerFileUpload() {
    document.getElementById('eml-upload').click();
}

// Handle File Upload
async function handleFileUpload(input) {
    if (input.files && input.files[0]) {
        const file = input.files[0];
        
        // Client-side Validation
        if (!file.name.toLowerCase().endsWith('.eml')) {
            alert('Invalid file format. Please upload a .eml file.');
            input.value = ''; 
            return;
        }
        
        if (file.size > 10 * 1024 * 1024) { // 10MB
            alert('File too large. Maximum size is 10MB.');
            input.value = '';
            return;
        }

        toggleLoading(true);

        try {
            const formData = new FormData();
            formData.append('file', file);

            const response = await fetch(`${API_URL}/triage`, {
                method: 'POST',
                body: formData 
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || 'Server processing failed');
            }
            
            // Add to Feed
            addPostToFeed(data);
            
            // Show success notification (simulated)
            showNotification('Analysis Complete', `Processed "${data.subject}"`);

        } catch (error) {
            console.error('Upload Error:', error);
            alert(`Failed to process email: ${error.message}`);
        } finally {
            toggleLoading(false);
            input.value = ''; 
        }
    }
}

// Render Result as Post
function addPostToFeed(data, atEnd = false) {
    const feedStream = document.getElementById('feed-stream');
    
    const post = document.createElement('div');
    post.className = 'post-card';
    
    // Determine badge color based on priority
    let badgeClass = 'badge-info';
    if (data.priority >= 4) badgeClass = 'badge-urgent';
    else if (data.priority >= 2) badgeClass = 'badge-warning';

    // Parse date if available
    let timeAgo = 'Just now';
    if (data.date) {
        try {
            const date = new Date(data.date);
            const now = new Date();
            const diff = Math.floor((now - date) / 1000); // seconds
            if (diff < 60) timeAgo = 'Just now';
            else if (diff < 3600) timeAgo = `${Math.floor(diff/60)}m ago`;
            else if (diff < 86400) timeAgo = `${Math.floor(diff/3600)}h ago`;
            else timeAgo = date.toLocaleDateString();
        } catch(e) {}
    }
    
    post.innerHTML = `
        <div class="post-header">
            <div class="user-info">
                <div class="avatar" style="background: var(--primary-color)">${getInitials(data.sender)}</div>
                <div class="user-meta">
                    <h4>${escapeHtml(data.sender)}</h4>
                    <span>${timeAgo}</span>
                </div>
            </div>
            <div style="display: flex; gap: 0.5rem;">
                <span class="badge ${badgeClass}">Priority ${data.priority}</span>
                ${data.category ? `<span class="badge badge-action">${data.category}</span>` : ''}
            </div>
        </div>
        <div class="post-content">
            <h3>${escapeHtml(data.subject)}</h3>
            <p>${escapeHtml(data.summary)}</p>
            
            ${data.meeting_info?.is_meeting ? `
            <div class="meeting-card">
                <div style="font-weight: 600;">📅 Meeting Detected</div>
                <div>${data.meeting_info.details || 'Check details'}</div>
            </div>
            ` : ''}
            
            <div class="stats-row">
                <span>📉 Compressed by ${data.compression_ratio || '0%'}</span>
                <span>⏱️ Triage time: < 1s</span>
            </div>
        </div>
        <div class="post-actions">
            <div class="action-btn" onclick="toggleLike(this)">❤️ Like</div>
            <div class="action-btn" onclick="toggleComments(this)">💬 Comment</div>
            <div class="action-btn" onclick="sharePost('${escapeHtml(data.subject)}')">↪️ Share</div>
            <div class="action-btn" style="margin-left: auto;" onclick="archivePost(this)">📥 Archive</div>
        </div>
        <div class="comments-section hidden">
            <div class="comment-input-row">
                <div class="avatar is-small">${currentUser.avatar}</div>
                <input type="text" placeholder="Write a comment..." onkeypress="handleComment(event, this)">
            </div>
        </div>
    `;

    if (atEnd) {
        feedStream.appendChild(post);
    } else {
        // Insert after the "Create Post" card if it exists, otherwise prepend
        // Assuming feedStream might have a "create post" input at top later, but for now just prepend
        feedStream.insertBefore(post, feedStream.firstChild);
    }
}

// Helper: Get Initials
function getInitials(name) {
    if (!name) return '?';
    return name.split(' ').map(n => n[0]).join('').substring(0, 2).toUpperCase();
}

// Helper: Escape HTML
function escapeHtml(unsafe) {
    if (typeof unsafe !== 'string') return '';
    return unsafe
         .replace(/&/g, "&amp;")
         .replace(/</g, "&lt;")
         .replace(/>/g, "&gt;")
         .replace(/"/g, "&quot;")
         .replace(/'/g, "&#039;");
}

// Social Interactions
function toggleLike(btn) {
    if (btn.classList.contains('active')) {
        btn.classList.remove('active');
        btn.style.color = 'inherit';
    } else {
        btn.classList.add('active');
        btn.style.color = '#ef4444'; // Red
        
        // Animation effect
        btn.animate([
            { transform: 'scale(1)' },
            { transform: 'scale(1.2)' },
            { transform: 'scale(1)' }
        ], { duration: 200 });
    }
}

function toggleComments(btn) {
    const card = btn.closest('.post-card');
    const section = card.querySelector('.comments-section');
    section.classList.toggle('hidden');
    if (!section.classList.contains('hidden')) {
        section.querySelector('input').focus();
    }
}

function handleComment(event, input) {
    if (event.key === 'Enter' && input.value.trim()) {
        const commentText = input.value;
        const section = input.closest('.comments-section');
        
        const commentDiv = document.createElement('div');
        commentDiv.className = 'comment';
        commentDiv.innerHTML = `
            <span class="comment-user">You</span>
            <span class="comment-text">${escapeHtml(commentText)}</span>
        `;
        
        section.insertBefore(commentDiv, section.firstChild.nextSibling); // Insert after input
        input.value = '';
    }
}

function sharePost(subject) {
    alert(`Shared "${subject}" to your network!`);
}

function archivePost(btn) {
    const card = btn.closest('.post-card');
    card.style.opacity = '0';
    setTimeout(() => {
        card.remove();
        showNotification('Archived', 'Post moved to archive.');
    }, 300);
}

// Notifications
function showNotification(title, message) {
    // Check if container exists
    let container = document.getElementById('notification-container');
    if (!container) {
        container = document.createElement('div');
        container.id = 'notification-container';
        document.body.appendChild(container);
    }
    
    const notif = document.createElement('div');
    notif.className = 'notification-toast';
    notif.innerHTML = `
        <div style="font-weight: 600;">${title}</div>
        <div style="font-size: 0.875rem;">${message}</div>
    `;
    
    container.appendChild(notif);
    
    // Remove after 3s
    setTimeout(() => {
        notif.style.opacity = '0';
        notif.style.transform = 'translateY(20px)';
        setTimeout(() => notif.remove(), 300);
    }, 3000);
}

// Batch Processing
async function runBatchProcess() {
    toggleLoading(true);
    try {
        const response = await fetch(`${API_URL}/batch`, { method: 'POST' });
        const data = await response.json();
        
        const container = document.getElementById('batch-results');
        container.innerHTML = ''; // Clear previous
        
        // Create a summary header
        const summary = document.createElement('div');
        summary.className = 'post-card';
        summary.innerHTML = `
            <h3>Batch Analysis Complete</h3>
            <p>Processed ${data.processed_count} emails in ${data.time_taken}s</p>
        `;
        container.appendChild(summary);
        
        data.results.forEach(thread => {
            const div = document.createElement('div');
            div.className = 'post-card';
            div.style.padding = '1rem';
            div.innerHTML = `
                <div style="display:flex; justify-content:space-between;">
                    <strong>${escapeHtml(thread.sender)}</strong>
                    <span class="badge badge-urgent">P${thread.priority}</span>
                </div>
                <div>${escapeHtml(thread.subject)}</div>
                <div style="color:var(--text-secondary); font-size:0.875rem;">${escapeHtml(thread.summary)}</div>
            `;
            container.appendChild(div);
        });
        
    } catch (error) {
        console.error('Batch error:', error);
        alert('Batch process failed');
    } finally {
        toggleLoading(false);
    }
}

// Auto-Reply (Drafts)
async function loadRecentThreadsForReply() {
    // Simulated data for now as endpoint might not return what we expect
    // In real app, fetch from backend
    const container = document.getElementById('reply-thread-list');
    container.innerHTML = '<div class="post-card"><p>Loading conversations...</p></div>';
    
    setTimeout(() => {
        container.innerHTML = '';
        const mockThreads = [
            { id: 1, subject: 'Project Deadline', sender: 'Alice', body: 'When is this due?' },
            { id: 2, subject: 'Lunch?', sender: 'Bob', body: 'Are you free for lunch?' }
        ];
        
        mockThreads.forEach(thread => {
            const div = document.createElement('div');
            div.className = 'post-card';
            div.innerHTML = `
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <h3>${thread.subject}</h3>
                    <button class="btn-primary" onclick="generateReplyFor('${thread.id}')">Draft Reply</button>
                </div>
                <p>${thread.body}</p>
                <div id="reply-area-${thread.id}" class="hidden" style="margin-top:1rem; border-top:1px solid var(--border-color); padding-top:1rem;">
                    <textarea class="post-input" rows="4">Hi ${thread.sender},\n\nThanks for your email.</textarea>
                    <button class="btn-primary" style="margin-top:0.5rem" onclick="alert('Sent!')">Send</button>
                </div>
            `;
            container.appendChild(div);
        });
    }, 500);
}

function generateReplyFor(id) {
    document.getElementById(`reply-area-${id}`).classList.remove('hidden');
}

// Dashboard
async function loadDashboard() {
    // Simulated
    document.getElementById('dash-processed').innerText = '1,243';
    document.getElementById('dash-saved').innerText = '12h';
}

// Feed Loading
async function loadFeed() {
    if (isLoadingMore || !hasMorePosts) return;
    
    // If it's the first page and we already have content (e.g. from manual upload), maybe don't reload?
    // For now, let's just append if it's page 1 and empty, or page > 1
    const feedStream = document.getElementById('feed-stream');
    if (currentPage === 1 && feedStream.children.length > 0) {
        // Already populated, might be manual uploads. 
        // In a real app we'd manage state better.
    }

    isLoadingMore = true;
    if (currentPage === 1) toggleLoading(true);

    try {
        const response = await fetch(`${API_URL}/threads?page=${currentPage}&limit=5`);
        if (!response.ok) throw new Error('Failed to load feed');
        
        const threads = await response.json();
        
        if (threads.length === 0) {
            hasMorePosts = false;
            if (currentPage === 1) {
                feedStream.innerHTML = '<div class="post-card" style="text-align:center">No emails found.</div>';
            }
        } else {
            threads.forEach(thread => {
                addPostToFeed(thread, true); // Append to end
            });
            currentPage++;
        }
    } catch (error) {
        console.error('Feed error:', error);
        showNotification('Error', 'Failed to load feed');
    } finally {
        isLoadingMore = false;
        toggleLoading(false);
    }
}

// Infinite Scroll Listener
window.addEventListener('scroll', () => {
    // Check if we are near bottom (within 200px)
    if ((window.innerHeight + window.scrollY) >= document.body.offsetHeight - 200) {
        if (!isLoadingMore && hasMorePosts && document.getElementById('view-single').classList.contains('hidden') === false) {
            loadFeed();
        }
    }
});

// Init
document.addEventListener('DOMContentLoaded', () => {
    // Initial welcome
    console.log('App Initialized');
    
    // Load initial feed
    loadFeed();
});

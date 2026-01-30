// Theme Toggle Logic
const htmlElement = document.documentElement;

// Initialize theme from localStorage or default to dark
const savedTheme = localStorage.getItem('theme') || 'dark';
htmlElement.setAttribute('data-theme', savedTheme);

function toggleTheme() {
    const currentTheme = htmlElement.getAttribute('data-theme');
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';

    htmlElement.setAttribute('data-theme', newTheme);
    localStorage.setItem('theme', newTheme);
    updateThemeIcon(newTheme);
}

function updateThemeIcon(theme) {
    const themeToggle = document.getElementById('themeToggle');
    if (!themeToggle) return;
    const icon = themeToggle.querySelector('i');
    if (theme === 'dark') {
        icon.className = 'fas fa-sun';
    } else {
        icon.className = 'fas fa-moon';
    }
}

document.addEventListener('DOMContentLoaded', () => {
    fetchJobs();
    fetchPrep();
    initModal();

    // Setup theme toggle button if it exists
    const themeToggle = document.getElementById('themeToggle');
    if (themeToggle) {
        themeToggle.addEventListener('click', toggleTheme);
        updateThemeIcon(htmlElement.getAttribute('data-theme'));
    }
});

function initModal() {
    const modal = document.getElementById('loginModal');
    const btn = document.getElementById('loginBtn');
    const span = document.getElementsByClassName('close-modal')[0];

    btn.onclick = () => {
        modal.style.display = 'flex';
        document.body.style.overflow = 'hidden';
    }

    span.onclick = () => {
        modal.style.display = 'none';
        document.body.style.overflow = 'auto';
    }

    window.onclick = (event) => {
        if (event.target == modal) {
            modal.style.display = 'none';
            document.body.style.overflow = 'auto';
        }
    }

    document.getElementById('loginForm').onsubmit = (e) => {
        e.preventDefault();
        handleLoginSuccess('User');
    }

    document.getElementById('googleLoginBtn').onclick = () => {
        const btn = document.getElementById('googleLoginBtn');
        const originalText = btn.innerHTML;
        btn.innerHTML = '<i class="fas fa-circle-notch fa-spin"></i> Connecting to Google...';
        btn.style.opacity = '0.7';
        btn.style.pointerEvents = 'none';

        setTimeout(() => {
            handleLoginSuccess('Google User');
        }, 1500);
    }
}

function handleLoginSuccess(userName) {
    const modal = document.getElementById('loginModal');
    const loginBtn = document.getElementById('loginBtn');

    modal.style.display = 'none';
    document.body.style.overflow = 'auto';

    loginBtn.innerHTML = `<i class="fas fa-user-circle"></i> ${userName}`;
    loginBtn.style.background = 'transparent';
    loginBtn.style.border = '1px solid var(--border-color)';

    alert(`Successfully signed in via ${userName}!`);
}

let allJobs = [];

async function fetchJobs() {
    try {
        const response = await fetch('/api/jobs');
        const jobs = await response.json();
        allJobs = jobs;
        renderJobs(jobs);
    } catch (error) {
        console.error('Error fetching jobs:', error);
    }
}

async function fetchPrep() {
    try {
        const response = await fetch('/api/prep');
        const prep = await response.json();
        renderPrep(prep);
    } catch (error) {
        console.error('Error fetching prep materials:', error);
    }
}

function renderJobs(jobs) {
    const container = document.getElementById('jobs-container');
    container.innerHTML = '';

    jobs.forEach((job, index) => {
        const card = document.createElement('div');
        card.className = 'job-card';
        card.style.animationDelay = `${index * 0.1}s`;

        card.innerHTML = `
            <div class="company">${job.company}</div>
            <h3>${job.title}</h3>
            <div class="job-details">
                <span><i class="fas fa-map-marker-alt"></i> ${job.location}</span>
                <span><i class="fas fa-briefcase"></i> ${job.type}</span>
            </div>
            <p style="font-size: 0.85rem; color: #94a3b8; margin-bottom: 1rem;">${job.requirements.split(',').slice(0, 3).join(' • ')}</p>
            <div class="job-footer">
                <span class="salary">${job.salary}</span>
                <span class="posted">${job.posted_date}</span>
            </div>
        `;

        card.addEventListener('click', () => {
            alert(`Opening details for ${job.title} at ${job.company}`);
        });

        container.appendChild(card);
    });
}

function renderPrep(materials) {
    const container = document.getElementById('prep-container');
    container.innerHTML = '';

    const icons = {
        'Aptitude': 'fa-brain',
        'Coding': 'fa-code',
        'Interview': 'fa-comments'
    };

    materials.forEach((item, index) => {
        const card = document.createElement('div');
        card.className = 'prep-card';
        card.style.animationDelay = `${index * 0.15}s`;
        card.style.cursor = 'pointer';

        const icon = icons[item.category] || 'fa-book';

        card.innerHTML = `
            <span class="prep-icon"><i class="fas ${icon}"></i></span>
            <div style="font-size: 0.7rem; color: var(--accent-color); font-weight: 800; text-transform: uppercase; margin-bottom: 0.5rem;">${item.category}</div>
            <h4>${item.title}</h4>
            <p>${item.description}</p>
            <a href="/prep/${item.id}" class="btn-outline" style="text-decoration: none; display: inline-block; margin-top: 1rem;">Start Learning</a>
        `;

        card.addEventListener('click', (e) => {
            if (e.target.tagName !== 'A') {
                window.location.href = `/prep/${item.id}`;
            }
        });

        container.appendChild(card);
    });
}

function searchJobs() {
    const query = document.getElementById('job-search').value.toLowerCase();
    const filtered = allJobs.filter(job =>
        job.title.toLowerCase().includes(query) ||
        job.company.toLowerCase().includes(query) ||
        job.requirements.toLowerCase().includes(query)
    );
    renderJobs(filtered);
}

// Add event listener for enter key on search
document.getElementById('job-search').addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        searchJobs();
    }
});

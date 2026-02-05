document.addEventListener('DOMContentLoaded', () => {

    setupInternalLinks();

    window.addEventListener('pageshow', (event) => {
        if (event.persisted) {
            document.body.classList.remove('fade-out');
        }
    });
    document.body.classList.remove('fade-out');

    if (document.body.classList.contains('page-home')) {
        initHome();
    } else if (document.getElementById('blog-grid')) {
        initBlogList();
    } else if (document.getElementById('project-grid')) {
        initProjectList();
    } else if (document.body.classList.contains('page-blog-post')) {
        initBlogPost();
    } else if (document.body.classList.contains('page-project-detail')) {
        initProjectDetail();
    } else if (document.getElementById('contactForm')) {
        initContact();
    }
});

function setupInternalLinks() {
    const internalLinks = document.querySelectorAll('a:not([target="_blank"]):not([href^="#"])');
    internalLinks.forEach(link => {
        link.addEventListener('click', function (e) {
            const destination = this.href;
            if (destination === window.location.href) return;

            e.preventDefault();
            document.body.classList.add('fade-out');
            setTimeout(() => {
                window.location.href = destination;
            }, 100);
        });
    });
}

function setupSearch(gridId) {
    const searchForm = document.querySelector('.search-widget');
    if (!searchForm) return;

    const searchInput = searchForm.querySelector('input[type="search"]');

    searchForm.addEventListener('submit', function (e) {
        e.preventDefault();
        const keyword = searchInput.value.trim().toLowerCase();
        const items = document.querySelectorAll(`#${gridId} .grid-item`);

        items.forEach(item => {
            const text = item.textContent.toLowerCase();
            item.style.display = text.includes(keyword) ? 'flex' : 'none';
        });
    });
}

function initHome() {
    loadMarkdown('Resume.md', 'resume-content', 'Could not load resume.');
    loadFeatured('blogs.json', 'featured-blog-widget', 'blog', 'No featured blog selected.');
    loadFeatured('projects.json', 'featured-project-widget', 'projects', 'No featured project selected.');
    initHelloCycler();
}

function initHelloCycler() {
    const helloElement = document.getElementById("hello-cycler");
    if (!helloElement) return;

    const greetings = [
        "Hello", "ನಮಸ್ಕಾರ", "Hola", "Bonjour", "Hello", "Guten Tag",
        "Ciao", "Olá", "Hello", "नमस्ते", "నమస్కారం", "வணக்கம்",
        "你好", "Hello", "こんにちは", "안녕하세요", "Hello", "Здравствуйте",
        "Merhaba", "سلام", "Hello", "שלום", "สวัสดี", "Hello", "Xin chào", "Γεια σας"
    ];
    let helloIndex = 0;
    const helloFadeTime = 600;
    const helloStayTime = 2000;

    const cycleHello = () => {
        helloElement.style.opacity = "0";
        setTimeout(() => {
            helloIndex = (helloIndex + 1) % greetings.length;
            helloElement.textContent = greetings[helloIndex];
            helloElement.style.opacity = "1";
        }, helloFadeTime);
    };
    setInterval(cycleHello, helloStayTime + helloFadeTime);
}

function initBlogList() {
    loadGrid('blogs.json', 'blog-grid', 'blog', 'date');
    loadFeatured('blogs.json', 'featured-blog-widget', 'blog');
}

function initProjectList() {
    loadGrid('projects.json', 'project-grid', 'projects', 'summary');
    loadFeatured('projects.json', 'featured-project-widget', 'projects');
}

function initBlogPost() {

    const authorDiv = document.getElementById('author-info');
    if (authorDiv && authorDiv.innerHTML.trim().length > 0) {
        return; 

    }

    const filename = window.location.pathname.split('/').pop(); 
    const slug = filename.replace('.html', ''); 

    if (!slug) return;

    fetch('../blogs.json')
        .then(res => res.json())
        .then(posts => {
            const meta = posts.find(p => p.slug === slug);
            if (!meta) return;

            if (authorDiv) {
                authorDiv.innerHTML = `
                     <p>Ruthvik Reddy Gade</p>
                     <p style="display: flex; align-items: center; gap: 8px;"><i class="fa-solid fa-calendar-days"></i> ${meta.date}</p>
                     <p style="display: flex; align-items: center; gap: 8px;"><i class="fa-solid fa-envelope"></i><a href="../contact.html">Connect</a></p>
                `;
            }
        })
        .catch(err => console.error(err));
}

function initProjectDetail() {

    const linksWidget = document.getElementById('links-widget');

    if (linksWidget && linksWidget.innerHTML.trim().length > 0) {
        return; 

    }

    const filename = window.location.pathname.split('/').pop();
    const slug = filename.replace('.html', '');

    if (!slug) return;

    fetch('../projects.json')
        .then(res => res.json())
        .then(projects => {
            const meta = projects.find(p => p.slug === slug);
            if (!meta) return;

            if (linksWidget) {
                let linkHtml = '<h4>CHECK IT OUT</h4><div class="featured-item" style="display: flex; flex-direction: column; gap: 10px;">';

                if (meta.github_url) {
                    linkHtml += `<a href="${meta.github_url}" target="_blank"><i class="fa-brands fa-github"></i> GitHub Repository</a>`;
                }
                if (meta.additional_url) {
                    linkHtml += `<a href="${meta.additional_url}" target="_blank"><i class="fa-solid fa-arrow-up-right-from-square"></i> Live Demo</a>`;
                }

                if (!meta.github_url && !meta.additional_url) {
                    linkHtml += `<p>No external links available.</p>`;
                }

                linkHtml += '</div>';
                linksWidget.innerHTML = linkHtml;
            }
        })
        .catch(err => console.error(err));
}

function initContact() {
    const form = document.getElementById('contactForm');
    if (form) {
        form.addEventListener('submit', function (e) {
            e.preventDefault();
            const name = document.getElementById('name').value.trim();
            const message = document.getElementById('message').value.trim();
            window.location.href = `mailto:gaderuthvikreddy@gmail.com?subject=Contact from ${encodeURIComponent(name)}&body=${encodeURIComponent(`Name: ${name}\n\nMessage:\n${message}`)}`;
        });
    }
}

async function loadMarkdown(file, containerId, errorMsg) {
    const container = document.getElementById(containerId);
    if (!container) return;
    try {
        const res = await fetch(file);
        if (!res.ok) throw new Error(res.status);
        const text = await res.text();
        if (typeof marked !== 'undefined') {
            container.innerHTML = marked.parse(text);
        } else {
             container.innerHTML = text;
        }
    } catch (e) {
        console.error(e);
        container.innerHTML = `<p>${errorMsg}</p>`;
    }
}

async function loadFeatured(jsonFile, containerId, routePrefix, errorMsg = 'No featured item.') {
    const container = document.getElementById(containerId);
    if (!container) return;
    try {
        const res = await fetch(jsonFile);
        const items = await res.json();
        const featured = items.find(i => i.featured === true);
        if (featured) {
            container.innerHTML = `
                <a href="${routePrefix}/${featured.slug}.html">
                    <h5>${featured.title}</h5>
                    <p>${featured.summary}</p>
                </a>
            `;
        } else {
            container.innerHTML = `<p>${errorMsg}</p>`;
        }
    } catch (e) {
        container.innerHTML = `<p>Loading failed.</p>`;
    }
}

async function loadGrid(jsonFile, gridId, routePrefix, metaField) {
    const grid = document.getElementById(gridId);
    if (!grid) return;
    try {
        const res = await fetch(jsonFile);
        const items = await res.json();
        grid.innerHTML = '';

        if (items.length === 0) {
            grid.innerHTML = '<p>Nothing to show yet.</p>';
            return;
        }

        items.forEach(item => {
            const el = document.createElement('a');

            el.href = `${routePrefix}/${item.slug}.html`;
            el.className = 'grid-item';

            let html = `<div class="grid-item-content"><h5>${item.title}</h5>`;
            if (metaField === 'date') {
                html += `<p class="grid-item-meta">${item.date}</p><p>${item.summary}</p>`;
            } else {
                html += `<p>${item.summary}</p>`;
            }
            html += `</div>`;

            el.innerHTML = html;
            grid.appendChild(el);
        });

        setupSearch(gridId);
    } catch (e) {
        grid.innerHTML = '<p>Could not load items.</p>';
        console.error(e);
    }
}
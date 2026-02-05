import os
import json
import markdown
import re

TEMPLATE_DIR = "."
OUTPUT_DIR = "."

def build_pages(json_file, template_file, content_folder, output_subfolder, type_prefix):

    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            items = json.load(f)
    except FileNotFoundError:
        print(f"Error: {json_file} not found.")
        return

    try:
        with open(template_file, 'r', encoding='utf-8') as f:
            template_html = f.read()
    except FileNotFoundError:
        print(f"Error: {template_file} not found.")
        return

    template_html = re.sub(
        r'<script>\s*document\.addEventListener\(\'DOMContentLoaded\', \(\) => \{\s*async function loadSingle(Post|Project).*?loadSingle(Post|Project)\(\);\s*\}\);\s*</script>', 
        '', 
        template_html, 
        flags=re.DOTALL
    )

    os.makedirs(os.path.join(OUTPUT_DIR, output_subfolder), exist_ok=True)

    for item in items:
        slug = item['slug']

        md_path = os.path.join(content_folder, f"{slug}.md")
        if not os.path.exists(md_path):
            print(f"Skipping {slug}, markdown not found at {md_path}")
            continue

        with open(md_path, 'r', encoding='utf-8') as f:
            md_content = f.read()

        html_content = markdown.markdown(md_content)

        output_html = template_html

        output_html = output_html.replace('href="style.css"', 'href="../style.css"')
        output_html = output_html.replace('src="scripts/main.js"', 'src="../scripts/main.js"')
        output_html = output_html.replace('href="index.html"', 'href="../index.html"')
        output_html = output_html.replace('href="projects.html"', 'href="../projects.html"')
        output_html = output_html.replace('href="blog.html"', 'href="../blog.html"')
        output_html = output_html.replace('href="contact.html"', 'href="../contact.html"')
        output_html = output_html.replace('href="Resume.pdf"', 'href="../Resume.pdf"')

        output_html = output_html.replace('Something Broke :( - err Bt1', item['title']) 
        output_html = output_html.replace('Something Broke :( - err Pt1', item['title']) 

        if type_prefix == 'blog':

            output_html = output_html.replace('<body class="theme-black">', '<body class="theme-black page-blog-post">')

            output_html = output_html.replace('id="post-header-summary"></p>', f'id="post-header-summary">{item["summary"]}</p>')
            output_html = output_html.replace('id="post-meta"></div>', f'id="post-meta">Published on {item["date"]}</div>')
            output_html = output_html.replace('id="post-body-title"></div>', f'id="post-body-title">{item["title"]}</div>')

            output_html = output_html.replace('id="post-content"></div>', f'id="post-content">{html_content}</div>')

            author_html = f'''
            <p>Ruthvik Reddy Gade</p>
            <p style="display: flex; align-items: center; gap: 8px;"><i class="fa-solid fa-calendar-days"></i> {item["date"]}</p>
            <p style="display: flex; align-items: center; gap: 8px;"><i class="fa-solid fa-envelope"></i><a href="../contact.html">Connect</a></p>
            '''
            output_html = output_html.replace('id="author-info">', f'id="author-info">{author_html}')

        elif type_prefix == 'projects':

            output_html = output_html.replace('<body class="theme-black">', '<body class="theme-black page-project-detail">')

            output_html = output_html.replace('id="project-header-summary"></p>', f'id="project-header-summary">{item["summary"]}</p>')
            output_html = output_html.replace('id="project-meta"></div>', f'id="project-meta">Updated: {item["date"]}</div>')
            output_html = output_html.replace('id="project-body-title"></div>', f'id="project-body-title">{item["title"]}</div>')

            output_html = output_html.replace('id="project-content"></div>', f'id="project-content">{html_content}</div>')

            links_html = '<h4>CHECK IT OUT</h4><div class="featured-item" style="display: flex; flex-direction: column; gap: 10px;">'

            has_links = False
            if 'github_url' in item and item['github_url']:
                links_html += f'<a href="{item["github_url"]}" target="_blank"><i class="fa-brands fa-github"></i> GitHub Repository</a>'
                has_links = True

            if 'additional_url' in item and item['additional_url']:
                links_html += f'<a href="{item["additional_url"]}" target="_blank"><i class="fa-solid fa-arrow-up-right-from-square"></i> Live Demo</a>'
                has_links = True

            if not has_links:
                links_html += '<p>No external links available.</p>'

            links_html += '</div>'
            output_html = output_html.replace('id="links-widget"></div>', f'id="links-widget">{links_html}</div>')

        output_filename = f"{slug}.html"
        output_path = os.path.join(OUTPUT_DIR, output_subfolder, output_filename)

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(output_html)

        print(f"Generated: {output_subfolder}/{output_filename}")

if __name__ == "__main__":
    print("Building Blogs...")
    build_pages('blogs.json', 'blog_template.html', 'blogs-build', 'blog', 'blog')

    print("Building Projects...")
    build_pages('projects.json', 'project_template.html', 'projects-build', 'projects', 'projects')
    print("Done!")
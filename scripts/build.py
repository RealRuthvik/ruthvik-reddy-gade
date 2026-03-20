import os
import json
import markdown
import re
from datetime import datetime
from PIL import Image, ExifTags

TEMPLATE_DIR = "."
OUTPUT_DIR = "."

def build_gallery():
    gallery_dir = os.path.join("assets", "gallery")
    output_file = "gallery.json"
    
    if not os.path.exists(gallery_dir):
        os.makedirs(gallery_dir)
        
    gallery_data = []
    
    for filename in os.listdir(gallery_dir):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
            filepath = os.path.join(gallery_dir, filename)
            device = "Unknown Device"
            date_taken = "1970:01:01 00:00:00"
            
            try:
                img = Image.open(filepath)
                exif = img._getexif()
                if exif:
                    for tag_id, value in exif.items():
                        tag = ExifTags.TAGS.get(tag_id, tag_id)
                        if tag == 'Model':
                            device = str(value).strip()
                        elif tag == 'DateTimeOriginal':
                            date_taken = str(value).strip()
                        elif tag == 'DateTime' and date_taken == "1970:01:01 00:00:00":
                            date_taken = str(value).strip()
            except Exception:
                pass
            
            location = "Unknown"
            if "_" in filename:
                location = filename.split("_")[0].replace("-", " ")
            
            gallery_data.append({
                "src": f"assets/gallery/{filename}",
                "device": device,
                "location": location,
                "date": date_taken
            })
            
    gallery_data.sort(key=lambda x: x['date'], reverse=True)
            
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(gallery_data, f, indent=4)
    print("Generated gallery.json")

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
        
        keywords = item.get('keywords', 'Ruthvik Reddy Gade, Technology, Engineering')
        description = item.get('summary', '').replace('"', '&quot;')
        
        output_html = template_html
        output_html = output_html.replace('SEO_DESCRIPTION_PLACEHOLDER', description)
        output_html = output_html.replace('SEO_KEYWORDS_PLACEHOLDER', keywords)
        output_html = output_html.replace('SEO_OG_TITLE_PLACEHOLDER', item['title'])

        md_path = os.path.join(content_folder, f"{slug}.md")
        if not os.path.exists(md_path):
            print(f"Skipping {slug}, markdown not found at {md_path}")
            continue

        with open(md_path, 'r', encoding='utf-8') as f:
            md_content = f.read()

        html_content = markdown.markdown(md_content)

        output_html = output_html.replace('href="style.css"', 'href="../style.css"')
        output_html = output_html.replace('src="scripts/main.js"', 'src="../scripts/main.js"')
        output_html = output_html.replace('href="index.html"', 'href="../index.html"')
        output_html = output_html.replace('href="about.html"', 'href="../about.html"')
        output_html = output_html.replace('href="projects.html"', 'href="../projects.html"')
        output_html = output_html.replace('href="blog.html"', 'href="../blog.html"')
        output_html = output_html.replace('href="gallery.html"', 'href="../gallery.html"')
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

        updates_html = ""
        if 'updates' in item and item['updates']:
            updates_html = '<div class="widget" style="margin-top: 1em;"><h4>UPDATES</h4><div class="featured-item" style="display: flex; flex-direction: column; gap: 10px;">'
            for update in item['updates']:
                updates_html += f'<div style="border-left: 2px solid var(--accent-color); padding-left: 10px;"><p style="font-size: 11px; color: var(--accent-color); margin-bottom: 2px;"><i class="fa-solid fa-clock"></i> {update["date"]}</p><p style="font-size: 12px; margin: 0;">{update["text"]}</p></div>'
            updates_html += '</div></div>'
        
        output_html = output_html.replace('<div id="updates-widget"></div>', updates_html)

        output_filename = f"{slug}.html"
        output_path = os.path.join(OUTPUT_DIR, output_subfolder, output_filename)

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(output_html)

        print(f"Generated: {output_subfolder}/{output_filename}")

def build_sitemap():
    base_url = "https://ruthvik.me"
    current_date = datetime.now().strftime("%Y-%m-%d")
    
    urls = [
        {"loc": f"{base_url}/", "priority": "1.0", "changefreq": "weekly"},
        {"loc": f"{base_url}/about.html", "priority": "0.9", "changefreq": "monthly"},
        {"loc": f"{base_url}/projects.html", "priority": "0.8", "changefreq": "weekly"},
        {"loc": f"{base_url}/blog.html", "priority": "0.8", "changefreq": "weekly"},
        {"loc": f"{base_url}/gallery.html", "priority": "0.8", "changefreq": "weekly"},
        {"loc": f"{base_url}/contact.html", "priority": "0.5", "changefreq": "yearly"},
    ]
    
    try:
        with open('blogs.json', 'r', encoding='utf-8') as f:
            for item in json.load(f):
                urls.append({
                    "loc": f"{base_url}/blog/{item['slug']}.html",
                    "priority": "0.7",
                    "lastmod": current_date,
                    "changefreq": "monthly"
                })
    except FileNotFoundError:
        pass

    try:
        with open('projects.json', 'r', encoding='utf-8') as f:
            for item in json.load(f):
                urls.append({
                    "loc": f"{base_url}/projects/{item['slug']}.html",
                    "priority": "0.7",
                    "lastmod": current_date,
                    "changefreq": "monthly"
                })
    except FileNotFoundError:
        pass

    xml_lines = ['<?xml version="1.0" encoding="UTF-8"?>']
    xml_lines.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')
    
    for u in urls:
        xml_lines.append('   <url>')
        xml_lines.append(f'      <loc>{u["loc"]}</loc>')
        if "lastmod" in u:
            xml_lines.append(f'      <lastmod>{u["lastmod"]}</lastmod>')
        if "changefreq" in u:
            xml_lines.append(f'      <changefreq>{u["changefreq"]}</changefreq>')
        if "priority" in u:
            xml_lines.append(f'      <priority>{u["priority"]}</priority>')
        xml_lines.append('   </url>')
        
    xml_lines.append('</urlset>')
    
    with open('sitemap.xml', 'w', encoding='utf-8') as f:
        f.write('\n'.join(xml_lines))
    print("Generated sitemap.xml")

if __name__ == "__main__":
    print("Building Gallery JSON...")
    build_gallery()

    print("Building Blogs...")
    build_pages('blogs.json', 'blog_template.html', 'blogs-build', 'blog', 'blog')

    print("Building Projects...")
    build_pages('projects.json', 'project_template.html', 'projects-build', 'projects', 'projects')

    print("Building Sitemap...")
    build_sitemap()
    
    print("Done!")
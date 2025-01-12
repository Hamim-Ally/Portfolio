import os
from inc import write
from loader import load_yaml, init_DataPack, merge_dicts, init_widgets, load_pages
from jinja2 import Environment, FileSystemLoader

# =============================================
# Environment Functions
# =============================================

# Create and return a Jinja2 environment with loaded templates.
def init_env(template_path):
    env = Environment(loader=FileSystemLoader(template_path))  # Use FileSystemLoader
    print("Template is loaded...")  # Debug line
    env.globals['print'] = print
    env.globals['int'] = int
    return env

# Add widget templates to the Jinja2 environment as global templates.
def init_global_widgets(env, widgets):
    for widget_name, widget_content in widgets.items():
        env.globals[widget_name] = env.from_string(widget_content)

# =============================================
# Rendering Functions
# =============================================

# Render a template with the given context.
def render_template(template_name, context, env):
    template = env.get_template(template_name)
    return template.render(context)

# Render content from YAML definitions.
def render_Content(content_sections, env, context):
    sections_content = ""
    for section in content_sections:
        if 'widget' in section:
            widget_name = section['widget']
            if widget_name in env.globals:
                widget_context = {**context, **section.get('data', {})}
                sections_content += env.globals[widget_name].render(widget_context)
        elif 'html' in section:
            sections_content += section['html']  # Use the HTML content directly
    return sections_content

# Render the full output path for the page.
def render_path(base_path, url):
    full_path = os.path.join(base_path, url.lstrip('/'))
    os.makedirs(full_path, exist_ok=True)
    return os.path.join(full_path, 'index.html')

# Generate HTML pages from YAML content and templates.
def render_pages():
    config = init_DataPack('src/config')
    widgets = init_widgets(config['widgets_path'])
    env = init_env(config['templates_path'])
    init_global_widgets(env, widgets)

    seen_urls = set()  # Track all URLs to detect duplicates
    
    # Loop through all page directories defined in config['pages_path']
    for pages_dir in config['pages_path']:
        page_files = load_pages(pages_dir)  # Load page files from each directory

        for page_file in page_files:
            content = load_yaml(os.path.join(pages_dir, page_file))

            # Skip page generation if 'url' is missing
            if 'url' not in content:
                print(f"Skipping '{page_file}' as it has no 'url'.")
                continue  # Skip to the next page

            url = content['url']
            # Enforce unique URLs across all pages
            if url in seen_urls:
                raise ValueError(f"Duplicate URL found: '{url}' in '{page_file}'.")
            seen_urls.add(url)

            # Enforce the presence of 'template'
            if 'template' not in content:
                raise KeyError(f"Template not defined in '{page_file}'.")

            # Merge additional data from config and page YAML content
            context = merge_dicts(config, content)

            # Render content sections if defined
            if 'content_sections' in content:
                context['sections_content'] = render_Content(content['content_sections'], env, context)

            # Define output path and render the template
            output_file_path = render_path('.', url)

            try:
                page_content = render_template(f"{content['template']}.html", context, env)
                # Write the rendered template to the output file
                write(page_content, output_file_path)
                print(f'   Page written to {output_file_path}')
            except Exception as e:
                print(f"Error rendering '{page_file}': {e}")


import click
import yaml
from jinja2 import Environment, FileSystemLoader
from pathlib import Path

@click.command()
@click.option('--yaml-file', default='infores_catalog.yaml', help='Path to YAML catalog.')
@click.option('--output-dir', default='docs', help='Output directory for markdown files.')
@click.option('--overview-template', help='Ref to jinja template for overview.')
@click.option('--detail-template', help='Ref to jinja template for resources.')
def generate_docs(yaml_file, output_dir, overview_template, detail_template):
    env = Environment(loader=FileSystemLoader('.'))
    
    # Use different variable names here
    overview_tmpl = env.get_template(overview_template)
    detail_tmpl = env.get_template(detail_template)

    with open(yaml_file, 'r') as f:
        data = yaml.safe_load(f)

    resources = data.get('information_resources', [])

    # Generate overview table
    overview_content = overview_tmpl.render(resources=resources)
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    with open(Path(output_dir) / 'registry.md', 'w') as f:
        f.write(overview_content)

    # Generate details for each resource
    detail_dir = Path(output_dir) / 'details'
    detail_dir.mkdir(parents=True, exist_ok=True)

    for resource in resources:
        detail_content = detail_tmpl.render(resource=resource)
        filename = resource['id'].replace(':', '_') + '.md'
        with open(detail_dir / filename, 'w') as f:
            f.write(detail_content)

if __name__ == '__main__':
    generate_docs()

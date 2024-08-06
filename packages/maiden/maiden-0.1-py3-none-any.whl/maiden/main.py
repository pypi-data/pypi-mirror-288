import re
import click
import yaml
import json
from jinja2 import Template

def load_data(file_path):
    """Load data from a YAML or JSON file"""
    if file_path.endswith('.yaml') or file_path.endswith('.yml'):
        with open(file_path, 'r') as f:
            return yaml.safe_load(f)
    elif file_path.endswith('.json'):
        with open(file_path, 'r') as f:
            return json.load(f)
    else:
        raise ValueError("Unsupported file format. Use YAML or JSON.")

def preprocess_template(template_str):
    """Preprocess the template to replace custom syntax with actual data"""
    pattern = r"<% FROM (.+?) GET '(.+?)' %>"
    matches = re.findall(pattern, template_str)

    for match in matches:
        source_file, key = match
        data = load_data(source_file)
        
        # Split the key by dots to traverse nested dictionaries
        keys = key.split('.')
        value = data
        for k in keys:
            value = value.get(k, '')
        
        # Handle cases where the key path is invalid
        if not value:
            value = "[Missing Data]"

        # Replace the custom directive with the actual value
        template_str = template_str.replace(f"<% FROM {source_file} GET '{key}' %>", value)
    
    return template_str

@click.command()
@click.argument('template_file')
@click.argument('output_file')
def generate_md(template_file, output_file):
    """CLI command to generate markdown from template"""
    with open(template_file, 'r') as f:
        template_str = f.read()

    # Preprocess template to replace custom syntax
    processed_template_str = preprocess_template(template_str)
    
    # Render the final markdown using Jinja2
    template = Template(processed_template_str)
    result = template.render()

    # Write output to file
    with open(output_file, 'w') as f:
        f.write(result)

if __name__ == '__main__':
    generate_md()

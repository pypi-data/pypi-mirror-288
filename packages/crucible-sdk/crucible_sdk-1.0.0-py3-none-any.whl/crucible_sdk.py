import os
import click
import yaml


def parse_openapi(openapi_file):
    with open(openapi_file, 'r') as file:
        openapi_spec = yaml.safe_load(file)

    endpoints = {}

    for path, path_item in openapi_spec['paths'].items():
        for method, method_item in path_item.items():
            if method not in ["get", "post", "delete", "put", "patch"]:
                continue

            endpoint_info = {
                "url": path,
                "method": method,
                "description": method_item.get("description", ""),
                "parameters": [],
                "requestBody": method_item.get("requestBody", None),
                "responses": method_item.get("responses", {})
            }

            # Process parameters
            if "parameters" in method_item:
                for param in method_item["parameters"]:
                    param_info = {
                        "name": param["name"],
                        "in": param["in"],
                        "required": param.get("required", False),
                        "description": param.get("description", ""),
                        "schema": param.get("schema", {})
                    }
                    endpoint_info["parameters"].append(param_info)

            endpoints[method_item.get("operationId", "")] = endpoint_info

    return endpoints


def create_init_file(directory):
    with open(os.path.join(directory, '__init__.py'), 'w') as f:
        f.write('')


def generate_sdk(config_file, openapi_file, output_dir):
    with open(config_file, 'r') as file:
        config = yaml.safe_load(file)

    endpoints = parse_openapi(openapi_file)
    base_class_name = config.get('class_name', 'APIClient')
    base_url = config.get('base_url', 'https://api.example.com')
    token_env_var = config.get('token_env_var', 'API_TOKEN')
    # Support for different auth types
    auth_type = config.get('auth_type', 'Bearer')

    base_class_code = f"""
import os
import requests

class {base_class_name}:
    def __init__(self, base_url: str = '{base_url}', api_key: str = None):
        self.base_url = base_url
        self.api_key = api_key or os.getenv('{token_env_var}')
        if not self.api_key:
            raise ValueError("API key must be provided either as a parameter or through the {token_env_var} environment variable.")
"""

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    create_init_file(output_dir)

    with open(os.path.join(output_dir, f"{base_class_name.lower()}.py"), 'w') as file:
        file.write(base_class_code)

    for function in config['functions']:
        print(f"Generating function: {function['name']}")
        func_name = function['name']
        endpoint = function['endpoint']
        method = function['method']
        parameters = function['parameters']

        submodule_path = func_name.split('.')
        if len(submodule_path) < 2:
            raise ValueError(
                f"Function name '{func_name}' is not in the format 'module.function'")

        module_name = submodule_path[0]
        submodule_name = submodule_path[1]

        module_dir = os.path.join(output_dir, module_name)
        if not os.path.exists(module_dir):
            os.makedirs(module_dir)
            create_init_file(module_dir)

        module_file = os.path.join(module_dir, f"{submodule_name}.py")
        # Overwrite the module file instead of appending
        with open(module_file, 'w') as f:
            f.write(
                f"from ..{base_class_name.lower()} import {base_class_name}\n")
            f.write("import requests\n\n")

        endpoint_info = None
        for op_id, ep_info in endpoints.items():
            if ep_info["url"] == endpoint and ep_info["method"] == method:
                endpoint_info = ep_info
                break

        if not endpoint_info:
            print(
                f"Endpoint {endpoint} with method {method} not found in OpenAPI")
            continue

        params_str = ", ".join(parameters)
        path_params = [param["name"]
                       for param in endpoint_info["parameters"] if param["in"] == "path"]
        query_params = [param["name"]
                        for param in endpoint_info["parameters"] if param["in"] == "query"]
        body_params = [
            param for param in parameters if param not in path_params and param not in query_params]

        path_format = endpoint
        for path_param in path_params:
            path_format = path_format.replace(
                f"{{{path_param}}}", f"{{{path_param}}}")

        if auth_type == 'Bearer':
            auth_header = f'"Authorization": f"Bearer {{self.api_key}}"'
        else:
            auth_header = f'"token": self.api_key'

        # Generate docstring
        docstring = f'"""{endpoint_info["description"]}\n\n'
        docstring += "    Args:\n"
        for param in endpoint_info["parameters"]:
            docstring += f'        {param["name"]} ({param["schema"].get("type", "unknown")}): {param["description"]}\n'
        if endpoint_info["requestBody"]:
            docstring += f'        data (dict): {endpoint_info["requestBody"].get("description", "Request body data")}\n'
        docstring += "\n    Returns:\n"
        docstring += "        dict: Response from the API.\n"
        docstring += '    """\n'

        function_code = f"""
def {submodule_name}(self, {params_str}):
    {docstring}
    url = self.base_url + f"{path_format}"
    headers = {{{auth_header}}}
"""

        if query_params:
            function_code += "    params = {\n"
            function_code += ",\n".join(
                [f'        "{param}": {param}' for param in query_params])
            function_code += "\n    }\n"
        else:
            function_code += "    params = None\n"

        if body_params and method in ['post', 'put', 'patch']:
            function_code += "    data = {\n"
            function_code += ",\n".join(
                [f'        "{param}": {param}' for param in body_params])
            function_code += "\n    }\n"
        else:
            function_code += "    data = None\n"

        function_code += f"""
    response = requests.{method}(url, headers=headers, params=params, json=data)
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()
"""

        print("Function code:")
        print(function_code)

        with open(module_file, 'a') as f:
            f.write(function_code)


@click.group()
def cli():
    pass


@click.command()
@click.argument('project_name')
def create_project(project_name):
    """Create a new SDK project."""
    os.makedirs(project_name)
    os.makedirs(os.path.join(project_name, 'causadb'))
    os.makedirs(os.path.join(project_name, 'tests'))
    create_init_file(os.path.join(project_name, 'causadb'))
    create_init_file(os.path.join(project_name, 'tests'))

    with open(os.path.join(project_name, 'pyproject.toml'), 'w') as f:
        f.write(f"""
[tool.poetry]
name = "{project_name}"
version = "0.1.0"
description = "A SDK for interacting with CausaDB API"
authors = ["Your Name <you@example.com>"]
[tool.poetry.dependencies]
python = "^3.8"
requests = "^2.25.1"
pydantic = "^1.8"
[tool.poetry.dev-dependencies]
pytest = "^6.2.2"
[build-system]
requires = ["poetry-core>=1.0.0"]
build-backend = "poetry.core.masonry.api"
""")

    with open(os.path.join(project_name, 'README.md'), 'w') as f:
        f.write("# " + project_name + "\n")

    with open(os.path.join(project_name, 'setup.cfg'), 'w') as f:
        f.write(f"""
[metadata]
name = {project_name}
version = 0.1.0
description = A SDK for interacting with CausaDB API
long_description = file: README.md
long_description_content_type = text/markdown
author = Your Name
author_email = you@example.com
license = MIT
license_file = LICENSE
classifiers =
    Programming Language :: Python :: 3
    License :: OSI Approved :: MIT License
    Operating System :: OS Independent

[options]
packages = find:
python_requires = >=3.8
install_requires =
    requests
    pydantic

[options.packages.find]
where = causadb
""")

    with open(os.path.join(project_name, 'LICENSE'), 'w') as f:
        f.write("MIT License\n\n...")

    with open(os.path.join(project_name, 'tests/test_example.py'), 'w') as f:
        f.write("""
def test_example():
    assert True
""")

    print(f"Project {project_name} created successfully.")


@click.command()
@click.argument('config_file')
@click.argument('openapi_file')
@click.argument('output_dir')
def update_sdk(config_file, openapi_file, output_dir):
    """Update the SDK codebase."""
    generate_sdk(config_file, openapi_file, output_dir)
    print(f"SDK updated successfully in {output_dir}.")


cli.add_command(create_project)
cli.add_command(update_sdk)

if __name__ == '__main__':
    cli()

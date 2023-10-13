import json
from bs4 import BeautifulSoup
from collections import defaultdict
from typing import Any, Dict, List, Union
from real_agents.adapters.data_model.base import DataModel
import requests
import re
import tiktoken

JsonNode = Dict[str, Union[str, List[Any], int]]
PossibleTemplate = Dict[str, Union[str, List[Any], int]]
OptimizedTemplate = Dict[str, Union[str, List[Any], int, set]]
PossibleTemplates = Dict[str, PossibleTemplate]


def find_potential_templates(node, possible_templates):
    """Find all potential templates in the HTML tree."""
    if node.name:  # Element node
        attributes = {attr: node[attr] for attr in node.attrs}
        children = []
        for child in node.children:
            child_json = find_potential_templates(child, possible_templates)
            if child_json:
                children.append(child_json)

        # Max depth of the tree
        depth = max([c["depth"] for c in children], default=0) + 1

        # Create a template hash
        template_hash = f"{node.name}#{sorted(attributes.keys())}#{[c['template_hash'] for c in children]}"

        # Gather template values
        template_values = list(attributes.values()) + [val for c in children for val in c["template_values"]]

        json_node = {
            "type": "ELEMENT",
            "tag_name": node.name,
            "attributes": attributes,
            "children": children,
            "template_hash": template_hash,
            "template_values": template_values,
            "depth": depth,
        }

        # Add node to possible templates
        if template_hash in possible_templates:
            if possible_templates[template_hash][0]["depth"] != depth:
                raise ValueError(f"Template depth mismatch for template {template_hash}")
            possible_templates[template_hash].append(json_node)
        else:
            possible_templates[template_hash] = [json_node]

        return json_node
    elif isinstance(node, str):  # Text node
        text = node.strip()
        if text:
            return {"type": "TEXT", "content": text, "template_hash": "TEXT", "template_values": [text], "depth": 0}
    return None


def optimize_template(template):
    """Check and adjust the template in possible_templates to optimize style."""
    values_to_inline = {
        i
        for i in range(len(template["nodes"][0]["templateValues"]))
        if all(n["templateValues"][i] == template["nodes"][0]["templateValues"][i] for n in template["nodes"])
    }
    return {**template, "valuesToInline": values_to_inline}


def is_string_a_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


def get_placeholder(template, value_index):
    """Get the placeholder for the value at the given index in the template."""
    placeholder_index = value_index + 1 - len([i for i in template["valuesToInline"] if i < value_index])
    return f"${placeholder_index}"


def create_template_tree(node, templates, render_for_template, current_value_index=0):
    """Convert the DOM into processed template tree."""
    if node["type"] == "TEXT":
        if current_value_index in render_for_template["valuesToInline"]:
            return {
                "template": node["content"],
                "valueIndex": current_value_index + 1,
                "consumedTemplates": [node["templateHash"]],
            }
        else:
            return {
                "template": get_placeholder(render_for_template, current_value_index),
                "valueIndex": current_value_index + 1,
                "consumedTemplates": [node["templateHash"]],
            }

    else:
        updated_value_index = current_value_index
        consumed_templates = [node["templateHash"]]

        attrs = "".join(
            [
                f' {k}="{v}"'
                if updated_value_index + i in render_for_template["valuesToInline"]
                else f" {k}={get_placeholder(render_for_template, updated_value_index + i)}"
                for i, (k, v) in enumerate(node["attributes"].items())
            ]
        )
        updated_value_index += len(node["attributes"])

        children = []
        for child in node["children"]:
            child_template = create_template_tree(child, templates, render_for_template, updated_value_index)
            children.append(child_template["template"])
            updated_value_index = child_template["valueIndex"]
            consumed_templates.extend(child_template["consumedTemplates"])

        return {
            "template": f"<{node['tagName'].lower()}{attrs}/>"
            if not children
            else f"<{node['tagName'].lower()}{attrs}>{''.join(children)}</{node['tagName'].lower()}>",
            "valueIndex": updated_value_index,
            "consumedTemplates": consumed_templates,
        }


def serialize_tree(node, templates):
    """Serialize the template tree into HTML string."""
    if node["type"] == "TEXT":
        return node["content"]
    elif node["templateHash"] in templates:
        template = templates[node["templateHash"]]
        return f"{{T{template['label']}({','.join([str(v) if is_string_a_number(v) else json.dumps(v) for i, v in enumerate(node['templateValues']) if i not in template['valuesToInline']])})}}"
    else:
        attrs = "".join([f' {k}="{v}"' for k, v in node["attributes"].items()])
        children = "".join([serialize_tree(c, templates) for c in node["children"]])
        return (
            f"<{node['tagName'].lower()}{attrs}/>"
            if not children
            else f"<{node['tagName'].lower()}{attrs}>{children}</{node['tagName'].lower()}>"
        )


def truncate_html_by_tokens(html_string, max_tokens, model_name, num_tags_to_remove_each_time=10):
    tokens_count = count_tokens(html_string, model_name)
    num_tags_to_remove_each_time = round(tokens_count / 500)
    soup = BeautifulSoup(html_string, "html.parser")
    # Remove all iframe tags
    html_string = remove_iframes(html_string)
    while tokens_count > max_tokens:
        tags = soup.find_all(True)  # find all tags
        # remove the last N tags
        for tag in tags[-num_tags_to_remove_each_time:]:
            tag.decompose()

        html_string = str(soup)

        # re-count the tokens
        tokens_count = count_tokens(html_string, model_name)

    return html_string


# hacky way
def remove_iframes(html_string):
    # Remove all iframe tags using regex
    return re.sub("<iframe.*?/iframe>", "", html_string, flags=re.DOTALL)


# if you wanna change encoding schema, refer to https://github.com/openai/openai-cookbook/blob/main/examples/How_to_count_tokens_with_tiktoken.ipynb
def count_tokens(text, model_name):
    encoding = tiktoken.get_encoding("cl100k_base")
    return len(encoding.encode(text))


class HTMLDataModel(DataModel):
    """A data model for HTML, for webot purpose."""

    def get_llm_side_data(self) -> str:
        html_string = self.raw_data
        truncated_html_string = truncate_html_by_tokens(html_string, 5000, "gpt-4")
        return truncated_html_string

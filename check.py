"""
This module checks if the text in the quran folder is correct.
"""
import os
import re
import yaml

QURAN_FOLDER = "quran"


def parse_linked(text):
    """Get the text from the first markdown quote after the props between the two ---. After that, replace all links in [[text|alias]] format with the alias text."""
    markdown = re.match(r"---\n.*\n---\n(.*)", text, re.DOTALL)
    if not markdown:
        return ""
    markdown = markdown.group(1)
    markdown_quote = re.match(r"> (.*)", markdown)
    if not markdown_quote:
        return ""
    markdown_quote = markdown_quote.group(1)

    link_regex = re.compile(r"\[\[(?P<text>.*?)\|(?P<alias>.*?)\]\]")
    markdown_quote = re.sub(link_regex, r"\g<alias>", markdown_quote)
    link_regex = re.compile(r"\[\[(?P<text>.*?)\]\]")
    markdown_quote = re.sub(link_regex, r"\g<text>", markdown_quote)
    return markdown_quote


def get_ref(text):
    """get the text property from the yaml between the ---"""
    props = re.match(r"---\n(.*)\n---", text, re.DOTALL)
    if not props:
        return ""
    props = yaml.load(props.group(1), Loader=yaml.FullLoader)
    return props["text"]


if __name__ == "__main__":
    errors = {}
    for ayah in os.listdir(QURAN_FOLDER):
        if len(ayah) == 6:
            continue
        ayah_path = os.path.join(QURAN_FOLDER, ayah)
        with open(ayah_path, "r", encoding="utf-8") as f:
            text = f.read()
        ref = get_ref(text)
        parsed = parse_linked(text)
        if parsed != ref:
            print(f"Error in {ayah_path}")
            errors[ayah] = {"expected": ref, "got": parsed}
    if errors:
      yaml.dump(errors, open("errors.yaml", "w", encoding="utf-8"), allow_unicode=True, default_flow_style=False, sort_keys=False)
      print(f"Errors found in {len(errors)} ayahs. See errors.yaml for details.")
    else:
      print("All text is correct")

import streamlit as st
from datetime import date
import os
import re
import yaml

BLOG_DIR = os.path.join(os.path.dirname(__file__), "..", "blog")
TAGS_FILE = os.path.join(BLOG_DIR, "tags.yml")
AUTHORS = ["nlu"]


def load_tags() -> dict:
    if not os.path.exists(TAGS_FILE):
        return {}
    with open(TAGS_FILE, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def save_tags(tags_dict: dict) -> None:
    with open(TAGS_FILE, "w", encoding="utf-8") as f:
        for key, meta in tags_dict.items():
            f.write(f"{key}:\n")
            f.write(f"  label: {meta['label']}\n")
            f.write(f"  permalink: {meta['permalink']}\n")
            f.write(f"  description: {meta['description']}\n")
            f.write("\n")

st.set_page_config(page_title="Blog Post Builder", layout="wide")
st.title("Blog Post Builder")

# --- Inputs ---
col1, col2 = st.columns(2)

with col1:
    pub_date = st.date_input("Publication date", value=date.today())
    title = st.text_input("Title", placeholder="My New Post")
    slug = st.text_input(
        "Slug (optional)",
        placeholder="my-new-post — leave blank to derive from title",
    )
    authors = st.multiselect("Authors", AUTHORS, default=["nlu"])

with col2:
    known_tags = load_tags()
    tags_input = st.text_input(
        "Tags (comma-separated)", placeholder="aws, cloud, howto"
    )
    tags = [t.strip() for t in tags_input.split(",") if t.strip()]
    new_tags = [t for t in tags if t and t not in known_tags]
    if new_tags:
        st.warning(f"New tags (not in tags.yml): **{', '.join(new_tags)}** — will be added on save.")

st.divider()

# --- Content ---
intro = st.text_area(
    "Intro / preview (shown in listing)",
    height=150,
    placeholder="This paragraph will appear in the blog listing page.",
)

body = st.text_area(
    "Body (shown only on full post page)",
    height=300,
    placeholder="Full post content goes here. Markdown is supported.",
)

# --- Tabbed code blocks ---
st.divider()
st.subheader("Tabbed code examples (Windows / Linux)")
st.caption("Each entry renders as a Windows + Linux tab pair. Leave both blank to skip.")

if "tab_blocks" not in st.session_state:
    st.session_state.tab_blocks = [{"label": "", "windows": "", "linux": ""}]

def add_block():
    st.session_state.tab_blocks.append({"label": "", "windows": "", "linux": ""})

def remove_block(i):
    st.session_state.tab_blocks.pop(i)

for i, block in enumerate(st.session_state.tab_blocks):
    with st.expander(f"Code block {i + 1}" + (f" — {block['label']}" if block["label"] else ""), expanded=True):
        block["label"] = st.text_input(
            "Section heading (optional)", value=block["label"],
            key=f"label_{i}", placeholder="e.g. Install the CLI"
        )
        c1, c2 = st.columns(2)
        with c1:
            block["windows"] = st.text_area(
                "Windows (PowerShell)", value=block["windows"],
                key=f"win_{i}", height=120,
                placeholder="pip install boto3"
            )
        with c2:
            block["linux"] = st.text_area(
                "Linux / macOS (bash)", value=block["linux"],
                key=f"lin_{i}", height=120,
                placeholder="pip3 install boto3"
            )
        if len(st.session_state.tab_blocks) > 1:
            st.button("Remove this block", key=f"remove_{i}", on_click=remove_block, args=(i,))

st.button("+ Add another code block", on_click=add_block)

# --- Derived values ---
def slugify(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_]+", "-", text)
    return text

def render_tab_block(block: dict) -> str:
    lines = []
    if block["label"]:
        lines.append(f"## {block['label']}\n")
    lines.append("import Tabs from '@theme/Tabs';")
    lines.append("import TabItem from '@theme/TabItem';")
    lines.append("")
    lines.append("<Tabs>")
    lines.append('  <TabItem value="windows" label="Windows">')
    lines.append("")
    lines.append("```powershell")
    lines.append(block["windows"].strip())
    lines.append("```")
    lines.append("")
    lines.append("  </TabItem>")
    lines.append('  <TabItem value="linux" label="Linux / macOS">')
    lines.append("")
    lines.append("```bash")
    lines.append(block["linux"].strip())
    lines.append("```")
    lines.append("")
    lines.append("  </TabItem>")
    lines.append("</Tabs>")
    return "\n".join(lines)

active_blocks = [b for b in st.session_state.tab_blocks if b["windows"].strip() or b["linux"].strip()]
use_mdx = bool(active_blocks)

effective_slug = slug.strip() if slug.strip() else slugify(title)
date_str = pub_date.strftime("%Y-%m-%d")
ext = "mdx" if use_mdx else "md"
filename = f"{date_str}-{effective_slug}.{ext}" if effective_slug else ""

# --- Build full content ---
authors_yaml = "[" + ", ".join(authors) + "]"
tags_yaml = "[" + ", ".join(tags) + "]" if tags else "[]"

front_matter_lines = ["---"]
if effective_slug:
    front_matter_lines.append(f"slug: {effective_slug}")
safe_title = title or '<title>'
if any(c in safe_title for c in ':#{}[]|>&*?!,'):
    safe_title = f'"{safe_title}"'
front_matter_lines.append(f"title: {safe_title}")
front_matter_lines.append(f"authors: {authors_yaml}")
front_matter_lines.append(f"tags: {tags_yaml}")
front_matter_lines.append("---")
front_matter = "\n".join(front_matter_lines)

truncate_marker = "{/* truncate */}" if use_mdx else "<!-- truncate -->"

full_content = front_matter + "\n\n"
if intro:
    full_content += intro + "\n\n"
full_content += truncate_marker + "\n\n"
if body:
    full_content += body + "\n\n"
for block in active_blocks:
    full_content += render_tab_block(block) + "\n\n"

# --- Preview ---
st.divider()
st.subheader("Front matter preview")
st.code(front_matter, language="yaml")

if use_mdx:
    st.info("Using `.mdx` — Tabs component will be included.")

with st.expander("Full file preview"):
    st.code(full_content, language="markdown")

# --- Save ---
st.divider()

if filename:
    output_path = os.path.normpath(os.path.join(BLOG_DIR, filename))
    st.write(f"Output file: `{output_path}`")
else:
    st.warning("Enter a title to determine the output filename.")
    output_path = None

can_save = bool(title and authors and output_path)

if st.button("Save blog post", disabled=not can_save, type="primary"):
    if os.path.exists(output_path):
        st.error(f"`{filename}` already exists. Rename or change the date/slug.")
    else:
        # Write new tags to tags.yml first
        if new_tags:
            updated_tags = dict(known_tags)
            for t in new_tags:
                label = t.replace("-", " ").title()
                updated_tags[t] = {
                    "label": label,
                    "permalink": f"/{t}",
                    "description": f"{label} tag description",
                }
            save_tags(updated_tags)
            st.success(f"Added to tags.yml: {', '.join(new_tags)}")

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(full_content)
        st.success(f"Saved: `{filename}`")
        st.info("Commit and push to `main` to publish via AWS Amplify.")

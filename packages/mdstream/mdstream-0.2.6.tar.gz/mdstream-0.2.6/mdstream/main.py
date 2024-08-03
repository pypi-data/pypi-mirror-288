import json
import time
from rich.console import Console
from rich.live import Live
from rich.markdown import Markdown as RichMarkdown
from rich.theme import Theme

class Markdown:
    """Stream formatted JSON-like text to the terminal with live updates."""
    
    def __init__(self, lines, mdargs=None, style="default", save=False):
        """Initialize the Markdown class.

        Usage:
            >>> from markdown_stream import Markdown
            >>> md = Markdown(lines=[{"key": "value"}], mdargs=None, style="default")
            >>> md.stream()
        """
        self.lines = lines
        self.printed = ""
        self.mdargs = mdargs or {
            "code_theme": "github-light",
            "inline_code_theme": "github-light",
            "style": style or "reverse",
        }
        self.style = self.mdargs.get("style", "reverse")
        self.console = Console(force_terminal=True, color_system="truecolor")
        self.live = Live(console=self.console, refresh_per_second=4)
        self.save = save

    def __del__(self):
        if self.live:
            self.live.stop()

    def stream(self):
        def generate_markdown(data, depth=0):
            """Generate Markdown from JSON with headers based on depth."""
            markdown_lines = []
            indent = " " * (depth * 2)  # Indentation for nested structures
            
            if isinstance(data, dict):
                for key, value in data.items():
                    markdown_lines.append(f"{indent}**{key}**:")
                    if isinstance(value, (dict, list)):
                        markdown_lines.extend(generate_markdown(value, depth + 1))
                    else:
                        markdown_lines.append(f"{indent}- {value}")
            elif isinstance(data, list):
                for item in data:
                    markdown_lines.extend(generate_markdown(item, depth))
            else:
                markdown_lines.append(f"{indent}{data}")
            
            return markdown_lines

        # Check if the input is a string and attempt to parse it as JSON
        if isinstance(self.lines, str):
            try:
                self.lines = json.loads(self.lines)
            except json.JSONDecodeError:
                # If it's just a string, display as is
                self.lines = [self.lines]

        # Ensure we have a list of items to process
        if isinstance(self.lines, dict):
            self.lines = [self.lines]

        with self.live as live:
            self.printed = ""
            for line in self.lines:
                if line:
                    markdown_lines = generate_markdown(line)
                    for markdown_line in markdown_lines:
                        # Update line-by-line
                        self.printed += markdown_line + "\n"
                        live.update(RichMarkdown(self.printed.strip(), **self.mdargs))
                        time.sleep(0.1)  # Adjust the delay for line-by-line update

# Example usage with mixed input
if __name__ == "__main__":
    # JSON string input
    json_string = '''
    {
        "name": "mbodied",
        "version": "1.0.6",
        "summary": "Embodied AI",
        "downloads": 0,
        "urls": {
            "Documentation": "https://github.com/mbodiai/embodied-agents#readme",
            "Issues": "https://github.com/mbodiai/embodied-agents/issues",
            "Source": "https://github.com/mbodiai/embodied-agents"
        },
        "description": "Benchmark, Explore, and Send API Requests Now\\n\\n[![license](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)",
        "github_url": "https://github.com/mbodiai/embodied-agents#readme"
    }
    '''

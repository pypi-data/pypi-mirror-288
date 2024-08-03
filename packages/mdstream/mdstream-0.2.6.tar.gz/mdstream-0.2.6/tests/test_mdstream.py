import pytest
from mdstream import MarkdownStream
import time
def test_mdstream():
    packages  = [
        {"name": "mdstream", "version": "0.0.1", "downloads": 100, "summary": "Markdown streamer",
         "urls": []},
    ]
    md = MarkdownStream()
    md.update("# Packages found:")
    for p in packages:
        md.update(f"## {p['name']}")
        md.update(f"**Version:** {p['version']}")
        md.update(f"**Downloads:** {p['downloads']}")
        md.update(f"**Summary:** {p['summary']}")
        md.update(f"**URLs:** {p.get('urls', '')}")
        md.update("---", final=True)
        time.sleep(2)

  
if __name__ == "__main__":
    test_mdstream()
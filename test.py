import markdown2
a = """
```mermaid
gantt
title A Gantt Diagram
dateFormat  YYYY-MM-DD
section Section
A task           :a1, 2014-01-01, 30d
Another task     :after a1  , 20d
section Another
Task in sec      :2014-01-12  , 12d
another task      : 24d
```
"""
print(a)
md = markdown2.markdown(a, extras=['fenced-code-blocks', 'mermaid'])

html_header = """<!DOCTYPE html>
<html>
  <head>
    <style>
    .mermaid-pre {
        visibility: hidden;
    }
    </style>
  </head>
  <body>
    <h1>Mermaid Example</h1>
"""

html_footer = """    <script type="module" defer>
      import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@9/dist/mermaid.esm.min.mjs';
      mermaid.initialize({
        securityLevel: 'loose',
        startOnLoad: true
      });
      let observer = new MutationObserver(mutations => {
        for(let mutation of mutations) {
          mutation.target.style.visibility = "visible";
        }
      });
      document.querySelectorAll("pre.mermaid-pre div.mermaid").forEach(item => {
        observer.observe(item, { 
          attributes: true, 
          attributeFilter: ['data-processed'] });
      });
    </script>
  </body>
</html>
"""

html = html_header + md + html_footer

print(md)

fp = "test-markdown.html"
with open(fp, "w+", newline="", encoding="UTF-8") as f:
    f.write(html)
#!/usr/bin/env python3

import requests as req, zipfile, io, markdown2 as md, sqlite3, os, shutil

html_tmpl = """<html><head><link rel="stylesheet" type="text/css" href="../style.css"/></head><body><section id="tldr"><div id="page">%content%</div></section></body></html>"""

doc_source = "https://github.com/tldr-pages/tldr/archive/master.zip"
doc_path = "tldrpages.docset/Contents/Resources/Documents/"
doc_pref = "tldr-master/pages"

if os.path.exists(doc_path):
    try: shutil.rmtree(doc_path)
    except OSError as e:
        print("Could not delete dirs " + e.strerror)
        raise SystemExit
os.makedirs(doc_path)

try: r = req.get(doc_source)
except ConnectionError:
    print("Could not load tldr-pages from " + doc_source)
    raise SystemExit

if r.status_code != 200:
    print("Could not load tldr-pages.")
    raise SystemExit

db = sqlite3.connect("tldrpages_vs%s.dsidx" % "0.0.2")
cur = db.cursor()

try: cur.execute('DROP TABLE searchIndex;')
except: pass
cur.execute('CREATE TABLE searchIndex(id INTEGER PRIMARY KEY, name TEXT, type TEXT, path TEXT);')
cur.execute('CREATE UNIQUE INDEX anchor ON searchIndex (name, type, path);')

# Generate HTML documents
markdowner = md.Markdown()
with zipfile.ZipFile(io.BytesIO(r.content), "r") as archive:
    for path in archive.namelist():
        if path.startswith(doc_pref) and path.endswith(".md"):
            sub_dir = os.path.join(doc_path, path[len(doc_pref)+1:path.rfind("/")])
            if not os.path.exists(sub_dir):
                try: os.mkdir(sub_dir)
                except OSError as e:
                    print("Could not create dir " + e.strerror)
                    raise SystemExit
            doc = markdowner.convert(archive.read(path))
            doc = html_tmpl.replace("%content%", doc)
            with open(os.path.join(doc_path, path[len(doc_pref)+1:].replace(".md", ".html")), "w+") as html:
                html.write(doc)

# copy static content
shutil.copyfile("styles/style.css", doc_path+"/style.css")
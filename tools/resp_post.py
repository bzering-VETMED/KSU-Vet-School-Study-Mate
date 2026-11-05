# Post-build for the respiratory exam pages: register the service worker (sitewide rule) then apply the sitewide clean look.
# Run from repo root after any resp_*.py build:  python3 tools/resp_post.py
import glob,subprocess
SW='<script>if("serviceWorker"in navigator)navigator.serviceWorker.register("sw.js",{updateViaCache:"none"}).then(r=>r.update()).catch(()=>{})</script>'
for f in glob.glob('systems-lec3-*.html')+['systems-lec-exam3.html','systems-lecture.html']:
    s=open(f).read()
    if 'serviceWorker' not in s and '</body>' in s: open(f,'w').write(s.replace('</body>',SW+'</body>'))
subprocess.run(['python3','tools/clean.py'])

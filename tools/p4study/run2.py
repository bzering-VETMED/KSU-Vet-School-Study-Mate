import sys,runpy; sys.path.insert(0,'/home/claude/studysheets')
import build, build2
build.build=build2.build_v2; build.build_items=None
for n in sys.argv[1:]: runpy.run_path(f'/home/claude/studysheets/lab{n}.py',run_name='__main__')

import sys,runpy; sys.path.insert(0,'/home/claude/studysheets')
import build, build2
def bi(L,title,items,todo=None): build2.build_items_v2(L,title,build2.convert(L,items),todo)
build.build_items=bi
for n in sys.argv[1:]: runpy.run_path(f'/home/claude/studysheets/lab{n}.py',run_name='__main__')

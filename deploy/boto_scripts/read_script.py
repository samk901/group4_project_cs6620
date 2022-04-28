import shlex
from shlex import quote, split


def read_script(filepath):
    with open(filepath) as fp:
        lines = fp.readlines()
        out=[]
        for line in lines:
            #sh = shlex.shlex(line)
            #line= sh.quote()
            s = split(line,comments=True)
#            s = str.join(s
            s= ' '.join(s)
            if s != '' and 'echo' not in s:
                out.append(s)

        print(out)
        return out

#read_script('install_scripts/mongo_install.sh')

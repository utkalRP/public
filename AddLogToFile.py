import fileinput
import glob

files = [f for f in glob.glob('**/*.cc', recursive=True)]
numFiles = len(files)
i = 1
for f in files:
    print(f'Processing file {i} of {numFiles} :: {f}')
    i = i + 1
    
    try:
        with fileinput.FileInput(f, inplace = True, backup = '.bak') as ff:
            for line in ff:
                if ff.isfirstline():
                    print('#include "util.h"')
                if line[0] == '{':
                    print(r'{ printf("%s :: %s :: %d\n", __FILE__, __FUNCTION__, __LINE__);', end = '\n')
                else:
                    print(line, end='')
    except Exception as e:
        print(e)
        pass

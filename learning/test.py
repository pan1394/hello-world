
import sys
sys.path.append(r'../')

import learning.pmath.add as add
import crawl.pm25 as pm25

print(add.add(2,3))
print(pm25.getPM25('shanghai'))

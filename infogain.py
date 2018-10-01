import csv
import sys
import pprint
import itertools
import math
from operator import itemgetter
from collections import defaultdict

reader = csv.DictReader(open(sys.argv[1], 'rt'), delimiter=',')

objectlist = []

for row in reader:
  objectlist.append(row)

total = len(objectlist)

sortedbyclass = sorted(objectlist, key=itemgetter('Class'))

percentofclass = []

for key, value in itertools.groupby(sortedbyclass, key=itemgetter('Class')):
  counter = 0
  for i in value:
    counter += 1
  percentofclass.append({
    key: counter/total
  })

attrlist = list(objectlist[0].keys())

numofattr = defaultdict(lambda: defaultdict(list))

percentofattr = defaultdict(lambda: defaultdict(list))

for attr in attrlist:
  if (not attr == 'Class') and (not attrlist.index(attr) == 0):
    for key, value in itertools.groupby(sorted(objectlist, key=itemgetter(attr)), key=itemgetter(attr)):
      counter = 0
      val = list(value)
      for i in val:
        counter += 1
      for x, y in itertools.groupby(sorted(val, key=itemgetter('Class')), key=itemgetter('Class')):
        ylist = list(y)
        counter2 = 0
        for i in ylist:
          counter2 += 1
        percentofattr[attr][key].append({
            x : counter2/counter
        })
      numofattr[attr][key].append(counter/total)

def entropy(p):
  avg = []
  for i in p:
    for key, value in i.items():
      avg.append(-(value * math.log(value, 2)))
  entropy = sum(avg)
  return entropy

averageentropy = entropy(percentofclass)

x = defaultdict(lambda: defaultdict(list))

for a, b in percentofattr.items():
  for c, d in b.items():
    x[a][c].append(entropy(d))

z = defaultdict(list)

for a, b in x.items():
  for c, d in b.items():
    for e, f in numofattr.items():
      for g, h in f.items():
        if a == e and c == g:
          z[a].append(d[0] * h[0])

entropyperattr = defaultdict(list)

for a, b in z.items():
  entropyperattr[a].append(sum(b))
  
finallist = defaultdict(list)

for a, b in entropyperattr.items():
  finallist[a].append(averageentropy - b[0])

for a, b in sorted(finallist.items(), key=itemgetter(1), reverse=True):
  print(a, ": ", b[0])
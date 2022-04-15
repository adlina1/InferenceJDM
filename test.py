import re

text = """// DUMP pour le terme 'être vivant non humain' (eid=1483990)

<def>

</def>



// les types de noeuds (Nodes Types) : nt;ntid;'ntname'

nt;1;'n_term'

// les noeuds/termes (Entries) : e;eid;'name';type;w;'formated name' 

e;1483990;'être vivant non humain';1;4
e;124600;'mourir';1;2755
e;251694;'mourir>126720';1;238;'mourir>cesser de vivre'
e;43601;'se reproduire';1;502
e;2442;'vivre';1;3276
"""

behindNodePattern = "(?s)^.*?(?=e;eid)"


# ENTRIES PREPROCESSING
prepro1 = re.sub(behindNodePattern, '', text, flags=re.MULTILINE) # Delete all what's behind the first nodes e;[...]

print(prepro1)
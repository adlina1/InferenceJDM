import re

text = """r;rid;node1;node2;type;w 

r;14414142;48855;329657;6;90
r;250109;48855;71624;6;95
r;13879590;48855;65081;6;107
r;13722873;48855;234036;6;111
r;13980998;48855;260820;6;111
r;14028987;48855;237445;6;111
r;13919617;48855;225847;6;120
r;10927013;48855;54794;6;140
r;10921504;48855;142602;6;197
r;12045180;48855;330964;6;198
r;13065602;48855;317929;6;202
r;13065300;48855;264881;6;208
r;13065600;48855;265277;6;211
r;250108;48855;86640;6;213
r;13065607;48855;101018;6;218
r;13065594;48855;91794;6;222
r;13065297;48855;110773;6;227
r;13065291;48855;265839;6;232
r;197200;48855;63235;6;233
r;290039869;48855;2983124;6;6096



r;532515;64938;48855;6;-265
r;13472603;37752;48855;6;-265
r;29806429;261487;48855;6;-234
r;532476;168259;48855;6;-220
r;532457;72510;48855;6;-212
r;11686972;181472;48855;6;-212
r;532434;37030;48855;6;-210
r;532439;39497;48855;6;-209
r;432249988;15417538;48855;6;10
r;279027909;2321605;48855;6;25
r;357132051;2386183;48855;6;320
r;357132098;14049980;48855;6;320
r;357132131;14049958;48855;6;346
r;257186293;10367246;48855;6;349
r;82982019;2466839;48855;6;350
r;25023400;130161;48855;6;353
r;368958566;14170065;48855;6;440
r;253556491;10314499;48855;6;441
r;325743409;12694696;48855;6;445
r;115279104;5892379;48855;6;446
r;355038536;14049927;48855;6;536
r;357132083;5809356;48855;6;540
r;355092077;14049946;48855;6;541
r;357132084;2549865;48855;6;545
r;358678631;14027721;48855;6;550
r;330642018;290976;48855;6;551
r;355048181;14049938;48855;6;561
r;357132132;14049965;48855;6;561
r;357132141;14049941;48855;6;561
r;95680170;2488909;48855;6;562
r;83022281;2551953;48855;6;563
r;82982017;2428010;48855;6;564
r;111045;150;48855;6;597
r;34663238;153003;48855;6;673



"""

text2 = """// DUMP pour le terme 'chat' (eid=150)

<def>
<br />
Le Chat domestique (Felis silvestris catus) est la sous-espèce issue de la domestication du Chat sauvage, mammifère carnivore de la famille des Félidés.
</def>



// les types de noeuds (Nodes Types) : nt;ntid;'ntname'

nt;1;'n_term'
nt;8;'n_chunk'
nt;666;'n_AKI'
nt;777;'n_wikipedia'

// les noeuds/termes (Entries) : e;eid;'name';type;w;'formated name' 

e;150;'chat';1;5437
e;2488909;'york chocolat';1;0
e;2428010;'german rex';1;0

// les types de relations (Relation Types) : rt;rtid;'trname';'trgpname';'rthelp' 

rt;6;'r_isa';'générique';Il est demandé d'énumérer les GENERIQUES/hyperonymes du terme. Par exemple, 'animal' et 'mammifère' sont des génériques de 'chat'.

// les relations sortantes : r;rid;node1;node2;type;w 

r;193876834;150;142832;6;-109
r;193855652;150;140176;6;-68
r;332081826;150;213377;6;-68
r;287694433;150;362056;6;611
r;107543;150;116032;6;703
r;12986924;150;31424;6;705
r;13008626;150;220342;6;705
r;22120523;150;391581;6;705
r;123140061;150;6737046;6;705
r;12986926;150;267394;6;707
r;14400314;150;436315;6;733
r;14030357;150;237445;6;7141

// les relations entrantes : r;rid;node1;node2;type;w 

r;1614483;181472;150;6;-211
r;193727420;4455;150;6;-114
r;82960983;2425150;150;6;-67
r;114275;142832;150;6;-60
r;370924;95256;150;6;-60
r;82960980;2360117;150;6;-60
r;82960994;2428010;150;6;583

// END
"""


behindNodePatternRelations = "(?s)^.*?(?=r;rid)"
commentsPattern = "^\/\/ *.*"
deleteRest = "(?s)r;[0-9].*?(?=\n\n)"
anotherTest = "(?s)(r;[0-9]).*?(?=\n\n)"

pp1 = re.sub(behindNodePatternRelations, '', text)
pp2 = re.sub(behindNodePatternRelations, '', pp1)
relations = re.sub(commentsPattern, '', pp1, flags=re.MULTILINE)
rr = re.search(anotherTest, relations)

final = "r;rid;node1;node2;type;w\n" + rr.group(0)
print(final)


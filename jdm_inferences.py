import requests
from bs4 import BeautifulSoup
import re, csv
import numpy as np
import os.path
import pandas as pd


# User prompt
inputTermA = "toto"
inputTermB = ""
# inputTermA = input("Entrez un premier terme: \n")
# inputTermB = input("Entrez un second terme: \n")
# inputRelation = input("Entrez une relation sémantique entre les deux précédents termes: \n")

filenameEntry = f"{inputTermA}_KBE.csv"
filenameRelation = f"{inputTermA}_KBR.csv"

# print(f"Asking system for {inputTermA} {inputRelation} {inputTermB}...")

# Parsing of the JDM lexical network DUMP on a given input Term
vgm_url = f'http://www.jeuxdemots.org/rezo-dump.php?gotermsubmit=Chercher&gotermrel={inputTermA}&rel='
html_text = requests.get(vgm_url).text
soup = BeautifulSoup(html_text, 'html.parser')

# Check if the file already exists to avoid making queries each time we want to use our system
file_existsE = os.path.exists(filenameEntry)
file_existsR = os.path.exists(filenameRelation)
if (file_existsE == True):
    os.remove(filenameEntry)
    #mettre tout le reste du code ici

# Taking everything starting from the code balise
page = soup.find('code').getText()

# RegEx patterns for preprocessing 
commentsPattern = "^\/\/ *.*"
behindNodePattern = "(?s)^.*?(?=e;)"
behindNodePatternRelations = "(?s)^.*?(?=r;)"
blankLinesPattern = "^\s*$"

# ENTRIES PREPROCESSING
prepro1 = re.sub(behindNodePattern, '', page) # Delete all what's behind the first nodes e;[...]
prepro2 = re.sub(commentsPattern, '', prepro1, flags=re.MULTILINE) # Delete all the comments (whitespace can be seen as \s in regex.) 
prepro3 = re.sub("((r;.*)|(rt;.*))", '', prepro2) # Delete relations, relations types, blank lines
entries = re.sub(blankLinesPattern, '', prepro3, flags=re.MULTILINE) 
# print(entries) 

# RELATIONS PREPROCESSING
pp1 = re.sub(behindNodePatternRelations, '', page)
relations = re.sub(commentsPattern, '', pp1, flags=re.MULTILINE)
# print(relations)



# Debug to redirect to a log file
# print(page) 

# Make this as a list
textEntry = entries.split("\n")
textRelation = relations.split("\n")

# Removing single quote from the list
for singleQuote in range(0,len(textEntry)):
    textEntry[singleQuote] = textEntry[singleQuote].replace("'","")

for singleQuote in range(0,len(textRelation)):
    textRelation[singleQuote] = textRelation[singleQuote].replace("'","")


# Convert raw data into semi-structured data (in this case csv format file) and save it.
np.savetxt(filenameEntry, textEntry, delimiter =",", fmt ='%s')
np.savetxt(filenameRelation, textRelation, delimiter =",", fmt ='%s')

dfEntry = pd.read_csv(filenameEntry, on_bad_lines='skip', delimiter=';')
dfRelation = pd.read_csv(filenameRelation, on_bad_lines='skip', delimiter=';')

# print(df.columns)
# print(dfRelation[:5])
# print(dfRelation.loc[dfRelation['type']==6].node2.iloc[0]) # r entrante
# print(len(dfEntry.loc[dfEntry['type']==4]))



# un terme peut avoir plusieurs génériques, en conséquence, itérer: chercher le 1er voir si r_agent positif,
# si oui, retourner oui termA peut ... sinon chercher le 2eme, voir si r_agent positif, sinon.. jusqu'à n 

# All the "is-a" (type=6) relations of the term given in input
nbGenerics = len(dfRelation.loc[dfRelation['type']==6].node2)


# For each generic of our input term, we check all their r_agent (type=24) and see if it corresponds to the input relation 
for i in range(nbGenerics - 58):
    
    # We take the generic
    check = dfEntry.loc[dfEntry['eid']==dfRelation.loc[dfRelation['type']==6].node2.iloc[i]]
    new_term = check.name.values[0]

    fileName = f"{new_term}_KBR.csv"
    file_exists = os.path.exists(fileName)

    # Avoid making queries each time we want to use our system
    if (file_exists == True):
        dfTerm = pd.read_csv(fileName, on_bad_lines='skip', delimiter=';')
        # We search for all the r_agent relations of the first generic (index i)
        for j in range(len(dfTerm.loc[dfTerm['type']==24])):
            # At the first matching with the termB (e.g voler), then it succeeds
            if(dfTerm.loc[dfTerm['type']==24].name.values[j] == inputTermB):
                print("true")
            # Otherwise if none of them match then we can infer it's false
            else:
                print("false")

    # If the file doesn't exist
    else:
        new_url = f'http://www.jeuxdemots.org/rezo-dump.php?gotermsubmit=Chercher&gotermrel={new_term}&rel='
        html_txt = requests.get(new_url).text
        soup = BeautifulSoup(html_txt, 'html.parser')
        paGe = soup.find('code').getText()

        print("later")
        #mettre tt ce qui a été fait au dessus, parser le fichier etc, le sauvegarder 
        # faire une fonction (bcp plus simple)
        # rajouter un nouveau filenameEntry = f"{inputTermA}_KBE.csv"









# inférence déductive : termeA r_agent termeB -> termA isA [xx]  &&&&&&  [xx] r_agent termB
#                               oui car pigeon r_isa oiseau et oiseau r_agent-1 voler


# les noeuds/termes (Entries) :
# chat
# e;213857;'voler>167847';1;276;'voler>déplacement aérien'
# e;eid;'name';type;w;'formated name'


#  les relations sortantes : 
#r;rid;node1;node2;type;w 
# r;211553581;150;213857;24;-30

# // les types de relations (Relation Types) : rt;rtid;'trname';'trgpname';'rthelp' 
# rt;0;'r_associated';'idée associée';Il est demandé d'énumérer les termes les plus étroitement associés au mot cible... Ce mot vous fait penser à quoi ?
# rt;1;'r_raff_sem';'raffinement sémantique';Raffinement sémantique vers un usage particulier du terme source
# rt;3;'r_domain';'domaine';Il est demandé de fournir des domaines relatifs au mot cible. Par exemple, pour 'corner', on pourra donner les domaines 'football' ou 'sport'.
# rt;4;'r_pos';'POS';Partie du discours (Nom, Verbe, Adjectif, Adverbe, etc.)
# rt;5;'r_syn';'synonyme';Il est demandé d'énumérer les synonymes ou quasi-synonymes de ce terme.
# rt;6;'r_isa';'générique';Il est demandé d'énumérer les GENERIQUES/hyperonymes du terme. Par exemple, 'animal' et 'mammifère' sont des génériques de 'chat'.
# rt;9;'r_has_part';'partie';Il faut donner des PARTIES/constituants/éléments (a pour méronymes) du mot cible. Par exemple, 'voiture' a comme parties : 'porte', 'roue', 'moteur', ...
# rt;10;'r_holo';'tout';Il est démandé d'énumérer des 'TOUT' (a pour holonymes)  de l'objet en question. Pour 'main', on aura 'bras', 'corps', 'personne', etc... Le tout est aussi l'ensemble comme 'classe' pour 'élève'.
# rt;11;'r_locution';'locution';A partir d'un terme, il est demandé d'énumérer les locutions, expression ou mots composés en rapport avec ce terme. Par exemple, pour 'moulin', ou pourra avoir 'moulin à vent', 'moulin à eau', 'moulin à café'. Pour 'vendre', on pourra avoir 'vendre la peau de l'ours avant de l'avoir tué', 'vendre à perte', etc..
# rt;13;'r_agent';'action>agent';L'agent (qu'on appelle aussi le sujet) est l'entité qui effectue l'action, OU la subit pour des formes passives ou des verbes d'état. Par exemple, dans - Le chat mange la souris -, l'agent est le chat. Des agents typiques de 'courir' peuvent être 'sportif', 'enfant',... (manger r_agent chat)
# rt;15;'r_lieu';'chose>lieu';Il est demandé d'énumérer les LIEUX typiques où peut se trouver le terme/objet en question. (carotte r_lieu potager)
# rt;17;'r_carac';'caractéristique';Pour un terme donné, souvent un objet, il est demandé d'en énumérer les CARACtéristiques (adjectifs) possibles/typiques. Par exemple, 'liquide', 'froide', 'chaude', pour 'eau'.
# rt;18;'r_data';'r_data';Informations diverses (plutôt d'ordre lexicales)
# rt;19;'r_lemma';'r_lemma';Le lemme (par exemple 'mangent a pour lemme  'manger' ; 'avions' a pour lemme 'avion' ou 'avoir').
# rt;23;'r_carac-1';'caractéristique-1';Quels sont les objets (des noms) possédant typiquement/possiblement la caractérisque suivante ? Par exemple, 'soleil', 'feu', pour 'chaud'.
# rt;24;'r_agent-1';'agent typique-1';Que peut faire ce SUJET ? (par exemple chat => miauler, griffer, etc.) (chat r_agent-1 manger)
# rt;27;'r_domain-1';'domaine-1';inverse de r_domain : à un domaine, on associe des termes
# rt;28;'r_lieu-1';'lieu>chose';A partir d'un lieu, il est demandé d'énumérer ce qui peut typiquement s'y trouver. Par exemple : Paris r_lieu-1 tour Eiffel
# rt;32;'r_sentiment';'sentiment';Pour un terme donné, évoquer des mots liés à des SENTIMENTS ou des EMOTIONS que vous pourriez associer à ce terme. Par exemple, la joie, le plaisir, le dégoût, la peur, la haine, l'amour, l'indifférence, l'envie, avoir peur, horrible, etc.
# rt;35;'r_meaning/glose';'glose/sens/signification';Quels SENS/SIGNIFICATIONS pouvez vous donner au terme proposé. Il s'agira de termes (des gloses) évoquant chacun des sens possibles, par exemple : 'forces de l'ordre', 'contrat d'assurance', 'police typographique', ... pour 'police'.
# rt;36;'r_infopot';'information potentielle';Information sémantique potentielle
# rt;55;'r_against';'s'oppose à';A quoi le terme suivant S'OPPOSE/COMBAT/EMPECHE ? Par exemple, un médicament s'oppose à la maladie.
# rt;56;'r_against-1';'a comme opposition';Inverse de r_against (s'oppose à) - a comme opposition active (S'OPPOSE/COMBAT/EMPECHE). Par exemple, une bactérie à comme opposition antibiotique.
# rt;106;'r_color';'couleur';A comme couleur(s)... chat r_color noir
# rt;128;'r_node2relnode-in';'r_node2relnode-in';Relation entre un noeud (quelconque) et un noeud de relation (type = 10)  - connecte le noeud d'entrée - permet de rendre le graphe connexe même avec les annotations de relations
# rt;140;'r_node2relnode-out';'r_node2relnode-out';Relation entre un noeud (quelconque) et un noeud de relation (type = 10) - connecte le noeud de sortie - permet de rendre le graphe connexe même avec les annotations de relations
# rt;170;'r_sing_from';'r_sing_from';La forme au singulier d'un terme. Exemple : chevaux r_sing_from cheval (pas de relation inverse)
# rt;333;'r_translation';'r_translation';Traduction vers une autre langue.
# rt;444;'r_link';'r_link';Lien vers une ressource externe (WordNet, RadLex, UMLS, Wikipedia, etc...)
# rt;555;'r_cooccurrence';'r_cooccurrence';co-occurences (non utilisée)
# rt;666;'r_aki';'r_aki';(TOTAKI) equivalent pour TOTAKI de l'association libre
# rt;777;'r_wiki';'r_wiki';Associations issues de wikipedia...
# rt;999;'r_inhib';'r_inhib';relation d'inhibition, le terme inhibe les termes suivants... ce terme a tendance à exclure le terme associé.
# rt;2000;'r_raff_sem-1';'r_raff_sem-1';Inverse de r_raff_sem (automatique)
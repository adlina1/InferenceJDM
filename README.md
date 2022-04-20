# InferenceJDM
InferenceJDM is a system to make inferences through textual data of the serious game "JeuxDeMots".
The data of JDM has been fed by games of thousands of people over a long period of time.

This tool aims to make inferences of different kind from terms of the knowledge base of Jeux de mots. <br>
To use the script, just run ``` python3 jdm_inferences.py ``` and you will be ask to enter two terms and a relation between those terms. <br> <br>
Three kind of inferences has been taken into account: 

* **Deductive inference** (we searched for the generics of our first input term to infer) <br> e.g 
*Une tortue peut-elle marcher ? oui car tortue est un reptile et un reptile peut marcher*

* **Inductive inference** (we searched for the specifics of our second input term to infer) <br> e.g 
*Un chat peut-il griffer ? oui car un chat est un sacré de birmanie et un sacré de birmanie peut griffer*

* **Transitive inference** (xRy and yRz => xRz, where R is any relationship between the terms, can be r_has_part, r_lieu, etc) <br> e.g 
*La Tour Eiffel est-elle en France? Oui car la Tour Eiffel est à Paris, et Paris et en France*

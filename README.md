Dupa ce am creat un chatbot si am reusit sa il introducem intr-o conversatie pe Slack, am experimentat cu modul in care acesta
citeste mesajele si ce face cand este "chemat". De exemplu am definit un tipar pentru "do nr1 op nr2" cu care bot-ul reuseste sa efectueze
calculele respective (screenshot in pdf la final).<br />
Dupa etapa asta am trecut la procesarea de text folosind functii din libraria AllenNLP, insa asta insemna tot un control destul de fin
asupra textului care vine de la utilizatorul si nu ar fi parut un proces prea automat si manual.<br />
De aceea, am trecut la a incerca analiza semantica pe parti de propozitie:<br />
"I want a pizza" => NP("I") si VP("want a pizza") => NP->Pronume("I") si [VP->Verb("want") si VP->NP->Substantiv("a pizza")]<br />
Astfel vom cauta verbe din care sa extragem intentia cum e aici cu "want" si dorinta de a avea ceva, ceea ce urmeaza acestui verb.<br />
Mai trebuie sa vedem si ce facem daca apar alte cuvinte intre verb si mancarea dorita => ar trebui sa il invatam tipurile de mancaruri,
de la general la particular, si sa reuseasca sa faca asocieri daca cumva inca nu a intalnit un anumit fel de mancare.<br />
<br />
Tudor Cocos & Romina Baila

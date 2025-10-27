headerNames = ['Num','Crom.','Nome','Tipo','Abilità','Mosse da Uova','Costo','Tot','PS','Att','Dif','ASp','DSp','Vel']
altText = ['Mosse','Solo Normale','Solo Nascosta','Solo Passiva','Inserisci','Pot','Prec','PP',
           'Vai ai filtri','Memoria','Evoluzioni','Mossa da Uova','Rara Mossa da Uova',
           'Comuni','Mega','Ultra','MT','L.','Evo','Uova']
catToName = ['Tipo','Abilità','Mossa','Gen','Costo','Genere','Modalità','Uova','Varianti Cromatiche','Bioma','Evoluzioni','Etichetta']
infoText = [
    'Amicizia per Caramella', 'Passiva', 'Riduzione Costo', 'Uovo per Specie', 'Abilità Nascosta', 
    'Solo da Uova', 'Solo Baby', 'Pokémon Paradosso', 'Cambio Forma', 'Biomi', 'Filtri'
]
biomeText = ['Comune','Non Comune','Raro','Super Raro','Ultra Raro',
             'Boss','Com.','NC','Raro','SR','UR','Alba','Giorno','Tramonto','Notte']
biomeLongText = [
    '<b>This form is only available via <span style="color:rgb(140, 130, 240);">Form Change</span>.</b> Other forms can be encountered in the biomes shown.<br>',
    '<b>This Pokemon is <span style="color:rgb(143, 214, 154);">Egg Exclusive</span>.</b><br>It does not appear in any biomes, and can only be obtained from eggs.',
    '<b>This is a <span style="color:rgb(216, 143, 205);">Baby Pokemon</span>.</b><br>It does not appear in any biomes, but can be unlocked by encountering its evolution.',
    '<b>This <span style="color:rgb(239, 131, 131);">Paradox Pokemon</span> is <span style="color:rgb(143, 214, 154);">Egg Exclusive</span>.</b><br>It can only be obtained from eggs, but can afterward be caught in Classic mode.',
    'This Pokemon can only be caught after obtaining <b><span style="color:rgb(239, 131, 131);">All Other Pokemon</span></b>.<br>It does not appear in standard eggs.',
    '<b>This form is unobtainable.</b>',
]
warningText = [
    'Restricted to Pokemon that have shiny variants.',
    'Abilities are restricted to only Main Abilities.',
    'Abilities are restricted to only Hidden Abilities.',
    'Abilities are restricted to only Passive Abilities.',
    '<b>There are no Pokemon that match the filters and the search term.</b><br>Adding another filter may change the results.',
    '<b>Click on a suggestion to filter it.</b><br>Filter preview is only for Species/Types/Abilities.',
    '<b>There are no Pokemon that match the filters and the search term.</b><br>Try a different combination.',
    '<b>There are no Pokemon that match the filters.</b><br>Remove filters, or change the connections to "OR".',
    '<b>There are no Pokemon or filters that match the search term.</b><br>Please check your spelling and try again.',
    'Click to see the instructions.',
]
procToDesc = [
    "Attacco Utente",
    "Difesa Utente",
    "Att. Sp. Utente",
    "Dif. Sp. Utente",
    "Velocità Utente",
    "Precisione Utente",
    "Elusione Utente",
    "Attacco",
    "Difesa",
    "Att. Sp.",
    "Dif. Sp.",
    "Velocità",
    "Precisione",
    "Elusione",
    "Avvelenato",
    "Iperavvelenato",
    "Sonno",
    "Congelamento",
    "Paralisi",
    "Scottatura",
    "Confuso",
    "Tentennando",
    "Att/Dif/AttSp/DifSp/Vel Utente",
    "Avvelenato/Paralisi/Sonno",
    "Scottatura/Paralisi/Congelamento",
    "Astrale Att/AttSp Utente",
    "Danno",
    "Priorità"
]
tagToDesc = [
    "Bersagli: Nemico Casuale",
    "Bersagli: Tutti i Nemici",
    "Bersagli: Intero Campo",
    "Alta Probabilità di Brutto Colpo",
    "Colpo Critico Garantito",
    "Tasso di Colpo Critico +2",
    "Attacco Utente al massimo",
    "Consuma il 33% dei PS",
    "Consuma il 50% dei PS",
    "Contraccolpo 50% dei PS",
    "Contraccolpo 50% del danno",
    "Contraccolpo 33% del danno",
    "Contraccolpo 25% del danno",
    "30% infligge danno doppio",
    "Non utilizzato",
    "Cura il 100% del danno inflitto",
    "Cura il 75% del danno inflitto",
    "Cura il 50% del danno inflitto",
    "Cura in base all'Attacco del bersaglio",
    "Cura gli Status",
    "Cura il Sonno",
    "Cura il Congelamento",
    "Cura la Scottatura",
    "Nessun effetto su Erba/Sobrio",
    "Non può seminare Pokémon Erba",
    "Attiva l'abilità Primacura",
    "Attiva l'abilità Sincrodanza",
    "Attiva l'abilità Vento Propizio",
    "Potenza aumentata da Affilama",
    "Potenza aumentata da Ferropugno",
    "Potenza aumentata da Megalancio",
    "Potenza aumentata da Ferromascella",
    "Potenza aumentata da Temerarietà",
    "Nessun effetto su Antiproiettile",
    "Impedito da Umidità",
    "Mossa basata sul suono",
    "Ignora Sostituto",
    "Ignora Abilità",
    "Ignora Protezione",
    "L'utente viene sostituito",
    "Il bersaglio viene sostituito",
    "Colpisce 2 volte",
    "Colpisce 3 volte",
    "Colpisce 10 volte",
    "Colpisce da 2 a 5 volte",
    "Si ripete per 2-3 turni",
    "Rimuove gli ostacoli",
    "Intrappola e danneggia il bersaglio",
    "Non può essere annullato",
    "Non può essere sostituito",
    "Non può essere ignorato",
    "Non può essere deviato",
    "Non può essere riflesso",
    "Colpisce sempre sotto la pioggia",
    "L'utente non può essere sostituito",
    "Il bersaglio non può essere sostituito",
    "Mossa KO in un colpo",
    "Modificato contro i Boss",
    "Nessun effetto sui Boss",
    "Abilità Esca",
    "Mossa da Contatto",
    "Parzialmente Implementata",
    "Non Implementata",
]
helpMenuText = """
<b>This is a <span style="color:rgb(140, 130, 240);">fast and powerful search</span> for PokeRogue</b>
<hr>
<p style="margin: 10px; font-weight: bold;">Use the <span style="color:rgb(140, 130, 240);">Search Bar</span> to add filters:<br></p>
<p style="margin: 10px; font-weight: bold;"><span style="color:${typeColors[9]};">${catToName[0]}</span>, 
<span style="color:${fidToColor(fidThreshold[0])[0]};">${catToName[1]}</span>,
<span style="color:${fidToColor(fidThreshold[1])[0]};">${catToName[2]}</span>,
<span style="color:${fidToColor(fidThreshold[2])[0]};">${catToName[3]}</span>,
<span style="color:${fidToColor(fidThreshold[3])[0]};">${catToName[4]}</span>,
<span style="color:${fidToColor(fidThreshold[4])[0]};">${catToName[5]}</span>,<br>
<span style="color:${fidToColor(fidThreshold[5])[1]};">${catToName[6]}</span>,
<span style="color:${eggTierColors(2)};">${catToName[7]}</span>,
<span style="color:${fidToColor(fidThreshold[7])[0]};">${headerNames[1]}</span>, or
<span style="color:${fidToColor(fidThreshold[8])[0]};">${catToName[9]}</span></p>
Combine multiple filters to get what you want <br>
<span style="color:rgb(145, 145, 145);">Click between filters to use the "OR" condition</span>
<hr>
<p style="margin: 10px; font-weight: bold;">Click the <span style="color:rgb(140, 130, 240);">Headers</span> to sort results:</p>
Click the <b>${headerNames[1]}</b> column to see only shiny variants
<p style="margin: 10px;">Click the <b>${headerNames[4]}</b> column to restrict to one slot:<br>
<b>Main Abilities</b>, 
<span style="color:rgb(240, 230, 140); font-weight: bold;">Hidden Ability</span>, or 
<span style="color:rgb(140, 130, 240); font-weight: bold;">Passive</span></p>
<b>${headerNames[5]}</b> are shown as <b>${fidToName[fidThreshold[6]]}</b> and <span style="color:rgb(240, 230, 140); font-weight: bold;">${fidToName[fidThreshold[6]+1]}</span><br> 
<span style="color:rgb(145, 145, 145);">Click the header to switch to <b>${infoText[9]}</b> instead<br>
This column will also show <b>filtered ${altText[0]}/${infoText[9]}</b></span>
<p style="margin: 10px;"><b>${headerNames[6]}</b> column shows rarity color of <b>${catToName[7]}</b>:<br> 
<b>${fidToName[fidThreshold[6]]}</b>, <span style="color:rgb(131, 182, 239);"><b>${fidToName[fidThreshold[6]+1]}</b></span>, <span style="color:rgb(240, 230, 140);"><b>${fidToName[fidThreshold[6]+2]}</b></span>, <span style="color:rgb(239, 131, 131);"><b>${fidToName[fidThreshold[6]+3]}</b></span>, <span style="color:rgb(216, 143, 205);"><b>${fidToName[fidThreshold[6]+4]}</b></span></p>
<hr>
<p style="margin: 10px; font-weight: bold;">Click on a <span style="color:rgb(140, 130, 240);">Pokemon</span> entry to see details:
<span style="color:rgb(145, 145, 145);">Moves, Abilities, Cost, Image, Pin, Name</span></p>
<p style="margin: 10px;">
Click a Pokemon's <b>Name</b> to see their full moveset.<br>
Color of <b>Pow</b> shows <span style="color:${col.or}; font-weight: bold;">Physical</span> or <span style="color:${col.bl}; font-weight: bold;">Special</span> damage<br>
Color of <b>Acc</b> shows <span style="color:${col.re}; font-weight: bold;">Multi-target</span> moves
</p>
<hr style="margin-bottom: 10px;">
<span style="color:rgb(145, 145, 145); font-size:11px">This site was created by Sandstorm, with a lot of hard work. I do not store any cookies or collect any personal data. Images and game data are from the PokeRogue GitHub. All asset rights are retained by their original creators.</span>
"""
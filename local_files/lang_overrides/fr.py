
headerNames = ['N°','Chrom.','Nom','Type','Talents','Capacités Œuf','Cout','Total','PV','Atq','Déf','ASp','DSp','Vit']
altText = ['Capacités','Principaux','Caché','Passif','Chercher','Puis.','Préc.','PP','Ajouter aux filtres','Champi Mémoriel',
           'Évolution','Capacités Œuf','Rare Capac. Œuf','Commun','Super','Hyper','CT','N.','Évo','Œuf']
catToName = ['Type','Talent','Capacité','Gen','Cout','Sexe','Mode',
             'Œuf','Variantes Chromatique','Biome','Lié à','Étiquette']
catToName = ['Type','Talent','Capacité','Gen','Cout','Œuf','Mode',
             'Évolution','Forme','Biome','Lié à','Variantes Chromatique','Étiquette']
infoText = ['Bonheur par Bonbon','Passif','Cout réduit','Acheter un Œuf','Talent Caché',
            'Exclusif aux Œufs','Exclusif aux Bébés','Pokémon Paradoxe','Changement de forme','Biomes','Filtres',
            'Réduit après ## œufs','par Niveau','par Œuf','par CT']
biomeText = ['Commun','Peu Commun','Rare','Super Rare','Hyper Rare','Boss','Com.','PC','Rare','SR','HR',
             'Aube','Jour','Crépuscule','Nuit']
biomeLongText = [
    '<b>Forme disponible uniquement par <span style="color:rgb(140, 130, 240);">changement de forme</span>.</b> Les autres formes peuvent être rencontrées dans les biomes affichés.',
    '<b>Ce Pokémon est disponible <span style="color:rgb(143, 214, 154);">exclusivement pas Œuf</span>.</b><br>Il n’apparait dans aucun biome et ne peut être trouvé que dans les Œufs.',
    '<b>Ce Pokémon est un <span style="color:rgb(216, 143, 205);">bébé</span>.</b><br>Il n’apparait dans aucun biome mais peut être débloqué en rencontrant son évolution.',
    '<b>Ce <span style="color:rgb(239, 131, 131);">Pokémon Paradoxe</span> est <span style="color:rgb(143, 214, 154);">exclusif aux Œufs</span>.</b><br>Il ne peut être trouvé que dans les Œufs, mais peut être obtenu plus tard dans le mode Classique.',
    'Ce Pokémon ne peut être obtenu qu’après avoir obtenu <b><span style="color:rgb(239, 131, 131);">tous les autres Pokémon</span></b>.<br>Il n’apparait par dans les Œuf standards.',
    '<b>This form is unobtainable.</b>'
]
phrases = {
    'exclusive': 'Exclusif',
    'new': 'Nouvelle',
    'tag': 'Attribut',
    'theEnd': 'La Fin',
    'fullyEvolved': 'Entièrement évolué',
    'formBase': 'Base',
    'formMega': 'Méga',
    'formNewMega': 'Nouveau Méga',
    'formGiga': 'Giga',
    'formTransformed': 'Transformé',
    'lureAbility': 'Talent d’Appât',
    'ignoresAbilities': 'Ignore les Talents',
    'electricImmunity': 'Immunité Électrik',
    'fireImmunity': 'Immunité Feu',
    'waterImmunity': 'Immunité Eau',
    'rainAbility': 'Talent Pluie',
    'sandAbility': 'Talent Tempête de Sable',
    'snowAbility': 'Talent Neige',
    'sunAbility': 'Talent Soleil',
    'targetSwitchesOut': 'Force le Changement',
    'spreadMoves': 'Attaques de Zone',
}
substitutions = [
    ['Osmose Équine','Osmose'],
    ['Masque de la ',''],
    ['Masque du ',''],
    ['Masque ',''],
    ['Rassemblement Forme','Rassemblement'],
    [' Mode Transe',' Transe'],
]
warningText = [
    'Limité aux Pokémon qui ont des variants chromatiques.',
    'Talents limités qu’aux talents principaux.',
    'Talents limités qu’aux talents cachés.',
    'Talents limités qu’aux passifs.',
    '<b>Aucun Pokémon ne correspond aux filtres utilisés.</b><br>Modifier les filtres pourrait changer les résultats.',
    '<b>Cliquez sur un suggestion poutr la filtrer.</b><br>La prévisualisation du filtre est uniquement pour les espèces/types/talents.',
    '<b>Aucun Pokémon ne correspond aux filtres ni aux termes saisis.</b><br>Essayez d’autres combinaisons.',
    '<b>Aucun Pokémon ne correspond aux filtres.</b><br>Retiez les filtres ou changer la connexion sur "OR".',
    '<b>Aucun Pokémon ne correspond aux filtres ni aux termes saisis.</b><br>Vérifiez les erreurs de frappe et réessayez.',
    'Cliquez pour voir les instructions.'
]
procToDesc = [
    "Atq du lanceur",
    "Déf du lanceur",
    "AtqSp du lanceur",
    "DéfSp du lanceur",
    "Vitesse du lanceur",
    "Précison du lanceur",
    "Esquive du lanceur",
    "Atq",
    "Déf",
    "AtqSp",
    "DéfSp",
    "Vitesse",
    "Précison",
    "Esquive",
    "Empoisonne",
    "Empoisonne gravement",
    "Endort",
    "Gèle",
    "Paralyse",
    "Brule",
    "Rend confus",
    "Apeure",
    "User Atq/Déf/AtS/DéS/Vit",
    "Poison/Para/Sommeil",
    "Brule/Para/Gel",
    "Lanceur Stellaire Atq/AtqSp",
    "Dégat",
    "Priorité"
]
tagToDesc = [
    "Cible : Ennemi au hasard",
    "Targets : Tous les enemies",
    "Targets : Tous les Pokémon",
    "Taux coup critique élevé",
    "Coup critique garanti",
    "Coup critique du lanceur +2",
    "Atq du lanceur au max",
    "Coute 33% des PV",
    "Coute 50% des PV",
    "Recul 50% des PV",
    "Recul 50% des dégâts",
    "Recul 33% des dégâts",
    "Recul 25% des dégâts",
    "30% dégâts doublés",
    "Inutilisé",
    "Soigne 100% dégâts infligés",
    "Soigne 75% dégâts infligés",
    "Soigne 50% dégâts infligés",
    "Soin basé sur Atq du lanceur",
    "Soigne problèmes de statut",
    "Soin sommeil",
    "Soin gel",
    "Soin brulure",
    "Aucun effet sur Plante/Envelocape",
    "Plante de grain impossible sur types Plante",
    "Active le talent Prioguérison",
    "Active le talent Danseuse",
    "Active le talent Aéroporté",
    "Boosté par Incisif",
    "Boosté par Poing de Fer",
    "Boosté par Méga Blaster",
    "Boosté par Prognathe",
    "Boosté par Téméraire",
    "Aucun effet sur Pare-Balles",
    "Empêché par Moiteur ability",
    "Capacité sonore",
    "Ignore Clonage",
    "Ignore les talents",
    "Ignore Abri",
    "Rappelle le lanceur",
    "Rappelle la cible",
    "Frappe 2 fois",
    "Frappe 3 fois",
    "Frappe 10 fois",
    "Frappe 2 à 5 fois",
    "Dure de 2 à 3 tours",
    "Retire les pièges",
    "Piège et blesse la cible",
    "Ne peut pas être annulée",
    "Ne peut pas être remplacée",
    "Ne peut pas être ignorée",
    "Ne peut pas être redirigée",
    "Ne peut pas être renvoyée",
    "Frappe toujours s'il pleut",
    "Le lanceur ne peut pas être remplacé",
    "La cible ne peut pas être remplacée",
    "K.-O. en 1 coup",
    "Altérée contre les Boss",
    "Aucun effet sur les Boss",
    "Trompe le talent",
    "Contact",
    "Partiellement implémenté",
    "Non-implementé"
]
helpMenuText = """
<b><span style="color:rgb(140, 130, 240);">Recherche rapide et puissante</span> pour PokeRogue</b>
<hr>
<p style="margin: 10px; font-weight: bold;">Ajoutez des filtres via la <span style="color:rgb(140, 130, 240);">barre de recherche</span>:<br></p>
<p style="margin: 10px; font-weight: bold;"><span style="color:${typeColors[9]};">${catToName[0]}</span>, 
<span style="color:${fidToColor(fidThreshold[0])[0]};">${catToName[1]}</span>,
<span style="color:${fidToColor(fidThreshold[1])[0]};">${catToName[2]}</span>,
<span style="color:${fidToColor(fidThreshold[2])[0]};">${catToName[3]}</span>,
<span style="color:${fidToColor(fidThreshold[3])[0]};">${catToName[4]}</span>,
<span style="color:${fidToColor(fidThreshold[4])[0]};">${catToName[5]}</span>,<br>
<span style="color:${fidToColor(fidThreshold[5])[1]};">${catToName[6]}</span>,
<span style="color:${eggTierColors(2)};">${catToName[7]}</span>,
<span style="color:${fidToColor(fidThreshold[7])[0]};">${headerNames[1]}</span>, ou
<span style="color:${fidToColor(fidThreshold[8])[0]};">${catToName[9]}</span></p>
Combinez plusieurs filtres pour affiner la recherche <br>  
<span style="color:rgb(145, 145, 145);">Cliquez entre eux pour correspondre à l’un ou l’autre</span>
<hr>
<p style="margin: 10px; font-weight: bold;">Cliquez sur les <span style="color:rgb(140, 130, 240);">Entêtes</span> pour trier les résultats</p>
<b>Chromatique</b> peut filtrer les variantes chromatique
<p style="margin: 10px;"><b>${headerNames[4]}</b> peut filtrer un seul slot de talents:<br>
<b>Talents principaux</b>,
<span style="color:rgb(240, 230, 140); font-weight: bold;">Talent caché</span>, ou
<span style="color:rgb(140, 130, 240); font-weight: bold;">Passif</span></p>
<b>${headerNames[5]}</b> affichées comme <b>${fidToName[fidThreshold[6]]}</b> et <span style="color:rgb(240, 230, 140); font-weight: bold;">${fidToName[fidThreshold[6]+1]}</span><br>
<span style="color:rgb(145, 145, 145);">Peut aussi afficher la source des mouvements filtrés</span>
<p style="margin: 10px;"><b>${headerNames[6]}</b> affiche la couleur de <b>${catToName[7]}</b>:<br>
<b>${fidToName[fidThreshold[6]]}</b>, <span style="color:rgb(131, 182, 239);"><b>${fidToName[fidThreshold[6]+1]}</b></span>, <span style="color:rgb(240, 230, 140);"><b>${fidToName[fidThreshold[6]+2]}</b></span>, <span style="color:rgb(239, 131, 131);"><b>${fidToName[fidThreshold[6]+3]}</b></span>, <span style="color:rgb(216, 143, 205);"><b>${fidToName[fidThreshold[6]+4]}</b></span></p>
<hr>
<p style="margin: 10px;">Cliquez pour <span style="color:rgb(240, 230, 140); font-weight: bold;">Épingler</span>, ou voir <a href="https://wiki.pokerogue.net/start" target="_blank"><b>Wiki</b></a> ou <span style="color:${fidToColor(fidThreshold[7])[0]}; font-weight: bold;">Variantes</span></p>
<p style="margin: 10px;">Cliquez un <span style="color:rgb(140, 130, 240); font-weight: bold;">${catToName[1]}</span> ou <span style="color:rgb(140, 130, 240); font-weight: bold;">${catToName[2]}</span> pour descriptions</p>
<hr style="margin-bottom: 10px;">
<span style="color:rgb(145, 145, 145); font-size:11px">Site créé par Sandstorm, et traduit de l'anglais. Aucune données personnelles collectées. Les images et données proviennent du Github de PokéRogue. Tous droits sont réservés à leurs créateurs respectifs.</span>
"""
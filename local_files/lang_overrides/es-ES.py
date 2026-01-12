headerNames = ['Dex','Shiny','Especie','Tipos','Habilidades','Mov. Huevo','Coste','BST','PS','Atq','Def','AtE','DfE','Vel']
altText = ['Movimientos','Solo Principal','Solo Oculta','Solo Pasiva','Buscar','Pot.','Prec.','PP','Añadir a filtros','Recuerdo','Evolución','Mov. Huevo','Mov. Huevo Raro','Común','Súper','Ultra','MT','Nv.','Evo','Huevo']
catToName = ['Tipo','Habilidad','Movimiento','Gen','Coste','Género','Modo','Nivel de Huevo','Variantes Shiny','Bioma','Relacionado con','Etiqueta']
biomeText = ['Común','Poco Común','Raro','Super Raro','Ultra Raro','Jefe','Com.','PCom.','Raro','SR','UR','Amanecer','Día','Atardecer','Noche']
infoText = ['Amistad por Caramelo','Pasiva','Reducción de Coste','Huevo de Especie','Habilidad Oculta',
            'Exclusivo de Huevo','Exclusivo de Cría','Pokémon Paradoja','Cambio de Forma','Biomas','Filtros',
            'Reducido después de ## huevos','por Nivel','por Huevo','por MT']
helpMenuText = """
<b><span style="color:rgb(140, 130, 240);">Búsqueda rápida y potente</span> para PokeRogue</b>
<hr>
<p style="margin: 10px; font-weight: bold;">Usa la <span style="color:rgb(140, 130, 240);">Barra de Búsqueda</span> para añadir filtros:<br></p>
<p style="margin: 10px; font-weight: bold;"><span style="color:${typeColors[9]};">${catToName[0]}</span>, 
<span style="color:${fidToColor(fidThreshold[0])[0]};">${catToName[1]}</span>,
<span style="color:${fidToColor(fidThreshold[1])[0]};">${catToName[2]}</span>,
<span style="color:${fidToColor(fidThreshold[2])[0]};">${catToName[3]}</span>,
<span style="color:${fidToColor(fidThreshold[3])[0]};">${catToName[4]}</span>,<br>
<span style="color:${fidToColor(fidThreshold[4])[0]};">${catToName[5]}</span>,
<span style="color:${fidToColor(fidThreshold[5])[1]};">${catToName[6]}</span>,
<span style="color:${eggTierColors(2)};">${catToName[7]}</span>,
<span style="color:${fidToColor(fidThreshold[7])[0]};">${headerNames[1]}</span>, 
<span style="color:${fidToColor(fidThreshold[8])[0]};">${catToName[9]}</span></p>
Puedes combinar múltiples filtros<br>
<span style="color:rgb(145, 145, 145);">Haz clic entre filtros para usar la condición “o”</span>
<hr>
<p style="margin: 10px; font-weight: bold;">Haz clic en las <span style="color:rgb(140, 130, 240);">Cabeceras</span> para reordenar</p>
Columna <b>${headerNames[1]}</b> puede filtrar las variantes
<p style="margin: 10px;">Columna <b>${headerNames[4]}</b> puede limitarse a:<br>
<b>Habilidad Principal</b>, 
<span style="color:rgb(240, 230, 140); font-weight: bold;">${infoText[4]}</span>, 
<span style="color:rgb(140, 130, 240); font-weight: bold;">${infoText[1]}</span></p>
<b>${headerNames[5]}</b> aparecen como <b>${fidToName[fidThreshold[6]]}</b> y <span style="color:rgb(240, 230, 140); font-weight: bold;">${fidToName[fidThreshold[6]+1]}</span><br> 
<span style="color:rgb(145, 145, 145);">Haz clic en Mov. Huevo para ver biomas<br>Muestra los movimientos o biomas filtrados</span>
<p style="margin: 10px;">Columna <b>${headerNames[6]}</b> coloreado por <b>${catToName[7]}</b>:<br> 
<b>${fidToName[fidThreshold[6]]}</b>, <span style="color:rgb(131, 182, 239);"><b>${fidToName[fidThreshold[6]+1]}</b></span>, <span style="color:rgb(240, 230, 140);"><b>${fidToName[fidThreshold[6]+2]}</b></span>, <span style="color:rgb(239, 131, 131);"><b>${fidToName[fidThreshold[6]+3]}</b></span>, <span style="color:rgb(216, 143, 205);"><b>${fidToName[fidThreshold[6]+4]}</b></span></p>
<hr>
<p style="margin: 10px;">Haz clic para <span style="color:rgb(240, 230, 140); font-weight: bold;">Fijar</span> Pokémon, ver <a href="https://wiki.pokerogue.net/start" target="_blank"><b>Wiki</b></a> o <span style="color:${fidToColor(fidThreshold[7])[0]}; font-weight: bold;">Shiny</span></p>
<p style="margin: 10px;">Haz clic en 
<span style="color:${col.wh}; font-weight: bold;">el Nombre</span>, 
<span style="color:${fidToColor(fidThreshold[3])[0]}; font-weight: bold;">${headerNames[6]}</span>, 
<span style="color:${col.pu}; font-weight: bold;">${catToName[1]}</span> o 
<span style="color:${col.pu}; font-weight: bold;">${catToName[2]}</span> para ver más detalles</p>
<hr style="margin-bottom: 10px;">
<span style="color:rgb(145, 145, 145); font-size:11px">Este sitio fue creado por Sandstorm, con mucho esfuerzo. No almaceno cookies ni recojo ningún dato personal. Las imágenes y los datos del juego provienen del GitHub de PokeRogue. Todos los derechos de los recursos pertenecen a sus creadores originales.</span>
"""
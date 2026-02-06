headerNames = ['Dex','Imagen','Especie','Tipos','Habilidades','Mov. Huevo','Coste',
               'BST','PS','Atq','Def','AtE','DfE','Vel']
altText = ['Movimientos','Solo Principal','Solo Oculta','Solo Pasiva','Buscar','Pot.','Prec.','PP',
           'Añadir a filtros','Recuerdo','Variocolor','Mov. Huevo','Mov. Huevo Raro',
           'Común','Súper','Ultra','MT','Nv.','Evo','Huevo']
catToName = ['Tipo','Habilidad','Movimiento','Gen','Coste','Nivel de Huevo','Modo',
             'Evolución','Forma','Bioma','Relacionado con','Variantes Variocolor','Etiqueta']
infoText = ['Amistad por Caramelo','Pasiva','Reducción de Coste','Huevo de Especie','Habilidad Oculta',
            'Exclusivo de Huevo','Exclusivo de Cría','Pokémon Paradoja','Cambio de Forma','Biomas','Filtros',
            'Reducido después de ## huevos','por Nivel','por Huevo','por MT']
biomeText = ['Común','Poco Común','Raro','Super Raro','Ultra Raro',
             'Jefe','Com.','PCom.','Raro','SR','UR','Amanecer','Día','Atardecer','Noche']
phrases = {
    'exclusive': 'Exclusivo',
    'new': 'Nuevo',
    'tag': 'Atributo',
    'theEnd': 'El Final',
    'fullyEvolved': 'Totalmente evolucionado',
    'formBase': 'Base',
    'formMega': 'Mega',
    'formNewMega': 'Nuevo Mega',
    'formGiga': 'Gigamax',
    'formTransformed': 'Transformado',
    'lureAbility': 'Habilidad de Colonia',
    'ignoresAbilities': 'Ignora Habilidades',
    'electricImmunity': 'Inmunidad Eléctrica',
    'fireImmunity': 'Inmunidad Fuego',
    'waterImmunity': 'Inmunidad Agua',
    'rainAbility': 'Habilidad de Lluvia',
    'sandAbility': 'Habilidad de Tormenta de Arena',
    'snowAbility': 'Habilidad de Nieve',
    'sunAbility': 'Habilidad de Sol',
    'targetSwitchesOut': 'Cambia al Objetivo',
    'spreadMoves': 'Movimientos de Área',
}
substitutions = [
    ['Teracristal Ogerpon','Tera Ogerpon'],
    ['Variedad ',''],
    ['Modo Daruma Darmanitan','Daruma Darmanitan']
]
helpMenuText = [
'Búsqueda rápida y potente</span> para PokeRogue',
'Usa la <span style="color:rgb(140, 130, 240);">Barra de Búsqueda</span> para añadir filtros:',
'Puedes combinar múltiples filtros',
'Haz clic entre filtros para usar la condición “o”',
'Haz clic en las <span style="color:rgb(140, 130, 240);">Cabeceras</span> para reordenar:',
'Columna <b>${headerNames[1]}</b> puede filtrar las variantes',
'Columna <b>${headerNames[4]}</b> puede limitarse a:',
'Habilidad Principal', '${infoText[4]}', '${infoText[1]}',
'<b>${headerNames[5]}</b> aparecen como <b>${fidToName[fidThreshold[4]]}</b> y <span style="color:rgb(240, 230, 140); font-weight: bold;">${fidToName[fidThreshold[4]+1]}</span>',
'Haz clic en el encabezado para cambiar a <b>${infoText[9]}</b>',
'Esa columna también mostrará <b>${altText[0]}/${infoText[9]} filtrado</b>',
'Columna <b>${catToName[4]}</b> muestra el color de <b>${catToName[5]}</b>:', 
'Haz clic en una entrada para ver los detalles de:',
'Haz clic en un <b>${headerNames[2]}</b> para ver su conjunto completo de movimientos.',
'El color de <b>${altText[5]}</b> indica daño <span style="color:${col.or}; font-weight: bold;">Físico</span> o <span style="color:${col.bl}; font-weight: bold;">Especial</span>',
'El color de <b>${altText[6]}</b> indica movimientos <span style="color:${col.re}; font-weight: bold;">Multiobjetivo</span>',
'Este sitio fue creado por Sandstorm, con mucho esfuerzo. No almaceno cookies ni recojo ningún dato personal. Las imágenes y los datos del juego provienen del GitHub de PokeRogue. Todos los derechos de los recursos pertenecen a sus creadores originales.',
'Versión del Juego', 'Fecha', 'Filtros Persistentes',
]
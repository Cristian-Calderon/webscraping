Tengo 3 csv que tengo que insertar a una base de datos necesito que me ayudes con la logica para poder relacionarlas entre si.



La primera se debe llamar : 
heroes y tendra esta estructura que sera la principal : 
name,link-Img,link-Page
Alchemist,https://www.dotabuff.com/assets/heroes/alchemist.jpg,https://www.dotabuff.com/heroes/alchemist
Axe,https://www.dotabuff.com/assets/heroes/axe.jpg,https://www.dotabuff.com/heroes/axe
Bristleback,https://www.dotabuff.com/assets/heroes/bristleback.jpg,https://www.dotabuff.com/heroes/bristleback
Centaur Warrunner,https://www.dotabuff.com/assets/heroes/centaur-warrunner.jpg,https://www.dotabuff.com/heroes/centaur-warrunner
Chaos Knight,https://www.dotabuff.com/assets/heroes/chaos-knight.jpg,https://www.dotabuff.com/heroes/chaos-knight
Dawnbreaker,https://www.dotabuff.com/assets/heroes/dawnbreaker.jpg,https://www.dotabuff.com/heroes/dawnbreaker
Doom,https://www.dotabuff.com/assets/heroes/doom.jpg,https://www.dotabuff.com/heroes/doom
Dragon Knight,https://www.dotabuff.com/assets/heroes/dragon-knight.jpg,https://www.dotabuff.com/heroes/dragon-knight
Earth Spirit,https://www.dotabuff.com/assets/heroes/earth-spirit.jpg,https://www.dotabuff.com/heroes/earth-spirit


luego perfil_heroes que tendra esta estructura :
Heroe,Popularidad,Porcentaje_de_Victoria,Resultado,Fuerza,Agilidad,Inteligencia,Velocidad_de_movimiento,Rango_de_vision,Armadura,Tiempo_de_Ataque_Base,Damage,Punto_de_ataque
Alchemist,61st,50.18%,won,23 +2.7,22 +1.5,25 +1.8,295,1800/800,3.08,1.7,50 - 56,0.35
Axe,17th,50.09%,won,25 +2.8,20 +1.7,18 +1.6,315,1800/800,2.8,1.7,56 - 60,0.4
Bristleback,51st,46.69%,lost,22 +2.7,17 +1.8,14 +2.8,295,1800/800,3.38,1.8,53 - 59,0.3
Centaur Warrunner,83rd,49.21%,lost,27 +4.0,15 +1.0,15 +1.6,305,1800/800,0.1,1.7,63 - 65,0.3
Chaos Knight,82nd,49.28%,lost,24 +3.1,18 +1.8,18 +1.2,325,1800/800,4.52,1.7,48 - 78,0.5
Dawnbreaker,61st,50.81%,won,25 +3.4,14 +1.7,20 +2.0,300,1800/800,3.96,1.7,54 - 58,0.46
Doom,84th,45.34%,lost,24 +3.8,15 +1.5,15 +1.7,290,1800/800,4.1,1.9,56 - 66,0.5
Dragon Knight,6th,52.78%,won,21 +3.6,16 +2.0,18 +1.7,315,1800/800,2.24,1.6,55 - 61,0.5
Earth Spirit,115th,46.59%,lost,22 +3.8,17 +2.4,18 +2.1,290,1800/800,2.38,1.7,47 - 57,0.35

y la otra tabla seria las habilidades:
id_habilidad,id_heroe,Héroe,Nombre de Habilidad,Descripción,Imagen
1,1,Alchemist,Acid Spray,"En inglés: Acid Spray.  Pulveriza ácido a gran presión sobre el área objetivo. Las unidades enemigas que caminen sobre el terreno contaminado reciben daño cada segundo y se reduce su armadura.",https://es.dotabuff.com/assets/skills/alchemist-acid-spray-5365-81d6b3d51a26dbd3d33d3841414067719e5631eb7a02236607cacd8776324967.jpg
2,1,Alchemist,Unstable Concoction,"En inglés: Unstable Concoction.  Alchemist prepara una mezcla inestable que puede lanzar a un héroe enemigo para aturdir e infligir daño en un área alrededor de la explosión. Cuanto más se prepare la mezcla, más daño causará y más tiempo aturdirá. Alchemist será más rápido mientras lleve la mezcla consigo. Tras 5 s, alcanza su máximo potencial de daño y tiempo de aturdimiento. Sin embargo, tras 5.5 s, la mezcla explotará sobre Alchemist si no la lanza.",https://es.dotabuff.com/assets/skills/alchemist-unstable-concoction-5366-81b1e5d67704538ae35269df43a631030d8085cde61862b166d1fb383147f468.jpg
3,1,Alchemist,Corrosive Weaponry,"En inglés: Corrosive Weaponry.  Alchemist recubre sus armas y potencia sus hechizos con un ácido que aplica una ralentización acumulable y una reducción del daño de ataque base a los enemigos alcanzados.  Los ataques aplican 2 acumulaciones. Mezcla Inestable aplica 1 acumulación por cada segundo de preparación.",https://es.dotabuff.com/assets/skills/alchemist-corrosive-weaponry-1116-3c81b60a8530283e3a4925553f20a4337bc75887af174d795f31d4c24e7c2d75.jpg
4,1,Alchemist,Berserk Potion,"En inglés: Berserk Potion.  Alchemist lanza una poción sobre un aliado, lo que le aplica una disipación básica y le otorga velocidad de ataque, velocidad de movimiento y regeneración de vida.  TIPO DE DISIPACIÓN: Básica.",https://es.dotabuff.com/assets/skills/alchemist-berserk-potion-642-b563a7a474c592bd43edb50ddb83a97af9559e65d3dc455dc748903d83d9ead5.jpg
5,1,Alchemist,Greevil's Greed,"En inglés: Greevil's Greed.  Alchemist sintetiza oro adicional de sus enemigos y de las Runas de Recompensa. Con cada víctima, Alchemist obtiene oro adicional base y una bonificación de oro adicional. Si Alchemist mata a otra unidad que dé oro en los siguientes 40 s, obtendrá una instancia de bonificación de oro adicional que se añade al total. Además hace que las Runas de Recompensa produzcan más oro de lo normal.",https://es.dotabuff.com/assets/skills/alchemist-greevils-greed-1333-5732fca37fe37b82177a8be9890337e3267e0afc99375e199c900815606cefac.jpg
6,1,Alchemist,Chemical Rage,"En inglés: Chemical Rage.  Alchemist hace que su Ogro entre en un estado de furia inducida por químicos que reduce su tiempo de ataque base y aumenta su velocidad de movimiento y regeneración de vida.  TIPO DE DISIPACIÓN: Básica.",https://es.dotabuff.com/assets/skills/alchemist-chemical-rage-5369-b743b415e5d40987b57ec8e8335e8f0cd55c93b8c260a87fe4832527ac636ec4.jpg
7,1,Alchemist,Unstable Concoction Throw,"En inglés: Unstable Concoction Throw.  ¡Lánzala antes de que explote!",https://es.dotabuff.com/assets/skills/alchemist-unstable-concoction-throw-5367-630446b105c4f58ff331d0ec7fa772b910b4a5bc9838653978cde1a11c75bb8a.jpg
8,2,Axe,Berserker's Call,"En inglés: Berserker's Call.  Axe provoca a las unidades enemigas cercanas, que se ven forzadas a atacarlo, y recibe armadura adicional mientras dure el efecto.",https://es.dotabuff.com/assets/skills/axe-berserkers-call-5007-f30d7f95a1a6ae8c45eb5b8f323b9a7148f6bcb3f7c74121d5746310f203b562.jpg
9,2,Axe,Battle Hunger,"En inglés: Battle Hunger.  Enfurece a una unidad enemiga, haciendo que reciba daño con el tiempo hasta que mate a otra unidad o termine el efecto. El daño aumenta en proporción a la armadura de Axe. El enemigo también es ralentizado siempre y cuando esté de espaldas a Axe.",https://es.dotabuff.com/assets/skills/axe-battle-hunger-5008-ecac4583b6dbd88ae530922fbfb8beceefb8997472e22bb62f58008c749c97ce.jpg
10,2,Axe,Counter Helix,"En inglés: Counter Helix.  Tras un número determinado de ataques, Axe realizará un contraataque espiral que infligirá daño puro a todos los enemigos cercanos.",https://es.dotabuff.com/assets/skills/axe-counter-helix-5009-b77d885afc3c807552246304350a9aa22732196915dedfde9e545f8cd0c29633.jpg
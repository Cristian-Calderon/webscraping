Tengo 2 csv que tengo que insertarlas en mi base de datos y que tienen que estar relacionadas como las puedo relacionar??:

la primera tabla seria objetos:
id_item,Nombre,Link
1,Aghanim's Shard,https://es.dotabuff.com/items/aghanims-shard
2,Aghanim's Scepter,https://es.dotabuff.com/items/aghanims-scepter
3,Magic Wand,https://es.dotabuff.com/items/magic-wand
4,Power Treads,https://es.dotabuff.com/items/power-treads
5,Blink Dagger,https://es.dotabuff.com/items/blink-dagger
6,Arcane Boots,https://es.dotabuff.com/items/arcane-boots
7,Black King Bar,https://es.dotabuff.com/items/black-king-bar
8,Phase Boots,https://es.dotabuff.com/items/phase-boots
9,Bracer,https://es.dotabuff.com/items/bracer
10,Glimmer Cape,https://es.dotabuff.com/items/glimmer-cape

la segunda tabla seria objetos-descripcion:
id_item,Nombre,Imagen,Costo,"""Descripción"""
1,Aghanim's Shard,https://es.dotabuff.com/assets/items/aghanims-shard-4e79e040a49fe45c7aa7aeb2b0776c06488564bc5cd33e742960153363910526.jpg,1400,"""Passive: Ability Upgrade Upgrades an existing ability or adds a new ability to your hero. Passive: Ability Upgrade"""
2,Aghanim's Scepter,https://es.dotabuff.com/assets/items/aghanims-scepter-d304fe07769b81d0c2624d78b12ed3a97194470b18d1999f8d5ed5654d8b1691.jpg,4200,"""Passive: Ability Upgrade Upgrades the ultimate, and some abilities, of all heroes. Passive: Ability Upgrade"""
3,Magic Wand,https://es.dotabuff.com/assets/items/magic-wand-8705c4305218afde38f755a6bdb2bb54da60a4b3ce6d8163950015c5f2bad52e.jpg,450,"""Active: Energy Charge Instantly restores 15 health and mana per charge stored.  Max 20 charges. Gains a charge whenever a visible enemy within 1200 range uses an ability. Active: Energy Charge 15 15"""
4,Power Treads,https://es.dotabuff.com/assets/items/power-treads-980cb4e9fc74127f29942cbfe149be2b414eec7e1614b860a4a6d312bc07f4a9.jpg,1400,"""Active: Switch Attribute Switches between +10 Strength, +10 Agility, or +10 Intelligence. Movement speed bonuses from multiple pairs of boots do not stack. Active: Switch Attribute"""
5,Blink Dagger,https://es.dotabuff.com/assets/items/blink-dagger-baaa3b7c2ac85481cfd574b8f305bcae4c8f4117e8f4050d100aa1da213a863d.jpg,2250,"""Active: Blink Teleport to a target point up to 1200 units away.  Blink Dagger cannot be used for 3 seconds after taking damage from an enemy hero or Roshan. Active: Blink 15 15"""
6,Arcane Boots,https://es.dotabuff.com/assets/items/arcane-boots-a3780516ff09b554f3aff61b4a97cf56eb0b901f12cec9e15956dfefd2e1e620.jpg,1400,"""Active: Replenish Restores 150 mana to all nearby allies.  Radius: 1200 Movement speed bonuses from multiple pairs of boots do not stack.  Passive: Basilius Aura Grants 1 mana regeneration to allies.  Radius: 1200 Active: Replenish 55 55"""
7,Black King Bar,https://es.dotabuff.com/assets/items/black-king-bar-8cd19b9e780334dfb49999208c4d5a4550c5e337ab2f55aa14e7c38cd2cd56f9.jpg,4050,"""Active: Avatar Applies a basic dispel. Grants 60% Magic resistance and immunity to pure and reflected damage. For the duration of the effect, any negative effect from enemy spells has no effect.  Duration: 9 / 8 / 7 / 6 Dispel Type: Basic Dispel Active: Avatar 95 50 95 50"""
8,Phase Boots,https://es.dotabuff.com/assets/items/phase-boots-1e1484aa86fdef3822ee6e7f6c36e4b0c857763757d8596ae0880c31e7ee7fe3.jpg,1500,"""Active: Phase Gives 20% increased movement speed on melee heroes, and 10% on ranged heroes, and lets you move through units and turn more quickly for 3 seconds. Movement speed bonuses from multiple pairs of boots do not stack. Active: Phase 8 8"""
9,Bracer,https://es.dotabuff.com/assets/items/bracer-6f90a395012ff706c86b8623eb58ee162eb4671f50f8f5b5b85528a4fc162004.jpg,505,
10,Glimmer Cape,https://es.dotabuff.com/assets/items/glimmer-cape-6f2d6a4a6d2b34573d2b9e1713c2333a76933a2b57ea2f95d55a407f12ed8b70.jpg,2150,"""Active: Glimmer After a 0.5 second delay, grants invisibility, 20 movement speed and a magic damage barrier that absorbs up to 300 damage to you or a target allied unit for 5 seconds.  Can be cast while channeling. Active: Glimmer 14 125 14 125"""
summon minecraft:leash_knot ~ ~ ~
execute as @e[type=minecraft:strider,distance=..8] if predicate {condition:"minecraft:entity_properties", entity: "this", predicate: {flags: {is_baby: false}}} run data modify entity @s leash.UUID set from entity @n[type=minecraft:leash_knot] UUID
kill @s
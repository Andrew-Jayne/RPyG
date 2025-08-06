✅ Move declarations from json into TOML

✅ use **init on dataclasses rather than blind dicts

✅ rework the encouter RPC system to be more extensible and understandable (content library made this free)

flesh-out the dungeon system

expand the encounter classes, and unify all encounters into a common system (enemies are not a facny special thing, and just go in the encounter pool)


well I didn't do any of that but now the content is loaded into cool classes and enums instead of a bunch of blind dicts

Need to find homes for all the content libraries, because I have latetent circular imports between encounter & content
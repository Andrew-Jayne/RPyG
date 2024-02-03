import json

with open('encounters/enemies_common.json', 'r') as enemies_file:
    enemies_lists = json.load(enemies_file)


target_object = enemies_lists['small_enemies'][0]['variant_lists']['lesser_variants'][0]



print(type(target_object))
print(target_object)
print(target_object.keys())
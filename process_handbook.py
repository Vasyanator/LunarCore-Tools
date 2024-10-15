import hashlib
import json
import os

# Compute the hash of a file
def compute_file_hash(filename):
    hasher = hashlib.sha256()
    with open(filename, 'rb') as f:
        while True:
            data = f.read(65536)  # Read in 64KB chunks
            if not data:
                break
            hasher.update(data)
    return hasher.hexdigest()

class Item:
    def __init__(self, item_id, title, item_type, section, rarity=None, main_stats=None):
        self.id = item_id
        self.title = title
        self.type = item_type  # 'default', 'planars', 'base_material', 'lightcone', 'material', 'unknown', 'other', etc.
        self.section = section  # The section name from the Handbook
        self.rarity = rarity  # integer 2 to 5 or None
        self.main_stats = main_stats or []  # list of main stats, if applicable

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'type': self.type,
            'section': self.section,
            'rarity': self.rarity,
            'main_stats': self.main_stats
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            item_id=data['id'],
            title=data['title'],
            item_type=data['type'],
            section=data['section'],
            rarity=data.get('rarity'),
            main_stats=data.get('main_stats', [])
        )

class HandbookData:
    def __init__(self):
        self.avatars_list = []
        self.relics_list = []
        self.props_list = []
        self.npc_monsters_list = []
        self.battle_stages = []
        self.battle_monsters_list = []
        self.mazes_list = []
        self.lightcones_list = []
        self.materials_list = []
        self.base_materials_list = []
        self.unknown_items_list = []
        self.other_items_list = []

def process_handbook(filename):
    items = []
    handbook_data = HandbookData()

    # Compute the hash of the input file
    file_hash = compute_file_hash(filename)

    # Define cache directory and files
    cache_dir = 'handbook_cache'
    cache_data_file = os.path.join(cache_dir, 'cache.json')
    cache_hash_file = os.path.join(cache_dir, 'hash.txt')

    # Check if cache exists and hashes match
    if os.path.exists(cache_data_file) and os.path.exists(cache_hash_file):
        with open(cache_hash_file, 'r') as f:
            cached_hash = f.read().strip()
        if cached_hash == file_hash:
            # Load cache
            with open(cache_data_file, 'r', encoding='utf-8') as f:
                cache = json.load(f)
            # Reconstruct handbook_data
            handbook_data.avatars_list = cache.get('avatars_list', [])
            handbook_data.relics_list = [Item.from_dict(item_dict) for item_dict in cache.get('relics_list', [])]
            handbook_data.props_list = cache.get('props_list', [])
            handbook_data.npc_monsters_list = cache.get('npc_monsters_list', [])
            handbook_data.battle_stages = cache.get('battle_stages', [])
            handbook_data.battle_monsters_list = cache.get('battle_monsters_list', [])
            handbook_data.mazes_list = cache.get('mazes_list', [])
            handbook_data.lightcones_list = [Item.from_dict(item_dict) for item_dict in cache.get('lightcones_list', [])]
            handbook_data.materials_list = [Item.from_dict(item_dict) for item_dict in cache.get('materials_list', [])]
            handbook_data.base_materials_list = [Item.from_dict(item_dict) for item_dict in cache.get('base_materials_list', [])]
            handbook_data.unknown_items_list = [Item.from_dict(item_dict) for item_dict in cache.get('unknown_items_list', [])]
            handbook_data.other_items_list = [Item.from_dict(item_dict) for item_dict in cache.get('other_items_list', [])]
            return handbook_data

    # Proceed to process the file as before
    # Read and process the file
    with open(filename, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    current_section = None

    # Sections to skip processing
    sections_to_skip = ['Lunar Core', 'Created', 'Commands']
    # Sections to process with basic processing
    basic_processing_sections = ['Items', 'Props (Spawnable)', 'NPC Monsters (Spawnable)', 'Battle Stages', 'Battle Monsters', 'Mazes', 'Avatars']

    i = 0
    while i < len(lines):
        line = lines[i].strip()

        # Check for section headers
        if line.startswith('# '):
            # This is a section header
            current_section = line[2:].strip()
            i += 1
            continue
        elif line == '':
            # Blank line
            i += 1
            continue
        else:
            # Skip processing for sections we are not interested in
            if current_section in sections_to_skip:
                i += 1
                continue

            # Process the line
            # Split the line into id and name
            if ':' in line:
                id_part, name_part = line.split(':', 1)
            else:
                i += 1
                continue  # Skip lines without ':'

            id_str = id_part.strip()
            name = name_part.strip()

            # Now, depending on current_section, we store data accordingly
            if current_section == 'Avatars':
                # Process avatars
                entry = {'id': id_str, 'name': name}
                handbook_data.avatars_list.append(entry)
            elif current_section == 'Items':
                # For 'Items' section, process as before
                # Skip IDs where the id is not a number
                if not id_str.isdigit():
                    i += 1
                    continue

                id_int = int(id_str)

                # Assign item_type based on given rules
                item_type = None  # We will determine item_type

                # First, check for 'unknown' items (name contains 'null')
                if 'null' in name.lower():
                    item_type = 'unknown'
                # characters in items. Skipping.
                elif 1001 <= id_int <= 8100:
                    pass
                # Materials: IDs in range 110000 - 119999
                elif 110000 <= id_int <= 119999:
                    item_type = 'material'
                # Base materials: IDs 1 - 1000
                elif 1 <= id_int <= 1000:
                    item_type = 'base_material'

                # Lightcones: IDs 20000 - 30000
                elif 20000 <= id_int <= 30000:
                    item_type = 'lightcone'
                    # Determine rarity based on the second digit
                    if len(id_str) < 2:
                        i += 1
                        continue  # Invalid ID format
                    second_digit = int(id_str[1])
                    if second_digit == 0:
                        rarity = 3
                    elif second_digit in [1, 2]:
                        rarity = 4
                    elif second_digit == 3:
                        rarity = 5
                    elif second_digit == 4:
                        rarity = 'free'
                    else:
                        rarity = None  # Unknown rarity
                    item = Item(item_id=id_str, title=name, item_type=item_type, section=current_section, rarity=rarity)
                    handbook_data.lightcones_list.append(item)
                    i += 1
                    continue
                # Relics (default and planars)
                elif len(id_str) == 5 and id_str[1] != '0':
                    first_digit = int(id_str[0])
                    if 3 <= first_digit <= 6:
                        # Determine the rarity based on the first digit minus 1
                        rarity = first_digit - 1  # Rarity from 2 to 5

                        # Determine the type based on the last digit
                        last_digit = int(id_str[-1])
                        if last_digit in [1, 2, 3, 4]:
                            item_type = 'default'
                        elif last_digit in [5, 6]:
                            item_type = 'planars'
                        else:
                            item_type = 'unknown'  # Could be other types in future

                        # Create the Item object
                        item = Item(item_id=id_str, title=name, item_type=item_type, section=current_section, rarity=rarity)
                        # Add to relics_list
                        handbook_data.relics_list.append(item)
                        i += 1
                        continue
                    else:
                        # IDs that don't meet the criteria fall into 'other'
                        item_type = 'other'
                else:
                    # IDs that don't meet any of the above criteria are 'other'
                    item_type = 'other'

                # Create the Item object
                item = Item(item_id=id_str, title=name, item_type=item_type, section=current_section)
                # Depending on item_type, store in appropriate list
                if item_type == 'material':
                    handbook_data.materials_list.append(item)
                elif item_type == 'base_material':
                    handbook_data.base_materials_list.append(item)
                elif item_type == 'unknown':
                    handbook_data.unknown_items_list.append(item)
                elif item_type == 'other':
                    handbook_data.other_items_list.append(item)
                else:
                    # For default and planars, we already handled them
                    pass
            elif current_section == 'Props (Spawnable)':
                # Process props
                entry = {'id': id_str, 'name': name}
                handbook_data.props_list.append(entry)
            elif current_section == 'NPC Monsters (Spawnable)':
                # Process npc monsters
                entry = {'id': id_str, 'name': name}
                handbook_data.npc_monsters_list.append(entry)
            elif current_section == 'Battle Stages':
                # Process battle stages
                entry = {'id': id_str, 'name': name}
                handbook_data.battle_stages.append(entry)
            elif current_section == 'Battle Monsters':
                # Process battle monsters
                entry = {'id': id_str, 'name': name}
                handbook_data.battle_monsters_list.append(entry)
            elif current_section == 'Mazes':
                # Process mazes
                entry = {'id': id_str, 'name': name}
                handbook_data.mazes_list.append(entry)
            else:
                # For sections not in our list, we can skip or store elsewhere
                pass

            i += 1

    # Prepare the cache data
    cache = {
        'avatars_list': handbook_data.avatars_list,
        'relics_list': [item.to_dict() for item in handbook_data.relics_list],
        'props_list': handbook_data.props_list,
        'npc_monsters_list': handbook_data.npc_monsters_list,
        'battle_stages': handbook_data.battle_stages,
        'battle_monsters_list': handbook_data.battle_monsters_list,
        'mazes_list': handbook_data.mazes_list,
        'lightcones_list': [item.to_dict() for item in handbook_data.lightcones_list],
        'materials_list': [item.to_dict() for item in handbook_data.materials_list],
        'base_materials_list': [item.to_dict() for item in handbook_data.base_materials_list],
        'unknown_items_list': [item.to_dict() for item in handbook_data.unknown_items_list],
        'other_items_list': [item.to_dict() for item in handbook_data.other_items_list],
    }

    # Ensure the cache directory exists
    if not os.path.exists(cache_dir):
        os.makedirs(cache_dir)

    # Save the cache data
    with open(cache_data_file, 'w', encoding='utf-8') as f:
        json.dump(cache, f, ensure_ascii=False, indent=4)

    # Save the file hash
    with open(cache_hash_file, 'w') as f:
        f.write(file_hash)

    # Return the HandbookData object
    return handbook_data

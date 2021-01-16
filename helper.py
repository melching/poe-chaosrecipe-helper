import random
import string


# create dict to map relevant bases to item class

ring_bases = [
    "Breach Ring", "Coral Ring", "Iron Ring", "Paua Ring", "Unset Ring", 
    "Sapphire Ring", "Topaz Ring", "Ruby Ring", "Diamond Ring", "Gold Ring", 
    "Moonstone Ring","Two-Stone Ring", "Amethyst Ring", "Prismatic Ring"
]
amulet_bases = [
    "Coral Amulet", "Paua Amulet", "Amber Amulet", "Jade Amulet", "Lapis Amulet", 
    "Gold Amulet", "Agate Amulet", "Citrine Amulet", "Turquoise Amulet", "Onyx Amulet", 
    "Marble Amulet", "Blue Pearl Amulet"
]
belt_bases = [
    "Chain Belt", "Rustic Sash", "Stygian Vise", "Heavy Belt", "Leather Belt", 
    "Cloth Belt", "Studded Belt", "Micro-Distillery Belt", "Vanguard Belt", "Crystal Belt"
]
body_bases = [
    'Arena Plate', "Assassin's Garb", 'Astral Plate', 'Battle Lamellar', 'Battle Plate', 
    'Blood Raiment', 'Bone Armour', 'Bronze Plate', 'Buckskin Tunic', 'Cabalist Regalia', 
    'Carnal Armour', 'Chain Hauberk', 'Chainmail Doublet', 'Chainmail Tunic', 'Chainmail Vest', 
    'Chestplate', 'Colosseum Plate', 'Commander\'s Brigandine', 'Conjurer\'s Vestment', 
    'Conquest Chainmail', 'Copper Plate', 'Coronal Leather', 'Crimson Raiment', 'Crusader Chainmail', 
    'Crusader Plate', 'Crypt Armour', 'Cutthroat\'s Garb', 'Desert Brigandine', 'Destiny Leather', 
    'Destroyer Regalia', 'Devout Chainmail', 'Dragonscale Doublet', 'Eelskin Tunic', 'Elegant Ringmail', 
    'Exquisite Leather', 'Field Lamellar', 'Frontier Leather', 'Full Chainmail', 'Full Dragonscale', 
    'Full Leather', 'Full Plate', 'Full Ringmail', 'Full Scale Armour', 'Full Wyrmscale', 
    'General\'s Brigandine', 'Gladiator Plate', 'Glorious Leather', 'Glorious Plate', 'Golden Plate', 
    'Holy Chainmail', 'Hussar Brigandine', 'Infantry Brigandine', 'Lacquered Garb', 'Latticed Ringmail', 
    'Light Brigandine', 'Lordly Plate', 'Loricated Ringmail', 'Mage\'s Vestment', 'Majestic Plate', 
    'Necromancer Silks', 'Occultist\'s Vestment', 'Oiled Coat', 'Oiled Vest', 'Ornate Ringmail', 
    'Padded Jacket', 'Padded Vest', 'Plate Vest', 'Quilted Jacket', 'Ringmail Coat', 'Sacrificial Garb', 
    'Sadist Garb', 'Sage\'s Robe', 'Saint\'s Hauberk', 'Saintly Chainmail', 'Savant\'s Robe', 'Scale Doublet', 
    'Scale Vest', 'Scarlet Raiment', 'Scholar\'s Robe', 'Sentinel Jacket', 'Shabby Jerkin', 'Sharkskin Tunic', 
    'Silk Robe', 'Silken Garb', 'Silken Vest', 'Silken Wrap', 'Simple Robe', 'Sleek Coat', 'Soldier\'s Brigandine', 
    'Spidersilk Robe', 'Strapped Leather', 'Sun Leather', 'Sun Plate', 'Thief\'s Garb', 'Triumphant Lamellar', 
    'Vaal Regalia', 'Varnished Coat', 'War Plate', 'Waxed Garb', 'Widowsilk Robe', 'Wild Leather', 
    'Wyrmscale Doublet', 'Zodiac Leather'
]
glove_bases = [
    'Ambush Mitts', 'Ancient Gauntlets', 'Antique Gauntlets', 'Arcanist Gloves', 
    'Assassin\'s Mitts', 'Bronze Gauntlets', 'Bronzescale Gauntlets', 'Carnal Mitts', 
    'Chain Gloves', 'Clasped Mitts', 'Conjurer Gloves', 'Crusader Gloves', 'Deerskin Gloves', 
    'Dragonscale Gauntlets', 'Eelskin Gloves', 'Embroidered Gloves', 'Fingerless Silk Gloves', 
    'Fishscale Gauntlets', 'Goathide Gloves', 'Goliath Gauntlets', 'Gripped Gloves', 
    'Hydrascale Gauntlets', 'Iron Gauntlets', 'Ironscale Gauntlets', 'Legion Gloves', 
    'Mesh Gloves', 'Murder Mitts', 'Nubuck Gloves', 'Plated Gauntlets', 'Rawhide Gloves', 
    'Ringmail Gloves', 'Riveted Gloves', 'Samite Gloves', 'Satin Gloves', 'Serpentscale Gauntlets', 
    'Shagreen Gloves', 'Sharkskin Gloves', 'Silk Gloves', 'Slink Gloves', 'Soldier Gloves', 
    'Sorcerer Gloves', 'Spiked Gloves', 'Stealth Gloves', 'Steel Gauntlets', 'Steelscale Gauntlets', 
    'Strapped Mitts', 'Titan Gauntlets', 'Trapper Mitts', 'Vaal Gauntlets', 'Velvet Gloves', 
    'Wool Gloves', 'Wrapped Mitts', 'Wyrmscale Gauntlets', 'Zealot Gloves'
]
boot_bases = [
    'Ambush Boots', 'Ancient Greaves', 'Antique Greaves', 'Arcanist Slippers', 
    'Assassin\'s Boots', 'Bronzescale Boots', 'Carnal Boots', 'Chain Boots', 'Clasped Boots', 
    'Conjurer Boots', 'Crusader Boots', 'Deerskin Boots', 'Dragonscale Boots', 'Eelskin Boots', 
    'Goathide Boots', 'Goliath Greaves', 'Hydrascale Boots', 'Iron Greaves', 'Ironscale Boots', 
    'Leatherscale Boots', 'Legion Boots', 'Mesh Boots', 'Murder Boots', 'Nubuck Boots', 
    'Plated Greaves', 'Rawhide Boots', 'Reinforced Greaves', 'Ringmail Boots', 'Riveted Boots', 
    'Samite Slippers', 'Satin Slippers', 'Scholar Boots', 'Serpentscale Boots', 'Shackled Boots', 
    'Shagreen Boots', 'Sharkskin Boots', 'Silk Slippers', 'Slink Boots', 'Soldier Boots', 
    'Sorcerer Boots', 'Stealth Boots', 'Steel Greaves', 'Steelscale Boots', 'Strapped Boots', 
    'Titan Greaves', 'Trapper Boots', 'Two-Toned Boots (Cold and Lightning Resistance)', 
    'Two-Toned Boots (Fire and Cold Resistance)', 'Two-Toned Boots (Fire and Lightning Resistance)', 
    'Two-Toned Boots','Vaal Greaves', 'Velvet Slippers', 'Wool Shoes', 'Wrapped Boots', 
    'Wyrmscale Boots', 'Zealot Boots'
]
helmet_bases = [
    'Aventail Helmet', 'Barbute Helmet', 'Battered Helm', 'Bone Circlet', 
    'Bone Helmet', 'Callous Mask', 'Close Helmet', 'Cone Helmet', 'Crusader Helmet', 
    'Deicide Mask', 'Eternal Burgonet', 'Ezomyte Burgonet', 'Fencer Helm', 'Festival Mask', 
    'Fluted Bascinet', 'Gilded Sallet', 'Gladiator Helmet', 'Golden Mask', 'Great Crown', 
    'Great Helmet', 'Harlequin Mask', 'Hubris Circlet', 'Hunter Hood', 'Iron Circlet', 
    'Iron Hat', 'Iron Mask', 'Lacquered Helmet', 'Leather Cap', 'Leather Hood', 'Lion Pelt', 
    'Lunaris Circlet', 'Magistrate Crown', 'Mind Cage', 'Necromancer Circlet', 'Nightmare Bascinet', 
    'Noble Tricorne', 'Pig-Faced Bascinet', 'Plague Mask', 'Praetor Crown', 'Prophet Crown', 
    'Raven Mask', 'Reaver Helmet', 'Regicide Mask', 'Royal Burgonet', 'Rusted Coif', 'Sallet', 
    'Samite Helmet', 'Scare Mask', 'Secutor Helm', 'Siege Helmet', 'Silken Hood', 'Sinner Tricorne', 
    'Solaris Circlet', 'Soldier Helmet', 'Steel Circlet', 'Torture Cage', 'Tribal Circlet', 
    'Tricorne', 'Ursine Pelt', 'Vaal Mask', 'Vine Circlet', 'Visored Sallet', 
    'Wolf Pelt', 'Zealot Helmet'
]

claw_bases = [
    'Awl', 'Blinder', 'Cat\'s Paw', 'Double Claw', 'Eagle Claw', 'Eye Gouger', 
    'Fright Claw', 'Gemini Claw', 'Gouger', 'Great White Claw', 'Gut Ripper', 
    'Hellion\'s Paw', 'Imperial Claw', 'Malign Fangs', 'Nailed Fist', 'Noble Claw', 
    'Prehistoric Claw', 'Shadow Fangs', 'Sharktooth Claw', 'Sparkling Claw', 
    'Terror Claw', 'Thresher Claw', 'Throat Stabber', 'Tiger\'s Paw', 'Timeworn Claw', 
    'Twin Claw', 'Vaal Claw', 'Void Fangs'
]
dagger_bases = [
    'Ambusher', 'Boot Blade', 'Boot Knife', 'Butcher Knife', 'Carving Knife', 
    'Copper Kris', 'Demon Dagger', 'Ezomyte Dagger', 'Fiend Dagger', 'Flashfire Blade', 
    'Flaying Knife', 'Flickerflame Blade', 'Glass Shank', 'Golden Kris', 'Gutting Knife', 
    'Hollowpoint Dagger', 'Imp Dagger', 'Imperial Skean', 'Infernal Blade', 'Platinum Kris', 
    'Pneumatic Dagger', 'Poignard', 'Pressurised Dagger', 'Prong Dagger', 'Royal Skean', 
    'Sai', 'Skean', 'Skinning Knife', 'Slaughter Knife', 'Stiletto', 'Trisula'
]
wand_bases = [
    'Accumulator Wand', 'Assembler Wand', 'Carved Wand', 'Congregator Wand', 'Convoking Wand', 
    'Crystal Wand', "Demon's Horn", 'Driftwood Wand', 'Engraved Wand', "Faun's Horn", 
    "Goat's Horn", 'Heathen Wand', 'Imbued Wand', 'Omen Wand', 'Opal Wand', 'Pagan Wand', 
    'Profane Wand', 'Prophecy Wand', 'Quartz Wand', 'Sage Wand', 'Serpent Wand', 
    'Spiraled Wand', 'Tornado Wand'
]
sword_bases = [
    "Corsair Sword", "Gemstone Sword", "Cutlass", "Variscite Blade", "Sabre", 
    "Copper Sword", "Rusted Sword"
]

itembases = {
    "rings": ring_bases,
    "amulets": amulet_bases,
    "belts": belt_bases,
    "body_armours": body_bases,
    "gloves": glove_bases,
    "boots": boot_bases,
    "helmets": helmet_bases,
    "weapons": claw_bases + dagger_bases + wand_bases + sword_bases
}


# define strings for filter, customizable for each object
head = "Show # ChaosRecipeMod\n"
tail = "\n\
    ItemLevel <= 74\n\
    ItemLevel >= 60\n\
    PlayAlertSound 16 300\n\
    Identified False\n\
    HasInfluence None\n\
    Rarity Rare\n\
    SetFontSize 50\n\
    SetBorderColor 0 0 0 255\n\
    SetBackgroundColor 200 0 0 255\n\
    MinimapIcon 2 Orange Kite\n\n"

str_ring =    head + "    Class Ring" + tail
str_amulet =  head + "    Class Amulet" + tail
str_belt =    head + "    Class Belt" + tail
str_glove =   head + "    Class Glove" + tail
str_boot =    head + "    Class Boot" + tail
str_body =    head + "    Class \"Body Armours\"" + tail
str_helmet =  head + "    Class Helmet" + tail
str_weapon1 = head + "    Class \"Claws\" \"Daggers\" \"Wands\"" + tail
str_weapon2 = head + "\
    Class Sword\n\
    Width < 2\n\
    Height < 4\
" + tail

filteradds = {
    "rings": str_ring,
    "amulets": str_amulet,
    "belts": str_belt,
    "body_armours": str_body,
    "gloves": str_glove,
    "boots": str_boot,
    "helmets": str_helmet,
    "weapons": str_weapon1+str_weapon2
}

def get_random_filtername(length):
    # Random string with the combination of lower and upper case
    letters = string.ascii_letters
    result_str = ''.join(random.choice(letters) for i in range(length))
    return "crh_" + result_str
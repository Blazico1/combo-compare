def id_to_vehicle(id):
    match id:
        case 0x00:
            return "Standard Kart S"
        case 0x01:
            return "Standard Kart M"
        case 0x02:
            return "Standard Kart L"
        case 0x03:
            return "Booster Seat"
        case 0x04:
            return "Classic Dragster"
        case 0x05:
            return "Offroader"
        case 0x06:
            return "Mini Beast"
        case 0x07:
            return "Wild Wing"
        case 0x08:
            return "Flame Flyer"
        case 0x09:
            return "Cheep Charger"
        case 0x0A:
            return "Super Blooper"
        case 0x0B:
            return "Piranha Prowler"
        case 0x0C:
            return "Tiny Titan"
        case 0x0D:
            return "Daytripper"
        case 0x0E:
            return "Jetsetter"
        case 0x0F:
            return "Blue Falcon"
        case 0x10:
            return "Sprinter"
        case 0x11:
            return "Honeycoupe"
        case 0x12:
            return "Standard Bike S"
        case 0x13:
            return "Standard Bike M"
        case 0x14:
            return "Standard Bike L"
        case 0x15:
            return "Bullet Bike"
        case 0x16:
            return "Mach Bike"
        case 0x17:
            return "Flame Runner"
        case 0x18:
            return "Bit Bike"
        case 0x19:
            return "Sugarscoot"
        case 0x1A:
            return "Wario Bike"
        case 0x1B:
            return "Quacker"
        case 0x1C:
            return "Zip Zip"
        case 0x1D:
            return "Shooting Star"
        case 0x1E:
            return "Magikruiser"
        case 0x1F:
            return "Sneakster"
        case 0x20:
            return "Spear"
        case 0x21:
            return "Jet Bubble"
        case 0x22:
            return "Dolphin Dasher"
        case 0x23:
            return "Phantom"
        case _:
            return f"Unknown vehicle {id:X}"
        
def id_to_driver(id):
    match id:
        case 0x00:
            return "Mario"
        case 0x01:
            return "Baby Peach"
        case 0x02:
            return "Waluigi"
        case 0x03:
            return "Bowser"
        case 0x04:
            return "Baby Daisy"
        case 0x05:
            return "Dry Bones"
        case 0x06:
            return "Baby Mario"
        case 0x07:
            return "Luigi"
        case 0x08:
            return "Toad"
        case 0x09:
            return "Donkey Kong"
        case 0x0A:
            return "Yoshi"
        case 0x0B:
            return "Wario"
        case 0x0C:
            return "Baby Luigi"
        case 0x0D:
            return "Toadette"
        case 0x0E:
            return "Koopa Troopa"
        case 0x0F:
            return "Daisy"
        case 0x10:
            return "Peach"
        case 0x11:
            return "Birdo"
        case 0x12:
            return "Diddy Kong"
        case 0x13:
            return "King Boo"
        case 0x14:
            return "Bowser Jr."
        case 0x15:
            return "Dry Bowser"
        case 0x16:
            return "Funky Kong"
        case 0x17:
            return "Rosalina"
        case 0x18:
            return "Mii S"
        case 0x19:
            return "Mii M"
        case 0x1A:
            return "Mii L"
        case _:
            return f"Unknown driver {id:X}"
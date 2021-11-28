class Config(object):
    attributes = ["strength", "dexterity", "constitution", "intelligence", "wisdom", "charisma" ]
    classes=[ "Expert", "Psychic", "Warrior" ]
    backgrounds=[ "Barbarian", "Clergy", "Courtesan", "Criminal", "Dilettante", "Entertainer",
            "Merchant", "Noble", "Official", "Peasant", "Physician", "Pilot", "Politician",
            "Scholar", "Soldier", "Spacer", "Technician", "Thug", "Vagabond", "Worker" ]
    skills = [ "administer", "connect", "exert", "fix", "heal", "know", "lead", "notice", "perform", "pilot", "program", "punch", 
            "shoot", "sneak", "stab", "survive",  "talk",  "trade", "work", "biopsionics", "metapsionics", "precognition", 
            "telekinesis", "telepathy", "teleportation" ]

from flask import Blueprint
from app.rpg.views import register_urls
from app.rpg.swn.models import StarsSheet, StarsWeapon
from app.rpg.swn.forms import StarsForm

bp = Blueprint('swn', __name__)

# We need to inject the BP name to be picked up in all templates
@bp.context_processor
def inject_user():
    return dict(bp_name='Stars Without Numbers', bp_route='swn')

register_urls(bp, StarsSheet, StarsForm, StarsWeapon, Config)
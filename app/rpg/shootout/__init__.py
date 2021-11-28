class Config(object):
    attributes = ["strength", "dexterity", "constitution", "intelligence", "wisdom", "charisma" ]
    classes=[ "Warrior", "Expert", "Arcanist", "Magister", "Pact Maker", "Shaman", "War Mage", "Adepts", "Witch Hunter", "Martial Adept", "Mystic"]
    backgrounds=[ "Arcane Scholar", "Cleric", "Courtesan", "Cowhand", "Criminal", "Dilettante", "Engineer",
            "Entertainer", "Gentry", "Government Mage", "Hedge Wizard", "Hirespell", "Hunter", "Inquisitor", "Labourer",
            "Merchant", "Official", "Physician", "Politician", "Rogue Mage", "Scholar", "Soldier", "Thug", "Vagabond", "Worker"]
    skills = [ "administer", "cast_magic", "connect", "exert", "fix", "heal", "horsemanship", 
            "know", "know_magic", "lead", "notice", "perform", "punch", "sail", "shoot", "sneak", "stab",
            "survive",  "talk",  "trade", "work" ]

from flask import Blueprint
from app.rpg.views import register_urls
from app.rpg.shootout.models import ShootoutSheet, ShootoutWeapon
from app.rpg.shootout.forms import ShootoutForm

bp = Blueprint('shootout', __name__)

# We need to inject the BP name to be picked up in all templates
@bp.context_processor
def inject_user():
    return dict(bp_name='Shootout', bp_route='shootout')

register_urls(bp, ShootoutSheet, ShootoutForm, ShootoutWeapon, Config)
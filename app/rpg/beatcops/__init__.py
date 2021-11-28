class Config(object):
    attributes = ["strength", "dexterity", "constitution", "intelligence", "wisdom", "charisma" ]
    classes=["Brain", "Brawn"]
    backgrounds=["Traffic Branch", "Armed Response Unit", "Dog Section", "Detective", "Tactical Support Group", 
                "Cyber Crime", "Response", "Neighbourhood", "PACE Officer", "Covert Policing Unit", "Counter Terror Firearms Officer" ]
    skills = [ "administer", "animal_handling", "connect", "drive", "exert", "fix", "heal", "investigate", 
            "know", "lead", "notice", "perform", "program", "punch", "program", "requisition", "search",
            "shoot",  "stealth",  "strike", "survive", "talk", "work" ]

from flask import Blueprint
from app.rpg.views import register_urls
from app.rpg.beatcops.models import BeatCopsSheet, BeatCopsWeapon
from app.rpg.beatcops.forms import BeatCopsForm

bp = Blueprint('beatcops', __name__)

# We need to inject the BP name to be picked up in all templates
# Reference -> https://stackoverflow.com/questions/26498689/flask-jinja-pass-data-to-a-base-template-all-templates
@bp.context_processor
def inject_user():
    return dict(bp_name='BeatCops', bp_route='beatcops')

register_urls(bp, BeatCopsSheet, BeatCopsForm, BeatCopsWeapon, Config)
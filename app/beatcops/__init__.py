class Config(object):
    attributes = ["strength", "dexterity", "constitution", "intelligence", "wisdom", "charisma" ]
    classes=["Brain", "Brawn"]
    backgrounds=["Traffic Branch", "Armed Response Unit", "Dog Section", "Detective", "Tactical Support Group", 
                "Cyber Crime", "Response", "Neighbourhood", "PACE Officer", "Covert Policing Unit", "Counter Terror Firearms Officer" ]
    skills = [ "administer", "animal_handling", "connect", "drive", "exert", "fix", "heal", "investigate", 
            "know", "lead", "notice", "perform", "program", "punch", "program", "requisition", "search",
            "shoot",  "stealth",  "strike", "survive", "talk", "work" ]

from flask import Blueprint
from app.common.views import register_urls
from app.beatcops.models import BeatCopsSheet, BeatCopsWeapon
from app.beatcops.forms import SheetForm

bp = Blueprint('beatcops', __name__)

# We need to inject the BP name to be picked up in all templates
@bp.context_processor
def inject_user():
    return dict(bp_name='BeatCops', bp_route='beatcops')

register_urls(bp, BeatCopsSheet, SheetForm, BeatCopsWeapon, Config)
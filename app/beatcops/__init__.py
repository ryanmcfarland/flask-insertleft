from flask import Blueprint

class Config(object):
    attributes = ["strength", "dexterity", "constitution", "intelligence", "wisdom", "charisma" ]
    classes=["Brain", "Brawn"]
    backgrounds=["Traffic Branch", "Armed Response Unit", 
                "Dog Section", "Detective", "Tactical Support Group", "Cyber Crime", 
                "Response", "Neighbourhood", "PACE Officer", "Counter Terror Firearms Officer" ]
    skills = [ "administer", "animal_handling", "connect", "drive", "fix", "heal", "investigate", 
            "know", "lead", "notice", "perform", "program", "punch", "program", "requisition", "search",
            "shoot",  "stealth",  "strike", "survive", "talk", "work" ]

bp = Blueprint('beatcops', __name__)

from app.beatcops.routes import Edit

edit = Edit.as_view('edit', "test")
bp.add_url_rule('/edit/<int:id>', view_func=edit)

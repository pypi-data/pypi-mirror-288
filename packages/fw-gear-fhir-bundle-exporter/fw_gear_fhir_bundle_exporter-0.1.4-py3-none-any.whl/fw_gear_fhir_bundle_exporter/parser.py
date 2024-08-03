"""Parser module to parse gear config.json."""

from flywheel_gear_toolkit import GearToolkitContext


# This function mainly parses gear_context's config.json file and returns relevant
# inputs and options.
def parse_config(
    gear_context: GearToolkitContext,
) -> bool:
    """Parse the config.json file.

    TODO: This may evolve with additional requirements.

    Returns:
        tuple: debug, include_encounter, include_bodystructure
    """

    debug = gear_context.config.get("debug")
    include_encounter = gear_context.config.get("include_encounter_resource")
    include_bodystructure = gear_context.config.get("include_body_structure_resource")

    return debug, include_encounter, include_bodystructure

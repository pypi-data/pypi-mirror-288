"""Main module."""

import logging

from .fhir_resource_bundle import get_patient_bundle, write_patient_bundle

log = logging.getLogger(__name__)


def run(context, debug, include_encounter, include_bodystructure):
    """Run the algorithm defined in this gear.

    Args:
        context (GearContext): The Context object
        debug (bool): The debug flag
        include_encounter (bool): The include_encounter flag
        include_bodystructure (bool): The include_bodystructure flag

    Raises:
        ValueError: Raised if the parent container type is not supported

    Returns:
        int: The Exit Code
    """
    try:
        # This gear is designed to be run on a project or subject container
        destination_container = context.client.get(context.destination["id"])
        # get parent type
        dest_parent_type = destination_container.parent["type"]
        dest_parent_id = destination_container.parent["id"]
        dest_parent = context.client.get(dest_parent_id)

        if dest_parent_type == "project":
            for subject in dest_parent.subjects():
                bundle = get_patient_bundle(
                    context.client, subject, include_encounter, include_bodystructure
                )
                write_patient_bundle(context, subject, bundle)
        elif dest_parent_type == "subject":
            bundle = get_patient_bundle(
                context.client, dest_parent, include_encounter, include_bodystructure
            )
            write_patient_bundle(context, dest_parent, bundle)
        # TODO: add support for session containers
        #       This would be done by passing the session object along with the subject
        #       e.g. get_patient_bundle(context.client, dest_parent.subject, dest_parent)
        else:
            log.debug(
                "Parent container type %s is not supported. Exiting.", dest_parent_type
            )
            raise ValueError(
                f"Parent container type {dest_parent_type} is not supported. Exiting."
            )
    except (ValueError, Exception) as exc:
        log.exception(exc)
        return 1

    return 0

import re
from dapla_suv_tools._internals.util.suv_operation_context import SuvOperationContext


ra_pattern = re.compile("^[rR][aA]-[0-9]{4}$")

guid_pattern = re.compile(
    r"^[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$"
)


def instance_str_validator(ctx: SuvOperationContext, **kwargs):
    instance_id = kwargs.get("instance_id", None)

    instance_owner_id = int(instance_id.split("/")[0])
    instance_guid = instance_id.split("/")[1]

    if not isinstance(instance_id, str):
        raise _set_error(
            ctx,
            "Parameter 'instance_id' must be a valid string. Eg. '123451213/12345678-1234-1234-1234-123456789012'",
        )

    if not re.match(guid_pattern, instance_guid):
        raise _set_error(
            ctx,
            "Guid for instance must match pattern 'xxxxxxxx-xxxx-vxxx-xxxx-xxxxxxxxxxxx' (x = digit 0-9, a-f)",
        )

    if not isinstance(instance_owner_id, int) or instance_owner_id == -1:
        raise _set_error(ctx, "Owner for instance must be a valid positive integer.")


def skjema_id_validator(ctx: SuvOperationContext, **kwargs):
    skjema_id = kwargs.get("skjema_id", -1)

    if not isinstance(skjema_id, int) or skjema_id == -1:
        raise _set_error(ctx, "Parameter 'skjema_id' must be a valid positive integer.")


def ra_nummer_validator(ctx: SuvOperationContext, **kwargs):
    ra_nummer = kwargs.get("ra_nummer", None)

    if not isinstance(ra_nummer, str):
        raise _set_error(ctx, "Parameter 'ra_nummer' must be a valid positive integer.")

    if not re.match(ra_pattern, ra_nummer):
        raise _set_error(
            ctx,
            "Parameter 'ra_nummer' must match pattern 'ra-XXXX' or 'RA-XXXX' (X = digit 0-9)",
        )


def periode_id_validator(ctx: SuvOperationContext, **kwargs):
    periode_id = kwargs.get("periode_id", -1)

    if not isinstance(periode_id, int) or periode_id == -1:
        raise _set_error(
            ctx, "Parameter 'periode_id' must be a valid positive integer."
        )


def _set_error(ctx: SuvOperationContext, message: str) -> Exception:
    ex = ValueError(message)
    ctx.set_error(error_msg=message, exception=ex)

    return ex

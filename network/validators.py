from rest_framework.exceptions import ValidationError


def check_supplier_chain(network_point):
    """
    Проверка цепочки поставщиков, чтобы она не превышала 3 уровней.
    """
    current = network_point.supplier
    level_network = 1

    while current is not None:
        level_network += 1
        if level_network > 3:
            raise ValidationError(
                "Цепочка поставщиков не может быть более трех уровней."
            )

        if (network_point.level == "retail" and current.level == "entrepreneur") or (
            network_point.level == "entrepreneur" and current.level == "retail"
        ):
            return True

        if (
            network_point.level == "retail"
            and current.level == "factory"
            and current.supplier
            and current.supplier.level == "entrepreneur"
        ) or (
            network_point.level == "entrepreneur"
            and current.level == "factory"
            and current.supplier
            and current.supplier.level == "retail"
        ):
            return True

        current = current.supplier

    return True

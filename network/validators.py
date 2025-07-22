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
            )  # Использование

        # Логика для проверки допустимых связей
        if (network_point.level == "retail" and current.level == "entrepreneur") or (
            network_point.level == "entrepreneur" and current.level == "retail"
        ):
            return True  # Допустимая связь между "Розничной сетью" и "ИП"

        # Логика для тройной вложенности (Завод → Розничная сеть → ИП и Завод → ИП → Розничная сеть)
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
            return True  # Допустимая вложенность "Завод → Розничная сеть → ИП"

        # Если ничего из этого не подошло, продолжаем искать на следующем уровне
        current = current.supplier

    return True  # Если цепочка не превышает 3 уровня и связи допустимы

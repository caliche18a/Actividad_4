from __future__ import annotations


AGE_GROUPS = [
    ("Mortalidad neonatal", range(0, 5), "Menor de 1 mes"),
    ("Mortalidad infantil", range(5, 7), "1 a 11 meses"),
    ("Primera infancia", range(7, 9), "1 a 4 años"),
    ("Niñez", range(9, 11), "5 a 14 años"),
    ("Adolescencia", range(11, 12), "15 a 19 años"),
    ("Juventud", range(12, 14), "20 a 29 años"),
    ("Adultez temprana", range(14, 17), "30 a 44 años"),
    ("Adultez intermedia", range(17, 20), "45 a 59 años"),
    ("Vejez", range(20, 25), "60 a 84 años"),
    ("Longevidad / Centenarios", range(25, 29), "85 a 100+ años"),
    ("Edad desconocida", range(29, 30), "Sin informacion"),
]

AGE_GROUP_ORDER = [group[0] for group in AGE_GROUPS]
AGE_GROUP_LABELS = {group[0]: group[2] for group in AGE_GROUPS}


def assign_age_group(code: int) -> str:
    for label, codes, _ in AGE_GROUPS:
        if int(code) in codes:
            return label
    return "Edad desconocida"

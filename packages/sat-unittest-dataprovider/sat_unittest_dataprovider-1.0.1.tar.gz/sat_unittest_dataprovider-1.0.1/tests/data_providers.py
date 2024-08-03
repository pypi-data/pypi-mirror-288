from typing import List, Tuple, Dict


def tuples_in_list() -> List[Tuple[int, int, int, str]]:
    return [
        (1, 2, 3, '1 + 2 is 3'),
        (2, 2, 4, '2 + 2 is 3')
    ]


def tuples_in_tuple() -> Tuple[Tuple[int, int, int, str], ...]:
    return (
        (1, 2, 3, '1 + 2 is 3'),
        (2, 2, 4, '2 + 2 is 3'),
    )


def dict_with_tuples() -> Dict[str, Tuple[int, int, int, str]]:
    return {
        "record_1": (1, 2, 3, '1 + 2 is 3'),
        "record_2": (2, 2, 4, '2 + 2 is 3'),
    }


a_dict: Dict[str, Tuple[int, int, int, str]] = {
    "record_1": (1, 2, 3, '1 + 2 is 3'),
    "record_2": (2, 2, 4, '2 + 2 is 3'),
}

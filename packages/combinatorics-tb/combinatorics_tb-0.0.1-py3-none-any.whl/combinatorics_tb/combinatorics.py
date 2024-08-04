from factorial_tb import factorial

def combinations(out_of: int, choose: int) -> int:
    if type(out_of) == int and type(choose) == int:
        if 0 <= choose <= out_of:
            return int(factorial.factorial(out_of) / (factorial.factorial(choose) * factorial.factorial(out_of - choose)))
        else:
            raise ValueError()

    else:
        raise TypeError()


def permutations(out_of: int, choose_where_order_matters: int) -> int:
    if type(out_of) == int and type(choose_where_order_matters) == int:
        if 0 <= choose_where_order_matters <= out_of:
            return int(factorial.factorial(out_of) / (factorial.factorial(out_of - choose_where_order_matters)))
        else:
            raise ValueError()

    else:
        raise TypeError()

if __name__ == "__main__":
    print(combinations(10, 4))
    print(permutations(10, 4))

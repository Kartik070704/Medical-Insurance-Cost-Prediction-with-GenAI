def format_indian_number(value: float) -> str:
    amount = f"{value:.2f}"
    whole, decimal = amount.split(".")
    sign = ""
    if whole.startswith("-"):
        sign = "-"
        whole = whole[1:]

    if len(whole) <= 3:
        grouped = whole
    else:
        grouped = whole[-3:]
        whole = whole[:-3]
        while whole:
            grouped = f"{whole[-2:]},{grouped}"
            whole = whole[:-2]

    return f"{sign}{grouped}.{decimal}"


def format_inr(value: float, symbol: str = "₹") -> str:
    return f"{symbol}{format_indian_number(value)}"

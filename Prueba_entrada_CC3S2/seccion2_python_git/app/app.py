# Implementa la función summarize y el CLI.
# Requisitos:
# - summarize(nums) -> dict con claves: count, sum, avg
# - Valida que nums sea lista no vacía y elementos numéricos (acepta strings convertibles a float).
# - CLI: python -m app "1,2,3" imprime: sum=6.0 avg=2.0 count=3

def summarize(nums: list) -> dict:
    if not isinstance(nums, list):
        raise ValueError("El input debe ser una lista de números o strings numéricos.")

    if len(nums) == 0:
        raise ValueError("El input no puede ser una lista vacía.")

    numbers: list[float] = []
    for num in nums:
        try:
            numbers.append(float(num))
        except:
            raise ValueError("Número invalidado, se salta: " + num)

    numbersCount = len(numbers)
    numbersTotal = sum(numbers)
    numbersAverage = numbersTotal / numbersCount
    return {"count": numbersCount, "sum": numbersTotal, "avg": numbersAverage}

if __name__ == "__main__":
    import sys
    raw = sys.argv[1] if len(sys.argv) > 1 else ""
    items = [p.strip() for p in raw.split(",") if p.strip()]
    
    result = summarize(items)
    print(f"Conteo: {result['count']}\nSuma: {result['sum']}\nPromedio: {result['avg']:.2f}")

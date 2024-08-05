import sqlglot
from sqlglot.optimizer import optimize


parsed = sqlglot.parse_one(
    """
            SELECT A OR (B OR (C AND D))
            FROM x
            WHERE Z = date '2021-01-01' + INTERVAL '1' month OR 1 = 0
        """
)

#schema = {"x": {"A": "INT", "B": "INT", "C": "INT", "D": "INT", "Z": "STRING"}}

f = optimize(
    parsed,
    #schema=schema,
)

breakpoint()
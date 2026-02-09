class Field:
    """
    Defines metadata for a single contract field.
    """

    def __init__(
        self,
        type_,
        *,
        optional: bool = False,
        nullable: bool = False,
        default=None,
        description: str | None = None,
        **constraints,
    ):
        self.type = type_
        self.optional = optional
        self.nullable = nullable
        self.default = default
        self.description = description
        self.constraints = constraints

    def __repr__(self) -> str:
        return (
            f"Field(type={self.type}, optional={self.optional}, "
            f"nullable={self.nullable}, constraints={self.constraints})"
        )

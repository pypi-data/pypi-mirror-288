class InvalidResource(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class ResourceNameNotFound(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

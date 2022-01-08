class HTMLError(Exception):
    """Exception raised for errors in the config HTML.

    Attributes:
        config --  which caused the error
    """

    def __init__(self, name, html):
        self.html_config = html
        self.name = name
        super().__init__()

    def __str__(self):
        return (f'The HTML config "{self.html_config}" have changed. '
                f'Change the config in `.config.{self.name}` attribute')
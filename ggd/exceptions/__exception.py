class HTMLError(Exception):
    """Exception raised for errors in the config HTML.

    Attributes:
        html -- which html balise caused the error
        name -- name of html balise
    """

    def __init__(self, name, html):
        self.html = html
        self.name = name
        super().__init__()

    def __str__(self):
        return (f'The HTML config "{self.html}" have changed. '
                f'Change the config in `.config.{self.name}` attribute')
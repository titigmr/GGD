class Config:
    VALID_EXTENSION = (".png", ".jpg", ".jpeg")
    BLOC_IMAGE = 'isv-r'
    BLOC_END = 'mye4qd'
    BLOC_POP = 'n3VNCb'
    BLOC_AFTER = '//*[@id="Sva75c"]/div/div/div[3]/div[2]/c-wiz/div/div[1]/div[1]/div[1]/a[3]'

    def __repr__(self):
        config = {'VALID_EXTENSION': self.VALID_EXTENSION,
                  'BLOC_IMAGE': self.BLOC_IMAGE,
                  'BLOC_POP': self.BLOC_POP,
                  'BLOC_END': self.BLOC_END,
                  'BLOC_AFTER': self.BLOC_AFTER}
        return str(config)
from dataclasses import dataclass

from model.artObject import ArtObject


@dataclass
class Arco:
    o1: ArtObject
    o2: ArtObject
    peso: int

    #non faccio cose di hash ecc perchè non ANDRò MAI a confrontare
    #mi servono solo per inserire i risultati della query del dao
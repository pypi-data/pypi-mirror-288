from dataclasses import dataclass

@dataclass
class Probability:
    value: float

    def __post_init__(self):
        if type(self.value) == float:
            if 0 <= self.value <= 1:
                pass

            else:
                raise ValueError()

        else:
            raise TypeError()


if __name__ == "__main__":
    p = Probability(.5)

    print(p.value)


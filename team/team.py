import jsonpickle


class ModelInfo:
    def __init__(self, name: str, link: str) -> None:
        self.name = name
        self.link = link


class TeamObject:
    def __init__(self, id: str, name: str, link: str) -> None:
        self.id = id
        self.name = name
        self.link = link


class Modeler(TeamObject):
    def __init__(self, id: str, name: str, link: str, models: list[ModelInfo]) -> None:
        super().__init__(id, name, link)
        self.models = models


class Creator(TeamObject):
    def __init__(self, id: str, name: str, link: str, image: str, bio: str) -> None:
        super().__init__(id, name, link)
        self.image = image
        self.bio = bio


class AssociateProfessor(TeamObject):
    def __init__(
        self, id: str, name: str, link: str, image: str, bio: str, tags: list[str]
    ) -> None:
        super().__init__(id, name, link)
        self.image = image
        self.bio = bio
        self.tags = tags


creators: list[Creator] = [
    Creator(
        id="665df2fdf0b761c8e9acc6f4",
        name="Hannah Rubin",
        bio="Professor Rubin is an evolutionary game theorist, philosopher of biology, and philosopher of science. She is an associate professor at the University of Missouri (Mizzou), and the professor who enabled the creation of ModelPy.",
        image="https://images.squarespace-cdn.com/content/v1/5616b03fe4b01bca36ae90fc/1509892492330-3KEYDHJ92ZYAM9KPA0YA/DSCN0107.JPG?format=750w",
        link="https://www.hannahrubin.net/teaching",
    ),
    Creator(
        id="665df2fdf0b761c8e9acc6f5",
        name="Kekoa Wong",
        bio="Kekoa has worked on research funded by the National Science Foundation, USAID, and the ND-IBM Tech Ethics Lab. He combines his academic backgrounds in philosophy and computer engineering to build tech that benefits society.",
        image="https://media.licdn.com/dms/image/D4D03AQGHya8O36f-Cg/profile-displayphoto-shrink_800_800/0/1715620397177?e=1723075200&v=beta&t=Ktby-t0iGlArCWzPjP1DApSS0DcTQ-VEv6M7hbAFMu4",
        link="https://www.kekoawong.com/",
    ),
    Creator(
        id="665df2fdf0b761c8e9acc6f5",
        name="Oluwatoni Akintola",
        bio="Oluwatoni (Toni) Akintola is a Class of 2026 Computer Science and Economics student at the University of Notre Dame. He is interested in game theory and how ABMs can be used to model and observe emergent behaviors occurrent in financial markets.",
        image="https://media.licdn.com/dms/image/D4D03AQFR_ukH2Pk7Fw/profile-displayphoto-shrink_100_100/0/1715601943362?e=1723075200&v=beta&t=BrDDzEpKNhc6Fdi-1KZxiVIzfFp07ObYM9hYTLOR3VU",
        link="https://www.kekoawong.com/",
    ),
]
associate_professors: list[AssociateProfessor] = [
    AssociateProfessor(
        id="665df2fdf0b761c8e9acc6f6",
        name="Kevin Zollman",
        bio="Professor Zollman is the Herbert A. Simon Professor of Philosophy and Social and Decision Sciences at Carnegie Mellon University. He is also the inaugural director of the Institute for Complex Social Dynamics, and the professor behind the Zollman Bandit model. ",
        image="https://www.kevinzollman.com/uploads/5/0/3/6/50361245/2331440.jpg",
        link="https://www.kevinzollman.com/",
        tags=["bayesian-agents", "bandit-model"],
    ),
    AssociateProfessor(
        id="665df2fdf0b761c8e9acc6f7",
        name="Jingyi Wu",
        bio="Professor Wu is Assistant Professor in the Department of Philosophy, Logic and Scientific Method at the London School of Economics. She works in social epistemology and philosophy of physics, and is the professor behind the Wu epistomological bandit model. ",
        image="https://www.jingyiwu.org/uploads/1/3/8/0/138010336/img-6947_orig.jpg",
        link="https://www.jingyiwu.org/",
        tags=["bayesian-agents", "bandit-model"],
    ),
]

modelers: list[Modeler] = [
    Modeler(
        id="665df2fdf0b761c8e9acc6f8",
        name="Kekoa Wong",
        link="https://www.kekoawong.com/",
        models=[
            ModelInfo(name="zollman-bandit",
                      link="/models/kekoawong/zollman-bandit"),
            ModelInfo(
                name="wu-epistemic-advantage",
                link="/models/kekoawong/wu-epistemic-advantage",
            ),
        ],
    ),
    Modeler(
        id="6663232c757be4ca9b70f242",
        name="Oluwatoni Akintola",
        link="https://github.com/toni-akintola",
        models=[
            ModelInfo(
                name="boltzmann-wealth-model",
                link="/models/toni-akintola/boltzmann-wealth-model",
            ),
        ],
    ),
]


def postTeamInfo():
    """Returns all creators, professors, and modelers on the server."""
    data = {
        "creators": creators,
        "professors": associate_professors,
        "modelers": modelers,
    }
    return jsonpickle.encode(data)

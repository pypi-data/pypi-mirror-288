import datetime
import json
import os
import random
import shutil
import string

import wonderwords

FAMOUS_SCIENTISTS = [
    # Female Scientists
    "Marie Curie",
    "Rosalind Franklin",
    "Ada Lovelace",
    "Jane Goodall",
    "Rachel Carson",
    "Dorothy Hodgkin",
    "Katherine Johnson",
    "Barbara McClintock",
    "Lise Meitner",
    "Vera Rubin",
    # Male Scientists
    "Albert Einstein",
    "Isaac Newton",
    "Galileo Galilei",
    "Charles Darwin",
    "Nikola Tesla",
    "Stephen Hawking",
    "Richard Feynman",
    "Niels Bohr",
    "Michael Faraday",
    "Alan Turing",
    # Female Scientists
    "Hypatia",
    "Emmy Noether",
    "Chien-Shiung Wu",
    "Mae Jemison",
    "Tu Youyou",
    "Maria Goeppert Mayer",
    "Rita Levi-Montalcini",
    "Gerty Cori",
    "Mary Anning",
    "Irene Joliot-Curie",  # Sorry Irène, for the accent
    # Male Scientists
    "Gregor Mendel",
    "James Clerk Maxwell",
    "Louis Pasteur",
    "Carl Linnaeus",
    "Erwin Schroedinger",  # Sorry Erwin, for the ö
    "Paul Dirac",
    "Linus Pauling",
    "Carl Sagan",
    "Jonas Salk",
    "Tim Berners-Lee",
]


class ExperimentTracker:
    def __init__(self, root_dir=None, experiment_name=None, job_name=None):
        if root_dir is None:
            root_dir = os.getcwd()
        self.root_dir = root_dir

        self._dict = {}

        if experiment_name is not None:
            self.set_experiment(experiment_name)
        else:
            self.experiment_name = None

        if job_name is not None:
            self.set_job(job_name)
        else:
            self.job_name = None

    def update_dict(self):
        self._dict["root_dir"] = self.root_dir
        self._dict["job_name"] = self.job_name
        self._dict["experiment_name"] = self.experiment_name

    def __setitem__(self, key, value):
        self._dict[key] = value

    def __getitem__(self, key):
        return os.abspath(
            os.path.join(
                self.root_dir, self.experiment_name, self.job_name, self._dict[key]
            )
        )

    def set_experiment(self, name=None):
        name = self._experiment_name(name)
        path = os.path.join(self.root_dir, name)
        if not os.path.isdir(path):
            os.makedirs(path)
        self.experiment_name = name
        self.update_dict()
        return self.experiment_name

    def set_job(self, name=None, template=None):
        if self.experiment_name is None:
            raise ValueError("set experiment first")
        name = self._job_name(name)
        path = os.path.join(self.root_dir, self.experiment_name, name)
        if not os.path.isdir(path):
            if template is None:
                self._create_job(path, name)
            else:
                shutil.copytree(template, path, dirs_exist_ok=False)
        self.job_name = name
        self.update_dict()
        return self.job_name

    def _create_job(self, path, name):
        os.makedirs(path)
        with open(os.path.join(path,"README.md"), "w") as f:
            f.write(
                f"""#{name}
"""
            )

    @staticmethod
    def _experiment_name(name):
        if name is None:
            name = random.choice(FAMOUS_SCIENTISTS).replace(" ", "_")
        name = ExperimentTracker._printable(name)
        return name

    @staticmethod
    def _job_name(name):
        if name is None:
            now = str(datetime.datetime.now().isoformat())
            date = now.split("T")[0]

            r = wonderwords.RandomWord()
            adjective = r.word(
                include_parts_of_speech=["adjectives"],
                word_min_length=3,
                word_max_length=8,
            )
            length = 12 - len(adjective)
            noun = r.word(
                include_parts_of_speech=["nouns"],
                word_min_length=length,
                word_max_length=length,
            )
            name = "_".join((date, adjective, noun))

        name = ExperimentTracker._printable(name)
        return name

    @staticmethod
    def _printable(name_string):
        s_ = "".join(s for s in name_string if s in string.printable)
        return s_

    def dump(self, name=None):
        if name is None:
            name = "job.json"
        with open(name, "w") as f:
            json.dump(self._dict, f)

    @classmethod
    def from_json(cls, file_name):
        with open(file_name, "r") as f:
            d = json.load(f)
        tracker = cls(
            root_dir=d["root_dir"],
            experiment_name=d["experiment_name"],
            job_name=d["job_name"],
        )
        for key, val in d:
            tracker[key] = val
        return tracker

import unittest
import os
import nblibrarian
import subprocess

NOTEBOOKS = [
    "notebooks/dcip/DCIP_2D_Overburden_Pseudosections.ipynb",
    "notebooks/dcip/DC_Building_Pseudosections.ipynb",
    "notebooks/dcip/DC_Cylinder_2D.ipynb",
    "notebooks/em/EM_Pipeline.ipynb",
    "notebooks/em/EM_EM31.ipynb",
    "notebooks/em/FDEM_Inductive_Sphere.ipynb",
    "notebooks/em/FDEM_VMD_Sphere.ipynb",
    "notebooks/em/TDEM_HorizontalLoop_Sphere.ipynb",
    "notebooks/mag/Mag_Dipole.ipynb",
    "notebooks/mag/Mag_FitProfile.ipynb",
    "notebooks/mag/Mag_Induced2D.ipynb",
    "notebooks/mag/MagneticDipoleApplet.ipynb",
    "notebooks/mag/MagneticPrismApplet.ipynb",
    "notebooks/inversion/LinearInversion.ipynb",
]

def tear_down():
    for nb in NOTEBOOKS:
        if os.path.exists(nb):
            os.remove(nb)

    for d in os.listdir('notebooks'):
        os.rmdir(os.path.sep.join(['notebooks', d]))

    os.rmdir('notebooks')
    os.remove('environment.yml')
    os.remove('requirements.txt')

class TestNblibrarian(unittest.TestCase):

    def test_defaults(self):
        lib = nblibrarian.Librarian()

        # default library name should be found
        assert lib.config_file == ".library-config.yml"

        # check that the values being read in are valid
        assert all([
            lib.config["source"]["github"][key] == val for
            key, val in zip(["user", "repo", "branch"], ["geoscixyz", "geosci-labs", "master"])
        ])

        for nb in NOTEBOOKS:
            assert nb in lib.notebook_list, f"{nb} not in notebook list"

        assert lib.content_url == "https://raw.githubusercontent.com/geoscixyz/geosci-labs/master"

    @unittest.expectedFailure
    def test_invalid_config(self):
        lib = nblibrarian.Librarian(".corrupt-library-config.yml")
        lib.source_url

    def test_command_line(self):
        assert(
            subprocess.call([
                "nblibrarian", "--config=.library-config.yml", "--jupyter-include=.jupyter-include", "-v", "--overwrite=False"
            ]) == 0
        )

        for nb in NOTEBOOKS:
            assert(os.path.isfile(nb))

        tear_down()

    def test_command_line_defaults(self):
        assert(
            subprocess.call([
                "nblibrarian"
            ]) == 0
        )

        for nb in NOTEBOOKS:
            assert(os.path.isfile(nb))

        tear_down()

    def test_requirements(self):
        assert(
            subprocess.call([
                "nblibrarian"
            ]) == 0
        )

        for nb in NOTEBOOKS:
            assert(os.path.isfile(nb))

        assert(os.path.isfile('requirements.txt'))
        assert(not os.path.isfile('environment.yml'))


if __name__ == "__main__":
    unittest.main()

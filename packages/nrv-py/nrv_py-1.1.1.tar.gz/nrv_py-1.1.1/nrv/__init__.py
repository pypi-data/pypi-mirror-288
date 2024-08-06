# pylint: skip-file
""" NeuRon Virtualizer, large scale modeling of Peripheral Nervous System with random stimulation waveforms"""

__copyright__ = "2023, Florian Kolbl"
__license__ = "CeCILL"
__version__ = "1.1.1"
__title__ = "NeuRon Virtualizer"
__authors__ = "Florian Kolbl, Roland Giraud, Louis Regnacq, Thomas Couppey"
__contributors__ = __authors__
__project__ = "NeuRon Virtualizer (NRV)"

#####################################
#  check environnement variables    #
#  check correct NRV configuration  #
#####################################
import os
import inspect
import platform


# GMSH must be imported before neuron to prevent installation issues
import gmsh
# create a dummy object to locate frameworks path
class DummyClass:
    """Dummy class"""

    pass

nrv_path = os.path.dirname(os.path.abspath(inspect.getsourcefile(DummyClass)))
root_path = nrv_path.replace("/nrv/", "")
# create the environnement variable NRVPATH if it does not exist
if "NRVPATH" not in os.environ:
    os.environ["NRVPATH"] = nrv_path

# change the permissions on nrv2calm --> shouldn't be needed anymore
'''
if not os.access(nrv_path + "/nrv2calm", os.X_OK):
    mode = os.stat(nrv_path + "/nrv2calm").st_mode
    mode |= (mode & 0o444) >> 2  # copy R bits to X
    os.chmod(nrv_path + "/nrv2calm", mode)
'''
######################
#  Public interface  #
######################
from .backend import compileMods
from .backend.parameters import *
from .backend.NRV_Class import load_any
from .backend.wrappers import *

from .fmod.materials import *
from .fmod.electrodes import *
from .fmod.stimulus import *
from .fmod.extracellular import *
from .fmod.recording import *
from .fmod.FEM.FEM import *
from .fmod.FEM.COMSOL_model import *
from .fmod.FEM.FENICS_model import *

######### May not be requiered at the end ###############
from .fmod.FEM.mesh_creator.MshCreator import *
from .fmod.FEM.mesh_creator.NerveMshCreator import *
from .fmod.FEM.mesh_creator.NRV_Msh import *
from .fmod.FEM.fenics_utils.FEMSimulation import *
from .fmod.FEM.fenics_utils.FEMParameters import *
from .fmod.FEM.fenics_utils.FEMResults import *
from .fmod.FEM.fenics_utils.fenics_materials import *
from .fmod.FEM.fenics_utils.f_materials import *
from .fmod.FEM.fenics_utils.layered_materials import *

########################################################

from .nmod.axons import *
from .nmod.unmyelinated import *
from .nmod.myelinated import *
from .nmod.fascicles import *
from .nmod.axon_pop_generator import *
from .nmod.nerve import *

from .nmod.results.axons_results import *
from .nmod.results.unmyelinated_results import *
from .nmod.results.myelinated_results import *
from .nmod.results.fascicles_results import *
from .nmod.results.nerve_results import *


from .utils.saving_handler import *
from .utils.nrv_function import *
from .utils.cell.CL_postprocessing import *
from .utils.cell.CL_simulations import *
from .utils.fascicle.FL_postprocessing import *

from .optim.CostFunctions import *
from .optim.Optimizers import *
from .optim.Problems import *
from .optim.optim_utils.ContextModifiers import *
from .optim.optim_utils.CostEvaluation import *
from .optim.optim_utils.OptimFunctions import *


from .eit.Protocol import pyeit_protocol
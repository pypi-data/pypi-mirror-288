# package marker
from thonny import get_workbench
from thonny.languages import tr
from thonnycontrib.data_visualization.hierarchical_view import HierarchicalView
from thonnycontrib.data_visualization.graphical_view import GraphicalView
from thonnycontrib.data_visualization.locals_variables_view import LocalVarView

'''Premet de charger les plug-ins au lancement de Thonny'''

def load_plugin() -> None:
    get_workbench().add_view(HierarchicalView, tr("Hierarchical data view"), "s")
    get_workbench().add_view(GraphicalView, tr("Graphical data view"), "s")
    get_workbench().add_view(LocalVarView, tr("Globals and locals variables"), "ne", default_position_key="AAA")

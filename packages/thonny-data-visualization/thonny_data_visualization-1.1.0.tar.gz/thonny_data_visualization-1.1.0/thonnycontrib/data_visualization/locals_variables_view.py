from logging import getLogger
from tkinter import ttk
from thonny.common import ValueInfo

from thonny import get_runner, get_workbench
from thonny.common import InlineCommand
from thonny.languages import tr
from thonny.memory import VariablesFrame
from thonnycontrib.data_visualization.representation_format import repr_format


logger = getLogger(__name__)

class LocalVarView(VariablesFrame):
    def __init__(self, master):
        self._last_progress_message = None
        super().__init__(master)
        
        self.name = "LVV"
        self.repr_db = {}

        ttk.Style().configure("Centered.TButton", justify="center")
        self.back_button = ttk.Button(
            self.tree,
            style="Centered.TButton",
            text=tr("Back to\ncurrent frame"),
            command=self._handle_back_button,
            width=15,
        )

        get_workbench().bind("BackendRestart", self._handle_backend_restart, True)
        get_workbench().bind("ToplevelResponse", self._handle_toplevel_response, True)
        get_workbench().bind("DebuggerResponse", self._debugger_response, True)
        get_workbench().bind("get_globals_response", self._handle_get_globals_response, True)
        
        # records last info from progress messages
        self._last_active_info = None

    def _handle_back_button(self):
        assert self._last_active_info is not None
        if len(self._last_active_info) == 2:
            self.show_variables(*self._last_active_info)

    def _handle_backend_restart(self, event):
        self._clear_tree()

    def _handle_get_globals_response(self, event):
        if "error" in event:
            self._handle_error_response(event["error"])
        elif "globals" not in event:
            self._handle_error_response(str(event))
        else:
            self.show_variables(event["globals"], event["module_name"])

    def _handle_toplevel_response(self, event):
        if "globals" in event:
            self.show_variables(event["globals"], "__main__")
        else:
            get_runner().send_command(InlineCommand("get_globals", module_name="__main__"))
            
    def _debugger_response(self, event):
        self._last_progress_message = event
        var_view = get_workbench().get_view("LocalVarView")
        frame_info = self.get_frame_by_id(event.stack[-1].id)
        var_view.show_variables(frame_info.globals, frame_info.module_name, frame_info.locals)
        
    def get_frame_by_id(self, frame_id):
        for frame_info in self._last_progress_message.stack:
            if frame_info.id == frame_id:
                return frame_info
        raise ValueError("Could not find frame %d" % frame_id)
    
    def show_variables(self, globals_, module_name, locals_ = None, is_active=True):
        self.repr_db = {}
        self.clear_error()
        for obj in globals_:
            repr = globals_[obj].repr
            new_repr, b, h = repr_format(self, repr)
            self.repr_db[repr] = new_repr
            globals_[obj] = ValueInfo(globals_[obj].id, new_repr)
        if not locals_:
            groups = [("GLOBALS", globals_)]
        else:
            for obj in locals_:
                repr = locals_[obj].repr
                new_repr, b, h = repr_format(self, repr)
                self.repr_db[repr] = new_repr
                locals_[obj] = ValueInfo(locals_[obj].id, new_repr)
            groups = [("LOCALS", locals_), ("GLOBALS", globals_)]
        self.update_variables(groups)
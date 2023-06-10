import tkinter as tk

class VerticalScrolledFrame:
    """
    Frame with vertical scrollbars
    """
    def __init__(self, master, **kwargs):
        # Get attributes passed 
        width = kwargs.pop('width', None)
        height = kwargs.pop('height', None)
        bg = kwargs.pop('bg', kwargs.pop('background', None))

        # Create outer frame
        self.outer = tk.Frame(master, **kwargs)

        # Create vertical scrollbar
        self.vsb = tk.Scrollbar(self.outer, orient=tk.VERTICAL)
        self.vsb.pack(fill=tk.Y, side=tk.RIGHT)

        # Create canvas, connect it to scrollbar and add keyboard bindings
        self.canvas = tk.Canvas(self.outer, highlightthickness=0, width=width, height=height, bg=bg)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.canvas['yscrollcommand'] = self.vsb.set
        self.canvas.bind("<Enter>", self._bind_mouse)
        self.canvas.bind("<Leave>", self._unbind_mouse)
        self.canvas.addtag_all("all")   # (added) for configuring width
        self.vsb['command'] = self.canvas.yview

        # Create inner frame
        self.inner = tk.Frame(self.canvas, bg=bg)
        # Pack the inner frame into the canvas with the topleft corner 4 pixels offset
        self.canvas.create_window(0, 0, window=self.inner, anchor='nw')
        self.canvas.bind("<Configure>", self._on_frame_configure) 

        self.outer_attr = set(dir(tk.Widget))

    def __getattr__(self, item):
        if item in self.outer_attr:
            # Geometry attributes etc (eg pack, destroy, tkraise) are passed on to self.outer
            return getattr(self.outer, item)
        else:
            # All other attributes (_w, children, etc) are passed to self.inner
            return getattr(self.inner, item)

    # To configure frame
    def _on_frame_configure(self, event=None):
        x1, y1, x2, y2 = self.canvas.bbox("all")
        height = self.canvas.winfo_height()
        width = self.canvas.winfo_width()
        self.canvas.config(scrollregion = (0,0, x2, max(y2, height)))
        self.canvas.itemconfigure("all", width=width)
        
    # Mouse bindings
    def _bind_mouse(self, event=None):
        self.canvas.bind_all("<4>", self._on_mousewheel)
        self.canvas.bind_all("<5>", self._on_mousewheel)
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    # Unbinding default bindings
    def _unbind_mouse(self, event=None):
        self.canvas.unbind_all("<4>")
        self.canvas.unbind_all("<5>")
        self.canvas.unbind_all("<MouseWheel>")

    # Function for scrolling when using mousewheel
    def _on_mousewheel(self, event):
        """Cross platform support"""
        if event.num == 4 or event.delta > 0:
            self.canvas.yview_scroll(-1, "units" )
        elif event.num == 5 or event.delta < 0:
            self.canvas.yview_scroll(1, "units" )
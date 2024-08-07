from psychopy.experiment.components import Param, getInitVals
from psychopy.localization import _translate
from .. import BaseMonkeyComponent
from pathlib import Path


class MouseMonkeyComponent(BaseMonkeyComponent):
    """
    Monkey which clicks at a specific time and position
    """
    # path to this Component's icon file
    iconFile = Path(__file__).parent / "mouseMonkey.png"
    # Text to display when this Component is hovered over
    tooltip = "Monkey which clicks at a specific time and position"

    def __init__(
        self, 
        exp, 
        parentName, 
        # basic
        name="clickMonkey",
        startType='time (s)', 
        startVal=0.1,
        startEstim='',
        stopType="duration (s)", 
        stopVal=0,
        durationEstim='',
        syncScreenRefresh=False,
        # action
        comp="",
        clickButton=0,
        clickPos=(0, 0),
        clickUnits="$win.units",
        clickMode="both",
        # testing
        disabled=False,
    ):
        # initialise the base class
        BaseMonkeyComponent.__init__(
            self, 
            exp, 
            parentName, 
            # basic
            name=name,
            startType=startType, 
            startVal=startVal,
            startEstim=startEstim,
            stopType=stopType, 
            stopVal=stopVal,
            durationEstim=durationEstim,
            syncScreenRefresh=syncScreenRefresh,
            # action
            comp=comp,
            # testing
            disabled=disabled,
        )
        # --- Action params ---

        self.order += [
            "clickButton",
            "clickPos",
            "clickUnits",
            "clickMode",
        ]
        self.params['clickButton'] = Param(
            clickButton, valType="code", inputType="choice", categ="Action",
            allowedVals=[0, 1, 2],
            allowedLabels=["Left click", "Middle (scroll) click", "Right click"],
            label=_translate("Mouse button"),
            hint=_translate(
                "What mouse button to click?"
            )
        )
        self.params['clickPos'] = Param(
            clickPos, valType="list", inputType="single", categ="Action",
            label=_translate("Click position [x,y]"),
            hint=_translate(
                "Where on screen to click?"
            )
        )
        self.params['clickUnits'] = Param(
            clickUnits, valType="str", inputType="choice", categ="Action",
            allowedVals=[
                "$win.units", "deg", "cm", "pix", "norm", "height", "degFlatPos", "degFlat"
            ],
            allowedLabels=[
                "from exp settings", "deg", "cm", "pix", "norm", "height", "degFlatPos", "degFlat"
            ],
            hint=_translate(
                "Units in which click position are specified"
            ),
            label=_translate("Spatial units"))
            
        self.params['clickMode'] = Param(
            clickMode, valType="str", inputType="choice", categ="Action",
            allowedVals=["both", "click", "release"],
            allowedLabels=[
                _translate("Click and release"),
                _translate("Click only"),
                _translate("Release only"),
            ],
            label=_translate("Click mode"), 
            hint=_translate(
                "Should this monkey click the mouse button at the start time, release at at the "
                "stop time, or do both?"
            ),
            direct=False
        )
    
    def writeStartCode(self, buff):
        # force use of hardware.Mouse over event.Mouse
        code = (
            "from psychopy.hardware.mouse import Mouse\n"
            "event.Mouse = Mouse\n"
        )
        buff.writeIndentedLines(code)
    
    def writeFrameCode(self, buff):
        # write on-start code
        dedent = self.writeStartTestCode(buff)
        if dedent:
            if self.params['clickMode'] in ("click", "both"):
                # if requested, and piloting, click key on start
                code = (
                    "if PILOTING:\n"
                    "    # if piloting, %(name)s will click\n"
                    "    %(name)s.response = %(name)s.comp.setMouseButtonState(\n"
                    "        button=%(clickButton)s,\n"
                    "        pressed=True,\n"
                    "        pos=layout.Position(%(clickPos)s, units=%(clickUnits)s, win=win).pix,\n"
                    "    )\n"
                )
                buff.writeIndentedLines(code % self.params)
            # dedent after
            buff.setIndentLevel(-dedent, relative=True)
        
        # write on-stop code
        dedent = self.writeStopTestCode(buff)
        if dedent:
            if self.params['clickMode'] in ("release", "both"):
                # if requested, and piloting, release key on stop
                code = (
                    "if PILOTING:\n"
                    "    # if piloting, %(name)s will release its click\n"
                    "    %(name)s.response = %(name)s.comp.setMouseButtonState(\n"
                    "        button=%(clickButton)s,\n"
                    "        pressed=False,\n"
                    "        pos=layout.Position(%(clickPos)s, units=%(clickUnits)s, win=win).pix,\n"
                    "    )\n"
                )
                buff.writeIndentedLines(code % self.params)
            # dedent after
            buff.setIndentLevel(-dedent, relative=True)

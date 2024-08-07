from psychopy.experiment.components import Param, getInitVals
from psychopy.localization import _translate
from .. import BaseMonkeyComponent
from pathlib import Path


class KeyboardMonkeyComponent(BaseMonkeyComponent):
    """
    Monkey which presses a key at a specific time
    """
    # path to this Component's icon file
    iconFile = Path(__file__).parent / "keyboardMonkey.png"
    # Text to display when this Component is hovered over
    tooltip = "Monkey which presses a key at a specific time"

    def __init__(
        self, 
        exp, 
        parentName, 
        # basic
        name="keyMonkey",
        startType='time (s)', 
        startVal=0.1,
        startEstim='',
        stopType="duration (s)", 
        stopVal=0,
        durationEstim='',
        syncScreenRefresh=False,
        # action
        comp="",
        pressKey="space",
        pressMode="both",
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
            "pressKey",
            "pressMode",
        ]
        self.params['pressKey'] = Param(
            pressKey, valType="str", inputType="single", categ="Action",
            label=_translate("Key"), 
            hint=_translate(
                "What key should this monkey press?"
            )
        )
        self.params['pressMode'] = Param(
            pressMode, valType="str", inputType="choice", categ="Action",
            allowedVals=["both", "press", "release"],
            allowedLabels=[
                _translate("Press and release"),
                _translate("Press only"),
                _translate("Release only"),
            ],
            label=_translate("Press mode"), 
            hint=_translate(
                "Should this monkey press the key at the start time, release at at the stop time, "
                "or do both?"
            ),
            direct=False
        )
    
    def writeFrameCode(self, buff):
        # write on-start code
        dedent = self.writeStartTestCode(buff)
        if dedent:
            if self.params['pressMode'] in ("press", "both"):
                # if requested, and piloting, press key on start
                code = (
                    "if PILOTING:\n"
                    "    # if piloting, %(name)s will press its key\n"
                    "    %(name)s.response = %(name)s.comp.device.makeResponse(\n"
                    "        code=%(pressKey)s,\n"
                    "        tDown=t,\n"
                    "    )\n"
                )
                buff.writeIndentedLines(code % self.params)
            # dedent after
            buff.setIndentLevel(-dedent, relative=True)
        
        # write on-stop code
        dedent = self.writeStopTestCode(buff)
        if dedent:
            if self.params['pressMode'] in ("release", "both"):
                # if requested, and piloting, release key on stop
                code = (
                    "if PILOTING:\n"
                )
                if self.params['pressMode'] == "release":
                    # if only releasing, get last matching keypress
                    code += (
                    "    # get ongoing keypress so %(name)s can release it\n"
                    "    %(name)s.response = None\n"
                    "    for kp in %(name)s.comp.device.responses:\n"
                    "        if kp.name == %(pressKey)s and kp.code.duration is None:\n"
                    "            %(name)s.response = kp\n"
                    "    if %(name)s.response is None:\n"
                    "        raise ValueError(\n"
                    "            \"%(name)s could not release the %(pressKey)s key as it is not pressed.\"\n"
                    "    )\n"
                    )
                code += (
                    "    # if piloting, %(name)s will release its key\n"
                    "    %(name)s.response.duration = t - %(name)s.response.tDown\n"
                )
                buff.writeIndentedLines(code % self.params)
            # dedent after
            buff.setIndentLevel(-dedent, relative=True)

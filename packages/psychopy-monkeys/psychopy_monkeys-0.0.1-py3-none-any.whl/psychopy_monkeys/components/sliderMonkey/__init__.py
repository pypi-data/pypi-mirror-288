from psychopy.experiment.components import Param, getInitVals
from psychopy.localization import _translate
from .. import BaseMonkeyComponent
from pathlib import Path


class SliderMonkeyComponent(BaseMonkeyComponent):
    """
    Monkey which makes a Slider response
    """
    # path to this Component's icon file
    iconFile = Path(__file__).parent / "sliderMonkey.png"
    # text to display when this Component is hovered over
    tooltip = "Monkey which makes a Slider response"

    def __init__(
        self, 
        exp, 
        parentName, 
        # basic
        name="sliderMonkey",
        startType='time (s)', 
        startVal=0.1,
        startEstim='',
        stopType="duration (s)", 
        stopVal=0,
        durationEstim='',
        syncScreenRefresh=False,
        # action
        comp="",
        sliderResp=0,
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
            "sliderResp",
        ]
        self.params['sliderResp'] = Param(
            sliderResp, valType="code", inputType="single", categ="Action",
            label=_translate("Slider response"),
            hint=_translate(
                "What value to choose on the Slider?"
            )
        )
    
    def writeFrameCode(self, buff):
        # write on-start code
        dedent = self.writeStartTestCode(buff)
        if dedent:
            # if piloting, set slider position on start
            code = (
                "if PILOTING:\n"
                "    # if piloting, %(name)s will start making a response\n"
                "    %(name)s.response = %(name)s.comp.markerPos = %(sliderResp)s\n"
            )
            buff.writeIndentedLines(code % self.params)
            # dedent after
            buff.setIndentLevel(-dedent, relative=True)
        
        # write on-active code
        dedent = self.writeActiveTestCode(buff)
        if dedent:
            # if piloting, continuously update marker pos while active
            code = (
                "if PILOTING:\n"
                "    # if piloting, %(name)s will continuously update the marker pos of %(comp)s\n"
                "    %(name)s.response = %(name)s.comp.markerPos = %(sliderResp)s\n"
            )
            buff.writeIndentedLines(code % self.params)
            # dedent after
            buff.setIndentLevel(-dedent, relative=True)
        
        # write on-stop code
        dedent = self.writeStopTestCode(buff)
        if dedent:
            # if requested, and piloting, release key on stop
            code = (
                "if PILOTING:\n"
                "    # if piloting, %(name)s will finish making a response\n"
                "    %(name)s.response = %(name)s.comp.rating = %(sliderResp)s\n"
            )
            buff.writeIndentedLines(code % self.params)
            # dedent after
            buff.setIndentLevel(-dedent, relative=True)

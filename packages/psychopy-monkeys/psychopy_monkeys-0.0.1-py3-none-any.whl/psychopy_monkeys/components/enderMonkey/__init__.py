from psychopy.experiment.components import Param, getInitVals
from psychopy.localization import _translate
from .. import BaseMonkeyComponent
from pathlib import Path


class RoutineEnderMonkeyComponent(BaseMonkeyComponent):
    """
    Monkey which ends the Routine
    """
    # path to this Component's icon file
    iconFile = Path(__file__).parent / "enderMonkey.png"
    # text to display when this Component is hovered over
    tooltip = "Monkey which ends the Routine"

    def __init__(
        self, 
        exp, 
        parentName, 
        # basic
        name="enderMonkey",
        startType='time (s)', 
        startVal=0.1,
        startEstim='',
        stopType="duration (s)", 
        stopVal=0,
        durationEstim='',
        syncScreenRefresh=False,
        # action
        comp="",
        showCountdown=True,
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
            # testing
            disabled=disabled,
        )

        # --- Basic params ---
        # we don't need comp as the ender monkey will simply act on the Routine it's in
        del self.params['comp']
        # add a forceEndRoutine param so the Comp registers as one which can end Routine, but hide it
        self.params['forceEndRoutine'] = Param(
            True, valType="code"
        )
        self.depends.append({
            'dependsOn': "forceEndRoutine",  # if...
            'condition': "",  # is...
            'param': "forceEndRoutine",  # then...
            'true': "hide",  # should...
            'false': "hide",  # otherwise...
        })

        # --- Action params ---

        self.order += [
            "showCountdown",
        ]
        self.params['showCountdown'] = Param(
            showCountdown, valType="code", inputType="bool", categ="Action",
            label=_translate("Show countdown?"),
            hint=_translate(
                "If True, will display an orange bar counting down from start time to stop time."
            )
        )
        # disable "show countdown" for conditional stop as there isn't a fixed time
        self.depends.append({
            'dependsOn': "stopType",  # if...
            'condition': "== 'condition'",  # is...
            'param': "showCountdown",  # then...
            'true': "disable",  # should...
            'false': "enable",  # otherwise...
        })
    
    def writeInitCode(self, buff):
        # get init values
        inits = getInitVals(self.params)
        # create a simple monkey to track status and etc.
        code = (
            "%(name)s = Monkey(\n"
            "    name='%(name)s',\n"
            ")\n"
        )
        buff.writeIndentedLines(code % inits)
        # add countdown
        code = (
            "%(name)s.countdown = visual.Progress(\n"
            "    win, direction='horizontal', \n"
            "    size=(win.size[0], 60), pos=(-win.size[0]/2, -win.size[1]/2), \n"
            "    anchor='bottom-left', units='pix', \n"
            "    barColor='#EC9703', backColor=None, borderColor=None,\n"
            "    autoDraw=False, \n"
            ")\n"
        )
        buff.writeIndented(code % self.params)
    
    def writeFrameCode(self, buff):
        startTime, duration, nonSlipSafe = self.getStartAndDuration()

        # write on-start code
        dedent = self.writeStartTestCode(buff)
        if dedent:
            if self.params['showCountdown'] and nonSlipSafe:
                # if piloting and showing countdown, start drawing it on start
                code = (
                    "if PILOTING:\n"
                    "    # if piloting, draw countdown to %(name)s ending the Routine\n"
                    "    %(name)s.countdown.setAutoDraw(True)\n"
                )
                buff.writeIndentedLines(code % self.params)
            # dedent after
            buff.setIndentLevel(-dedent, relative=True)
        
        # write on-active code
        dedent = self.writeActiveTestCode(buff)
        if dedent:
            if self.params['showCountdown'] and nonSlipSafe:
                # if piloting and showing countdown, update countdown
                code = (
                    f"if PILOTING:\n"
                    f"    # if piloting, update countdown to %(name)s ending the Routine\n"
                    f"    %(name)s.countdown.progress = (t - {startTime}) / {duration}\n"
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
                "    # if piloting, %(name)s will end the Routine\n"
                "    continueRoutine = False\n"
            )
            buff.writeIndentedLines(code % self.params)
            # dedent after
            buff.setIndentLevel(-dedent, relative=True)

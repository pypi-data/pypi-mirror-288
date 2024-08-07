from psychopy.experiment.components import BaseComponent, Param, getInitVals
from psychopy.localization import _translate
from pathlib import Path


class BaseMonkeyComponent(BaseComponent):
    """
    Base class for all PsychoPy Monkey Components, implements the base minimum features.
    """
    # mark it as coming from this plugin
    plugin = "psychopy-monkeys"
    # only implemented in Python, for now...
    targets = ["PsychoPy"]
    # all monkeys go in the same category
    categories = ['Monkeys']
    # what is the earliest version of PsychoPy this Component works with?
    version = "2024.2.0"

    def __init__(
        self, 
        exp, 
        parentName, 
        # basic
        name="monkey",
        startType='frame N', 
        startVal='1',
        startEstim='',
        stopType='duration (frames)', 
        stopVal='1',
        durationEstim='',
        syncScreenRefresh=False,
        # action
        comp="",
        # testing
        disabled=False,
    ):
        # initialise base class
        BaseComponent.__init__(
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
            saveStartStop=False,
            syncScreenRefresh=syncScreenRefresh,
            # testing
            disabled=disabled,
        )

        # import the monkey class
        self.exp.requireImport("Monkey", importFrom='psychopy_monkeys')

        # --- Basic params ---
        self.order += [
            "comp",
        ]
        self.params['comp'] = Param(
            comp, valType="code", inputType="single", categ="Basic",
            label=_translate("Component"),
            hint=_translate(
                "Component for this monkey to act on."
            ),
        )
    
    def writeInitCode(self, buff):
        # get init values
        inits = getInitVals(self.params)
        # create a simple monkey to track status and etc.
        code = (
            "%(name)s = Monkey(\n"
            "    name='%(name)s',\n"
            "    comp=%(comp)s,\n"
            ")\n"
        )
        buff.writeIndentedLines(code % inits)


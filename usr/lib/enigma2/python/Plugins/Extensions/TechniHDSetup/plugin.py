#######################################################################
#
#    TechniHD Setup
#    Original Source Coded by Vali (c)2011 (FlexControl)
#
#######################################################################
                                                            

from Plugins.Plugin import PluginDescriptor
from Screens.Screen import Screen
from Screens.MessageBox import MessageBox
from Screens.Standby import TryQuitMainloop
from Components.ActionMap import ActionMap
from Components.Pixmap import Pixmap
from Components.config import config, ConfigSubsection, getConfigListEntry, ConfigSelection, ConfigInteger, ConfigYesNo
from Components.ConfigList import ConfigListScreen
from Tools.Directories import fileExists
from skin import parseColor
from os import system


config.technihd = ConfigSubsection()
config.technihd.SecondInfobar = ConfigSelection(default="NowAndNextInfo", choices = [("TunerAndCryptInfos", _("TunerState, Crypt, SNR,...")),("NowAndNextInfo", _("Now and Next EventInfo"))])
config.technihd.Infobar = ConfigSelection(default="NextEventInfo", choices = [("BouquetInfo", _("BouquetInfo")),("NextEventInfo", _("Next EventInfo"))])
config.technihd.InfobarSatPos = ConfigYesNo(default=False)

class TechniHDSetup(ConfigListScreen, Screen):
	skin = """
		<screen name="TechniHDSetup" position="center,center" size="600,580" title="TechniHD Setup">
			<ePixmap alphatest="blend" pixmap="TechniHD/buttons/red.png" position="67,528" size="40,40" zPosition="2" />
			<ePixmap alphatest="blend" pixmap="TechniHD/buttons/green.png" position="322,528" size="40,40" zPosition="2" />
			<eLabel font="Regular;20" halign="left" position="100,529" size="180,26" text="Cancel" transparent="1" />
			<eLabel font="Regular;20" halign="left" position="354,529" size="180,26" text="Save" transparent="1" />
			<widget itemHeight="30" name="config" position="51,339" scrollbarMode="showOnDemand" size="492,165" font="Regular; 16" />
		        <eLabel position="48,30" size="492,253" zPosition="1" backgroundColor="grey" />
                        <eLabel position="50,32" size="488,249" zPosition="2" backgroundColor="dblau" />
                        <widget name="preview" zPosition="3" position="60,41" size="469,230" alphatest="blend" />
		</screen>"""

	def __init__(self, session):
		Screen.__init__(self, session)
		self.session = session
		self.datei = "/usr/share/enigma2/TechniHD/skin.xml"
		self.data = "/usr/lib/enigma2/python/Plugins/Extensions/TechniHDSetup/preview/"
		self["preview"] = Pixmap()
		list = []
		list.append(getConfigListEntry(_("Show SecondInfobar with:"), config.technihd.SecondInfobar))
		list.append(getConfigListEntry(_("Show Infobar with:"), config.technihd.Infobar))
		list.append(getConfigListEntry(_("Show Infobar with OrbitalPosition:"), config.technihd.InfobarSatPos))
		ConfigListScreen.__init__(self, list, on_change = self.UpdateComponents)
		self["actions"] = ActionMap(["OkCancelActions", "ColorActions"], 
									{
									"red": self.exit, 
									"green": self.save,
									"cancel": self.exit
									}, -1)
		self.onLayoutFinish.append(self.UpdateComponents)

	def UpdateComponents(self):
		prev = self.data + "sib-" + config.technihd.SecondInfobar.value + ".png"
                if fileExists(prev):
			self["preview"].instance.setPixmapFromFile(prev)

	def save(self):
		for x in self["config"].list:
			x[1].save()
		try:
			skin_lines = []
			skn_file = self.datei
			skFile = open(skn_file, "r")
			file_lines = skFile.readlines()
			for x in file_lines:
				if 'name="SecondInfoBarDisabled"' in x:
					if config.technihd.SecondInfobar.value == "TunerAndCryptInfos":
						x = '<screen name="SecondInfoBar" title="Second InfoBar Normal" position="0,0" zPosition="11" size="1280,720" flags="wfNoBorder" backgroundColor="transparent">\n'
				elif 'title="Second InfoBar Normal"' in x:	
                                        if config.technihd.SecondInfobar.value == "NowAndNextInfo":
						x = '<screen name="SecondInfoBarDisabled" title="Second InfoBar Normal" position="0,0" zPosition="11" size="1280,720" flags="wfNoBorder" backgroundColor="transparent">\n'
				elif 'EventNextInformation' in x:
					if config.technihd.Infobar.value == "BouquetInfo":
						x = '<!-- BouquetInformation!! do not change this line --><widget source="session.CurrentService" render="Label" position="255,608" size="760,27" font="hd;22" halign="left" backgroundColor="hblau" transparent="1"><convert type="BouquetInfo">Bouquet</convert></widget>\n'
				elif 'BouquetInformation' in x:	
                                        if config.technihd.Infobar.value == "NextEventInfo":
						x = '<!-- EventNowAndNextInformation!! do not change this line --><widget source="session.Event_Next" render="Label" position="241,607" size="91,25" font="Regular2; 20" halign="center" backgroundColor="hblau" transparent="1"><convert type="EventTime">StartTime</convert><convert type="ClockToText">Format:%H:%M</convert></widget><widget source="session.Event_Next" render="Label" position="319,607" size="86,25" font="Regular2; 20" halign="center" backgroundColor="hblau" transparent="1"><convert type="EventTime">EndTime</convert><convert type="ClockToText">Format:- %H:%M</convert></widget><widget source="session.Event_Next" render="Label" position="414,608" size="600,25" font="hd;22" halign="left" backgroundColor="hblau" transparent="1"><convert type="EventName">Name</convert></widget>\n'
				elif 'ChannelNameInformation' in x:
					if config.technihd.InfobarSatPos.value == True:
						x = '<!-- OrbitPosAndChanNameInformation!! do not change this line --><widget source="session.CurrentService" render="Label" position="254,648" size="91,25" font="Regular2; 20" valign="center" backgroundColor="background" transparent="1"><convert type="ServiceOrbitalPosition">Short</convert></widget><widget source="session.CurrentService" render="Label" position="335,642" size="494,37" font="Regular; 30" valign="center" backgroundColor="background" transparent="1" zPosition="1"><convert type="ServiceName">Name</convert></widget>\n'
				elif 'OrbitPosAndChanNameInformation' in x:
					if config.technihd.InfobarSatPos.value == False:
						x = '<!-- ChannelNameInformation!! do not change this line --><widget source="session.CurrentService" render="Label" position="255,642" size="572,37" font="Regular; 30" valign="center" backgroundColor="background" transparent="1" zPosition="1"><convert type="ServiceName">Name</convert></widget>\n'
				skFile.close()
                                skin_lines.append(x)
			xFile = open(self.datei, "w")
			for x in skin_lines:
				xFile.writelines(x)
			xFile.close()
		except:
			self.session.open(MessageBox, _("Error"), MessageBox.TYPE_ERROR)
		restartbox = self.session.openWithCallback(self.restartGUI,MessageBox,_("TechniHD needs a restart to apply."), MessageBox.TYPE_YESNO)
		restartbox.setTitle(_("Restart?"))

	def restartGUI(self, answer):
		if answer is True:
			self.session.open(TryQuitMainloop, 3)
		else:
			self.close()

	def exit(self):
		for x in self["config"].list:
			x[1].cancel()
		self.close()


def main(session, **kwargs):
	session.open(TechniHDSetup)
	
def setup(menuid):
    if menuid == 'mainmenu':
        return [(_('TechniHD') + " " + _('Setup'),
          main,
          'TechniHDSetup',
          45)]
    return []

def Plugins(**kwargs):
	return PluginDescriptor(name="TechniHDSetup", description=_("Setup for TechniHD-skin"), where = PluginDescriptor.WHERE_MENU, fnc=setup)

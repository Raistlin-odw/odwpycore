import sys
# deadline use ironPython, so add python26's pythonpath
# after this, we can use 'os' and some other modules
sys.path.append('S:/workflowtools_ep20/software/python26')

import time
import os

from System.IO import *
from System.Text import *

from Deadline.Events import *
from Deadline.Scripting import *

PROJECT = 'S:/E020DW/DWep20'
IMAGES_PB = '%s/images_pb' % PROJECT
SCENE_PB = '%s/episodes_pb' % PROJECT
STOP_FILE = 'd:/stop.txt'

######################################################################
## This is the function that Deadline calls to get an instance of the
## main DeadlineEventListener class.
######################################################################
def GetDeadlineEventListener():
	return MyEvent()

######################################################################
## This is the main DeadlineEventListener class for MyEvent.
######################################################################
class MyEvent (DeadlineEventListener):
	
	def set_shot_name(self,shotName):
		'''set shot name
		'''
		self.ShotName = shotName
		
	def read_trigger_file(self):
		with open(self.File_Trigger,'r') as f:
			self.File_Trigger_Temp = f.read()
			
	def get_post_bat_file(self):
		l = self.ShotName.split('_')
		#outputFilePath = '%s/%s/%s/%s' % (IMAGES_PB,l[0]+'_'+l[1],l[2],self.ShotName)
		outputFilePath = '{imPB}/{ep}/{seq}/{shot}'.format(imPB=IMAGES_PB,ep='%s_%s' % (l[0],l[1]),\
														seq=l[2],shot=self.ShotName)
		outputFileName = '%s/%s' % (outputFilePath,self.ShotName)
		self.File_Bat_Post= '%s.bat' % outputFileName
		print self.File_Bat_Post
		
	def get_pre_bat_file(self):
		l = self.ShotName.split('_')
		#mayaScene_dir = '%s/%s/%s/%s' % (SCENE_PB,l[0]+'_'+l[1],l[2],self.ShotName)
		mayaScene_dir = '{scene}/{ep}/{seq}/{shot}'.format(scene=SCENE_PB,ep='%s_%s' % (l[0],l[1]),\
														seq=l[2],shot=self.ShotName)
		self.File_Bat_Pre = '%s/%s.bat' % (mayaScene_dir,self.ShotName)
		self.File_Trigger = '%s/%s.txt' % (mayaScene_dir,self.ShotName)
		print self.File_Bat_Pre
			
	def OnJobStarted(self,job):
		'''overwrite default
		use os.system to execute set rendering settings and some other operations before
		Maya scene can be render
		'''
		if not job.JobName.startswith('pb_'):
			return
		shot_name = job.JobName.replace('pb_','')
		self.set_shot_name(shot_name)
		self.get_pre_bat_file()

		os.system('start %s' % self.File_Bat_Pre)
		self.read_trigger_file()
		print 'file_trigger_temp:', self.File_Trigger_Temp
		while True:
			if os.path.exists( self.File_Trigger_Temp ):
				os.remove(self.File_Trigger_Temp)
				break
			elif os.path.exists( STOP_FILE ):
				break
			else:
				print '*'
				time.sleep(2)
		
	def OnJobFinished( self, job ):
		'''overwrite default 
		generate quicktime movie after Maya rendering job complete
		use RVIO to generate movie
		'''
		
		movieSettings = GetConfigEntryWithDefault( "QTSettings", "" ).strip()
		
		if not job.JobName.startswith('pb_'):
			return
		print 'job.JobName:%s' % job.JobName
		
		outputDirectories = job.JobOutputDirectories
		#outputFilenames = job.JobOutputFileNames
		shot_name = job.JobName.replace('pb_','')
		f = '%s.0%s.tga' % (shot_name,job.FirstFrame)
		outputFilenames = [f]
		
		# get audio file
		self.set_shot_name(shot_name)
		#self.get_audio()
		self.get_post_bat_file()
		os.system('start %s' % self.File_Bat_Post)


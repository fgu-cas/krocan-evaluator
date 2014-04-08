#!/usr/bin/env python
import sys, os, csv, re, math
import matplotlib.pyplot as plt
from PyQt4.QtGui import QApplication, QDialog, QFileDialog, QMessageBox
from ui_krocan import Ui_Krocan

def processFile(track):
  frames = []
  params = {}
  with open(track, 'r') as f:
    for line in f:
      if not re.match('^[ ]*(\%|//)', line):
        frames.append(re.split("[ ]+", line))
      else:
        tmp = re.findall('%ArenaCenterXY.0 \( ([0-9.]+) [0-9.]+ \)', line)
        if tmp:
          params["arena_x"] = float(tmp[0])
        tmp = re.findall('%ArenaCenterXY.0 \( [0-9.]+ ([0-9.]+) \)', line)
        if tmp:
          params["arena_y"] = float(tmp[0])
        tmp = re.findall('ArenaDiameter_m.0 \(( [0-9.]+ )\)', line)
        if tmp:
          params["diameter"] = float(tmp[0])
        tmp = re.findall('ReinforcedSector.0 \( ([0-9.]+) \)', line)
        if tmp:
          params["shock_radius"] = float(tmp[0])
        tmp = re.findall('TrackerResolution_PixPerCM.0 \( ([0-9.]+) \)', line)
        if tmp:
          params["pix_per_cm"] = float(tmp[0])
#todo: add a general solution
  return (frames, params)

def analyseTrack(frames, params):
  frames = [f for f in frames if f[2] is not '0' and f[3] is not '0']
  entrances = 0
  outside = True
  for frame in frames:
    if frame[5] != '0': # frame[5] = state
      if outside:
        outside = False
        entrances += 1
    else:
      outside = True

  distance = 0
  for frame_pair in zip(frames[::5], frames[5::5]):
    distance += math.hypot(float(frame_pair[0][2])-float(frame_pair[1][2]), float(frame_pair[0][3])-float(frame_pair[1][3]))
  distance /= params["pix_per_cm"]

  max_time_avoided = 0
  outside = True
  first_timestamp = frames[0][1]
  for frame in frames:
    if frame[5] != '0':
      current_time_avoided = int(frame[1]) - int(first_timestamp)
      if current_time_avoided > max_time_avoided:
        max_time_avoided = current_time_avoided
      outside = False
    elif not outside:
      outside = True
      first_timestamp = frame[1]

  time_first_entrance = 0
  for frame in frames:
    if frame[5] != '0':
      time_first_entrance = frame[1]
      break

  shocks = 0
  shocking = False
  for frame in frames:
    if frame[5] == '2':
      if not shocking:
        shocking = True
        shocks += 1
    else:
      shocking = False

  frames_in_centre = 0
  inside = (params["diameter"]/2)/math.sqrt(2)
  for frame in frames:
    if math.hypot(float(frame[2])-params["arena_x"], float(frame[3])-params["arena_y"]) < inside:
      frames_in_centre+=1
  center_to_periphery = round(frames_in_centre/len(frames), 3)
  
  return [ entrances, round(distance, 2), max_time_avoided, time_first_entrance, shocks, center_to_periphery ]

def renderGraphs(tracks, params, filename):

  arena_frame = plt.subplot2grid((1,2), (0,0))
  arena_frame.set_title("Rat track [Arena frame]")
  arena_frame.set_xlim([params["arena_x"]-params["diameter"]/2,params["arena_x"]+params["diameter"]/2])
  arena_frame.set_ylim([params["arena_y"]-params["diameter"]/2,params["arena_y"]+params["diameter"]/2])
  arena_frame.set_aspect('equal', adjustable='box')
  arena_frame.axis('off')
  arena_frame.add_artist(plt.Circle((params["arena_x"],params["arena_y"]),params["diameter"]/2,color='r',fill=False))
  arena_frame.plot([float(f[2]) for f in tracks[0] if f[2] is not '0'], [float(f[3]) for f in tracks[0] if f[3] is not '0'])

  xvals = []
  yvals = []
  for i in range(min(len(tracks[0]), len(tracks[1]))):
    # god forgive me
    if not ((tracks[0][i][2] is '0' and tracks[0][i][3] is '0') or (tracks[1][i][2] is '0' and tracks[1][i][3] is '0')):
      xvals.append(float(tracks[0][i][2]) - float(tracks[1][i][2]))
      yvals.append(float(tracks[0][i][3]) - float(tracks[1][i][3]))

  robot_frame = plt.subplot2grid((1,2), (0,1))
  robot_frame.set_title("Rat track [Robot frame]")
  robot_frame.set_xlim(-params["diameter"], params["diameter"])
  robot_frame.set_ylim(-params["diameter"], params["diameter"])
  robot_frame.set_aspect('equal', adjustable='box')
  robot_frame.axis('off')
  robot_frame.add_artist(plt.Circle((0, 0), params["shock_radius"],color='y',fill=False))
  robot_frame.plot(xvals, yvals) 

  # histogram = plt.subplot2grid((2,2), (1,0), colspan=2)

  plt.savefig(filename)

class KrocanEvaluator(QDialog, Ui_Krocan):
  
  files = []

  def __init__(self):
    QDialog.__init__(self)
    self.setupUi(self)

    self.addButton.clicked.connect(self.addButtonClicked)
    self.removeButton.clicked.connect(self.removeButtonClicked)
    self.processButton.clicked.connect(self.processButtonClicked)

    self.show()

  def addButtonClicked(self, _):
    selected_files = QFileDialog.getOpenFileNames(self, "Open tracks", "", "Logs (*.dat)")
    row = self.fileList.currentRow()
    if row is not -1:
      self.files[row+1:row+1] = selected_files
    else:
      self.files += selected_files
    self.updateUI()

  def removeButtonClicked(self, _):
    row = self.fileList.currentRow()
    if row is not -1:
      self.files.pop(row)
    self.updateUI()

  def processButtonClicked(self, _):
    output_dir = QFileDialog.getExistingDirectory(self, "Output directory")
    with open(output_dir+'/tracks.csv', 'w') as f:
      writer = csv.writer(f)
      writer.writerow([ "Filename", "Entrances", "Distance", "Maximum Time Avoided", "Time to first entrance", "Shocks", "Time spent in center"])
      for track in self.files:
        writer.writerow([os.path.basename(track)] + analyseTrack(*processFile(track)))
    for track_pair in zip(self.files[::2], self.files[1::2]):
      rat_frames, params = processFile(track_pair[0])
      robot_frames, _ = processFile(track_pair[1])
      renderGraphs((rat_frames, robot_frames), params, track_pair[0]+'.png')
    message = QMessageBox()
    message.setText("Processing successful!\nSaved into \"%s\"" % output_dir)
    message.exec_()

  def updateUI(self):
    if len(self.files) > 0 and len(self.files) % 2 == 0:
      self.processButton.setEnabled(True)
    else:
      self.processButton.setEnabled(False)
    self.fileList.clear()
    rat = True
    for file in self.files:
      self.fileList.addItem("[%s] %s" % ("RAT" if rat else "ROB", file))
      rat = not rat

def main():
  app = QApplication(sys.argv)
  evaluator = KrocanEvaluator()
  sys.exit(app.exec_())

if __name__ == '__main__':
  main()


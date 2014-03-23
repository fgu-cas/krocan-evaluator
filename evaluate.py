#!/usr/bin/env python
import sys, os, csv, re, math
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
  for frame_pair in zip(frames, frames[1:]):
    distance += math.hypot(float(frame_pair[0][2]), float(frame_pair[1][2]))
  # distance *= cm_per_px

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


class KrocanEvaluator(QDialog, Ui_Krocan):
  
  hasFiles = False

  def __init__(self):
    QDialog.__init__(self)
    self.setupUi(self)

    self.addButton.clicked.connect(self.addButtonClicked)
    self.removeButton.clicked.connect(self.removeButtonClicked)
    self.processButton.clicked.connect(self.processButtonClicked)

    self.show()

  def addButtonClicked(self, _):
    files = QFileDialog.getOpenFileNames(self, "Open tracks", "", "Logs (*.dat)")
    if (len(files) is not 0):
      if ('/' not in self.fileList.item(0).text()):
        self.fileList.clear()
        self.hasFiles = True
      if self.fileList.currentRow() is not -1:
        self.fileList.insertItems(self.fileList.currentRow()+1, files)
      else:
        self.fileList.addItems(files)

  def removeButtonClicked(self, _):
    if self.hasFiles:
      self.fileList.takeItem(self.fileList.row(self.fileList.currentItem()))

  def processButtonClicked(self, _):
    if not self.hasFiles:
      self.addButtonClicked(_)
    if self.hasFiles:
      files = []
      for i in range(0, self.fileList.count()):
        files.append(self.fileList.item(i).text())
      # files.sort(key= lambda filename: "_".join(filename.split("_")[:-1]))
      output_filename = QFileDialog.getSaveFileName(self, "Save .csv", "", "CSV files (*.csv)")
      if output_filename[-4:] != ".csv":
        output_filename += ".csv"
      with open(output_filename, 'w') as f:
        writer = csv.writer(f)
        writer.writerow([ "Filename", "Entrances", "Distance", "Maximum Time Avoided", "Time to first entrance", "Shocks", "Time spent in center"])
        for track in files:
          writer.writerow([os.path.basename(track)] + analyseTrack(*processFile(track)))
      message = QMessageBox()
      message.setText("Processing successful!\nSaved into \"%s\"" % output_filename)
      message.exec_()

def main():
  app = QApplication(sys.argv)
  evaluator = KrocanEvaluator()
  sys.exit(app.exec_())

if __name__ == '__main__':
  main()


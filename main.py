import datetime
import os
import subprocess
import sys
import time
import traceback

from PySide2 import QtWidgets, QtGui
from PySide2.QtGui import QFontDatabase

from Main_Window import Ui_Form


# from better_ffmpeg_progress import FfmpegProcess


# supported_color_space = ['libx264 (最佳品質)', 'yuv420p (兼容性)']


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.ui = Ui_Form()
        self.ui.setupUi(self)

        QFontDatabase.addApplicationFont("NotoSansTC-Regular.otf")
        # self.ui.Color.addItems(supported_color_space)
        # self.ui.Resolution_W.setText("1920")
        # self.ui.Resolution_H.setText("1080")
        # self.ui.ErrorLog.moveCursor(QtGui.QTextCursor.End)
        self.scrollbar = (
            self.ui.ErrorLog.verticalScrollBar()
        )  # the self.scrollbar is the same as your self.console_window

        try:
            time.sleep(0.1)  # needed for the refresh
            self.scrollbar.setValue(10000)  # try input different high value

        except:
            pass  # when it is not available

        self.ui.InputButton.clicked.connect(self.open_folder)
        self.ui.OutputButton.clicked.connect(self.open_file)
        self.ui.StartButton.clicked.connect(self.start)
        self.ui.Progress.setEnabled(False)

    def open_folder(self):
        input_dir = QtWidgets.QFileDialog.getExistingDirectory(
            self, "選擇資料夾(請確保只有要輸入的圖片以避免錯誤)"
        )
        if input_dir:
            self.ui.InputDir.setText(input_dir)
        else:
            print("No Directory Selected")

    def open_file(self):
        output_dir = QtWidgets.QFileDialog.getSaveFileName(
            self, "選擇輸出檔案", "", "MPEG-4 (*.mp4)"
        )
        if output_dir[0]:
            self.ui.OutputDir.setText(output_dir[0])
        else:
            print("No File Selected")

    def start(self):
        if self.ui.InputDir.text() == "":
            QtWidgets.QMessageBox.information(
                self, "警告", "請選擇輸入資料夾", QtWidgets.QMessageBox.Close
            )
            return False
        if self.ui.OutputDir.text() == "":
            QtWidgets.QMessageBox.information(
                self, "警告", "請選擇輸出檔案", QtWidgets.QMessageBox.Close
            )
            return False
        """
        if self.ui.Resolution_W.text() == "":
            QtWidgets.QMessageBox.information(self, "警告", "請輸入解析度(寬)", QtWidgets.QMessageBox.Close)
            return False
        if self.ui.Resolution_H.text() == "":
            QtWidgets.QMessageBox.information(self, "警告", "請輸入解析度(長)", QtWidgets.QMessageBox.Close)
            return False
        """
        input_dir = self.ui.InputDir.text()
        if os.path.isdir(input_dir) is False:
            QtWidgets.QMessageBox.information(
                self, "警告", "輸入資料夾不存在", QtWidgets.QMessageBox.Close
            )
            return False
        output_dir = self.ui.OutputDir.text()
        """
        if self.ui.Color.currentText() == "libx264 (最佳品質)":
            color_space = "libx264"
        else:
            color_space = "yuv420p"
        """
        resolution_w = self.ui.Resolution_W.text()
        resolution_h = self.ui.Resolution_H.text()
        frame_rate = self.ui.Framerate.text()
        fps = self.ui.FPS.text()
        file_format = self.ui.FileFormat.text()
        if file_format == "":
            QtWidgets.QMessageBox.information(
                self, "警告", "請輸入檔案格式", QtWidgets.QMessageBox.Close
            )
            return False
        elif file_format.find(".") != -1:
            file_format = file_format.replace(".", "")
        if resolution_w and resolution_h:
            if resolution_w.isdigit() is False:
                QtWidgets.QMessageBox.information(self, "警告", "解析度(寬)請輸入數字")
                return False
            if resolution_h.isdigit() is False:
                QtWidgets.QMessageBox.information(self, "警告", "解析度(長)請輸入數字")
                return False
            if int(resolution_w) < 1 or int(resolution_h) < 1:
                QtWidgets.QMessageBox.information(self, "警告", "解析度(寬)與(長)請輸入大於0的數字")
                return False
            if int(resolution_w) != float(resolution_w) or int(resolution_h) != float(
                resolution_h
            ):
                QtWidgets.QMessageBox.information(self, "警告", "解析度(寬)與(長)請輸入整數")
                return False
        if os.path.isfile(output_dir) is True:
            if QtWidgets.QMessageBox.Yes == QtWidgets.QMessageBox.warning(
                self,
                "警告",
                "輸出檔案已存在，是否覆寫",
                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                QtWidgets.QMessageBox.Yes,
            ):
                print("Overwrite")
            else:
                print("Cancel")
                return False

        print("Start")
        self.ui.StartButton.setEnabled(False)
        self.ui.StartButton.setText("處理中...")
        try:
            if resolution_w and resolution_h:
                process_log = subprocess.Popen(
                    [
                        "ffmpeg.exe",
                        "y",
                        "-framerate",
                        f"1/{frame_rate}",
                        "-i",
                        f"{input_dir}/%3d.{file_format}",
                        "-c:v",
                        "libx264",
                        "-vf",
                        f"fps={fps}",
                        "-pix_fmt",
                        "yuv420p",
                        f"{output_dir}",
                        "-s",
                        f"{resolution_w}x{resolution_h}",
                    ],
                    stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE,
                )
            else:
                process_log = subprocess.Popen(
                    [
                        "ffmpeg.exe",
                        "-y",
                        "-framerate",
                        f"1/{frame_rate}",
                        "-i",
                        f"{input_dir}/%3d.{file_format}",
                        "-c:v",
                        "libx264",
                        "-vf",
                        f"fps={fps}",
                        "-pix_fmt",
                        "yuv420p",
                        f"{output_dir}",
                    ],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    shell=True,
                )
                process_log_text = process_log.communicate()[1].decode("utf-8")
                print(process_log_text)
                self.ui.ErrorLog.setText(process_log_text)
            self.ui.ErrorLog.moveCursor(QtGui.QTextCursor.End)
        except:
            self.ui.ErrorLog.setText("處理失敗")
            QtWidgets.QMessageBox.information(
                self, "警告", "處理失敗", QtWidgets.QMessageBox.Close
            )
            error_traceback = traceback.format_exc()
            print(error_traceback)
            if not os.path.isdir("ErrorLog"):
                os.mkdir("ErrorLog")
            date = datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")
            with open(
                "ErrorLog/ErrorLog_{}.txt".format(date), "w", encoding="utf-8"
            ) as f:
                f.write(error_traceback)
            self.ui.ErrorLog.setText(error_traceback)
        self.ui.StartButton.setEnabled(True)
        self.ui.StartButton.setText("開始")


if __name__ == "__main__":
    app = QtWidgets.QApplication()
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
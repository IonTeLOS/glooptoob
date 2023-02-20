import sys
import os
import os.path
import webbrowser
import argparse
import atexit
import subprocess
import locale
from subprocess import CREATE_NO_WINDOW
from pathlib import Path
from PyQt5 import QtCore
from PyQt5.QtWidgets import QMainWindow, QWidget, QLabel, QLineEdit, QApplication, QPushButton, QVBoxLayout, QStatusBar, QMessageBox
from PyQt5.QtGui import QIcon
from pytube import YouTube
from pytube import Playlist
from pytube import Search


class InstallDialog(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'Install GloopToob'
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        screen = app.primaryScreen()
        rect = screen.availableGeometry()
        self.setGeometry(round(int(rect.width()/2 - 200)),
                         round(int(rect.height()/2 - 100)), 400, 200)
        self.setFixedSize(400, 200)

        buttonReply = QMessageBox.question(
            self, 'GloopToob', "Do you want to install GloopToob?", QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        if buttonReply == QMessageBox.Yes:
            atexit.register(self.restart)
            atexit.register(self.install)
            app.quit()
        else:
            app.quit()
        self.show()

    def install(self):
        folder = "%USERPROFILE%\\Videos\\GloopToob\\"
        afolder = "%APPDATA%\\GloopToob\\"
        sfolder = "%APPDATA%\\Microsoft\\Windows\\Start Menu\\Programs\\"
        download_folder = os.path.expandvars(folder)
        app_folder = os.path.expandvars(afolder)
        start_folder = os.path.expandvars(sfolder)
        application_path = os.path.dirname(os.path.realpath(sys.executable))
        lpro = subprocess.Popen(["mkdir", download_folder], shell=True, stdin=None,
                                stdout=None, stderr=None, close_fds=True, creationflags=CREATE_NO_WINDOW)
        lpro = subprocess.Popen(["mkdir", app_folder], shell=True, stdin=None,
                                stdout=None, stderr=None, close_fds=True, creationflags=CREATE_NO_WINDOW)
        lpro = subprocess.Popen(["copy", application_path + '\\glooptoob.exe', app_folder], shell=True,
                                stdin=None, stdout=None, stderr=None, close_fds=True, creationflags=CREATE_NO_WINDOW)
        lpro = subprocess.Popen(["copy", sys._MEIPASS + '\\glooptoob.ico', app_folder], shell=True,
                                stdin=None, stdout=None, stderr=None, close_fds=True, creationflags=CREATE_NO_WINDOW)
        lpro = subprocess.Popen(["copy", sys._MEIPASS + '\\GloopToob.lnk', app_folder], shell=True,
                                stdin=None, stdout=None, stderr=None, close_fds=True, creationflags=CREATE_NO_WINDOW)
        cprocess = subprocess.Popen(["xcopy", app_folder + "GloopToob.lnk", start_folder, "/Y"], shell=True, 
                                stdin=None, stdout=None, stderr=None, close_fds=True, creationflags=CREATE_NO_WINDOW)
        sys.exit(0)
        
    def restart(self):
        apppath = "%APPDATA%\\GloopToob\\glooptoob.exe"
        self_path = os.path.expandvars(apppath)
        selfpath = str(Path(self_path))
        startprocess = subprocess.Popen([selfpath], shell=True, stdin=None,
                                stdout=None, stderr=None, close_fds=True, creationflags=CREATE_NO_WINDOW)


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        def get_path(filename):
            if hasattr(sys, "_MEIPASS"):
                return os.path.join(sys._MEIPASS, filename)
            else:
                return filename

        if getattr(sys, 'frozen', False):
            application_path = os.path.dirname(
                os.path.realpath(sys.executable))
            destination = os.path.expandvars(
                "%APPDATA%\\GloopToob\\glooptoob.exe")
            mydestination = Path(destination)
            if not mydestination.is_file():
                InstallDialog()
                sys.exit(0)
            else:
                print("GloopToob path: " + application_path + "\glooptoob")
        else:
            application_path = os.path.dirname(os.path.abspath(__file__))
            print("GloopToob path: " + application_path + "\glooptoob.py")
        self.setWindowTitle("GloopToob")
        self.setWindowIcon(QIcon(get_path("gt.png")))
        screen = app.primaryScreen()
        rect = screen.availableGeometry()
        self.setGeometry(round(int(rect.width()/2 - 200)),
                         round(int(rect.height()/2 - 200)), 400, 400)
        self.setFixedSize(400, 400)
        sourcelink = "<a href='https://github.com/iontelos/glooptoob'>Read More - Donate</a>"
        self.label = QLabel(self)
        self.label.setOpenExternalLinks(True)
        self.label.setTextFormat(QtCore.Qt.RichText)
        self.label.setText(
            '1. Paste/Type a YouTube URL <br><br>2. Click button to download <br><br>3. Search-Download first result <br><br>4. Open GloopToob media folder  <br><br>5. Repeat steps >> Enjoy!   ' + sourcelink)
        self.label.linkHovered.connect(self.donate_timer)
        self.label.setStyleSheet("font-weight: bold")
        self.line = QLineEdit(self)
        self.line.setPlaceholderText(
            'https://www.youtube.com/watch?v=...   OR search keyword')
        self.line.setClearButtonEnabled(True)
        self.line.returnPressed.connect(self.search)
        vbutton = QPushButton('Download video', self)
        vbutton.setIcon(QIcon(get_path("v_download.png")))
        vbutton.clicked.connect(self.get_video)
        vbutton.setToolTip('download video from the YouTube url entered above')
        abutton = QPushButton('   Get audio only', self)
        abutton.setIcon(QIcon(get_path("a_download.png")))
        abutton.clicked.connect(self.get_audio)
        abutton.setToolTip(
            'download only audio from the YouTube video url entered above')
        sbutton = QPushButton('    Search  +  Get', self)
        sbutton.setIcon(QIcon(get_path("s_download.png")))
        sbutton.clicked.connect(self.search_download)
        sbutton.setToolTip(
            'search YouTube for the keyword entered above \nand download the first video in the search results \nHint: press ENTER to just search YouTube in your browser')
        self.fbutton = QPushButton('Open media folder', self)
        self.fbutton.setObjectName("folderbutton")
        self.fbutton.setIcon(QIcon(get_path("f_download.png")))
        self.fbutton.setToolTip(
            'open folder containing your GloopToob downloads')

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.line)
        layout.addWidget(vbutton)
        layout.addWidget(abutton)
        layout.addWidget(sbutton)
        layout.addWidget(self.fbutton)
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
        self.sBar = QStatusBar()
        self.setStatusBar(self.sBar)
        QtCore.QMetaObject.connectSlotsByName(self)

    def get_video(self):
        folder = "%USERPROFILE%\\Videos\\GloopToob\\"
        download_folder = os.path.expandvars(folder)
        if not self.line.text().strip():
            print('Enter a valid url and try again')
            self.sBar.showMessage('Enter a valid url and try again')
        elif "&list" in self.line.text():
            self.sBar.showMessage('Downloading video playlist..')
            playlist = Playlist(self.line.text())
            for video in playlist.videos:
                print('downloading : {} with url : {}'.format(
                    video.title, video.watch_url))
                video.streams.filter(type='video', progressive=True, file_extension='mp4').order_by(
                    'resolution').desc().first().download(download_folder)
            print('Downloaded videos from requested playlist')
            self.sBar.showMessage('Your downloads are ready')
            self.line.clear()
        else:
            yt = YouTube(self.line.text())
            print('Downloading video: ' + yt.title)
            YouTube(self.line.text()).streams.filter(progressive=True, file_extension='mp4').order_by(
                'resolution').desc().first().download(download_folder)
            print('Downloaded requested video')
            self.sBar.showMessage('Downloaded ' + yt.title)
            self.line.clear()

    def get_audio(self):
        folder = "%USERPROFILE%\\Videos\\GloopToob\\"
        download_folder = os.path.expandvars(folder)
        if not self.line.text().strip():
            print('Enter a valid url and try again')
            self.sBar.showMessage('Enter a valid url and try again')
        elif "&list" in self.line.text():
            self.sBar.showMessage('Downloading audio playlist..')
            playlist = Playlist(self.line.text())
            for video in playlist.videos:
                print('downloading : {} with url : {}'.format(
                    video.title, video.watch_url))
                video.streams.filter(
                    only_audio=True).first().download(download_folder)
            print('Downloaded audio files from requested playlist')
            self.sBar.showMessage('Your downloads are ready')
            self.line.clear()
        else:
            yt = YouTube(self.line.text())
            print('Downloading audio: ' + yt.title)
            YouTube(self.line.text()).streams.filter(
                only_audio=True).first().download(download_folder)
            print('Downloaded requested audio')
            self.sBar.showMessage('Downloaded ' + yt.title)
            self.line.clear()

    def search_download(self):
        if not self.line.text().strip():
            print(
                'Please provide some context for your search >> Write a keyword or more to search for')
            self.sBar.showMessage('Write a keyword or more to search for')
        else:
            folder = "%USERPROFILE%\\Videos\\GloopToob\\"
            download_folder = os.path.expandvars(folder)
            s = Search(self.line.text())
            results = s.results
            first_result = results[0]
            print(
                f"Downloading video (first search result): {first_result.title}")
            webbrowser.open(
                'https://www.youtube.com/results?search_query=' + self.line.text())
            YouTube(first_result.watch_url).streams.filter(type='video', progressive=True,
                                                           file_extension='mp4').order_by('resolution').desc().first().download(download_folder)
            print('Download finished')
            self.sBar.showMessage(
                'Downloaded video of first YouTube search result')
            self.line.clear()

    def search(self):
        webbrowser.open(
            'https://www.youtube.com/results?search_query=' + self.line.text())

    @QtCore.pyqtSlot()
    def on_folderbutton_clicked(self):
        folder = "%USERPROFILE%\\Videos\\GloopToob\\"
        download_folder = os.path.expandvars(folder)
        print('Download folder: ' + download_folder)
        os.system("start " + download_folder)

    def donate_timer(self):
        self.sBar.showMessage('Donate to support app developer')
        self.timer = QtCore.QTimer(self)
        self.timer.singleShot(1500, self.donate)

    def donate(self):
        webbrowser.open("https://glooptoob.page.link/donate")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setApplicationName("GloopToob")
    app.setOrganizationName("TeLOS")
    app.setOrganizationDomain("https://teloslinux.org")
    mainWin = MainWindow()
    parser = argparse.ArgumentParser(prog="glooptoob", description="GloopToob : Download YouTube videos or their audio tracks, download all videos/audio tracks from a YouTube playlist, search YouTube and download first search result..",
                                     epilog="~~ Enjoy ! - read more-contribute : https://github.com/iontelos/glooptoob ~~")
    parser.add_argument(
        '-u', '--url', help='provide a YouTube url including the https:// part (optional)', required=False)
    parser.add_argument('-a', '--audio', help='download only audio (optional)',
                        default=False, action='store_true')
    parser.add_argument(
        '-s', '--search', help='search YouTube and download first result (optional - can be combined with --audio)', required=False)

    args = parser.parse_args()

    locale.setlocale(locale.LC_NUMERIC, "")
    folder = "%USERPROFILE%\\Videos\\GloopToob\\"
    download_folder = os.path.expandvars(folder)
    down_folder = Path(download_folder)
    if not down_folder.is_file():
        lpro = subprocess.Popen(["mkdir", down_folder], shell=True, stdin=None,
                                stdout=None, stderr=None, close_fds=True, creationflags=CREATE_NO_WINDOW,)

    if args.search and args.audio:
        s = Search(args.search)
        results = s.results
        first_result = results[0]
        print(f"Downloading audio (first search result): {first_result.title}")
        webbrowser.open(
            'https://www.youtube.com/results?search_query=' + args.search)
        YouTube(first_result.watch_url).streams.filter(
            only_audio=True).first().download(download_folder)
        os.system("start " + download_folder)
        print('Download finished')
        sys.exit(0)
    elif args.search:
        s = Search(args.search)
        results = s.results
        first_result = results[0]
        print(f"Downloading video (first search result): {first_result.title}")
        webbrowser.open(
            'https://www.youtube.com/results?search_query=' + args.search)
        YouTube(first_result.watch_url).streams.filter(type='video', progressive=True,
                                                       file_extension='mp4').order_by('resolution').desc().first().download(download_folder)
        os.system("start " + download_folder)
        print('Download finished')
        sys.exit(0)
    elif args.audio and args.url:
        yt = YouTube(args.url)
        print('Downloading audio: ' + yt.title)
        YouTube(args.url).streams.filter(
            only_audio=True).first().download(download_folder)
        print('Downloaded requested audio')
        sys.exit(0)
    elif args.url:
        yt = YouTube(args.url)
        print('Downloading video: ' + yt.title)
        YouTube(args.url).streams.filter(progressive=True, file_extension='mp4').order_by(
            'resolution').desc().first().download(download_folder)
        print('Downloaded requested video')
        sys.exit(0)
    else:
        mainWin.show()
        sys.exit(app.exec_())

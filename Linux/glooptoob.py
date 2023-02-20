import sys
import os
import os.path
import webbrowser
import argparse
import atexit
import subprocess
import locale
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
        self.setGeometry(round(int(rect.width()/2 - 200)), round(int(rect.height()/2 - 100)), 400, 200)
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
        application_path = os.path.dirname(os.path.realpath(sys.executable))
        destination = os.path.expandvars("/home/$USER/.local/bin/glooptoob")
        os.system("cp " + application_path + "/glooptoob " + destination)
    
    def restart(self):
        destination = os.path.expandvars("/home/$USER/.local/bin/glooptoob")
        selfpath = str(Path(destination))
        startprocess = subprocess.Popen([selfpath], shell=True, stdin=None, stdout=None, stderr=None, close_fds=True)


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        
        def get_path(filename):
            if hasattr(sys, "_MEIPASS"):
                return os.path.join(sys._MEIPASS, filename)
            else:
                return filename
        
        if getattr(sys, 'frozen', False):
            application_path = os.path.dirname(os.path.realpath(sys.executable))
            lbin = os.path.expandvars('/home/$USER/.local/bin/')
            destination = os.path.expandvars('/home/$USER/.local/bin/glooptoob')
            idest = os.path.expandvars('/home/$USER/.local/share/icons/')
            ddest = os.path.expandvars('/home/$USER/.local/share/applications/')
            fpath = os.path.expandvars('/home/$USER/Downloads/GloopToob/')
            mydestination = Path(destination)
            if not mydestination.is_file():
                icon = get_path("gt.png ")
                desktopfile = get_path("glooptoob.desktop ")
                os.system("mkdir -p " + lbin)
                os.system("mkdir -p " + idest)
                os.system("mkdir -p " + ddest)
                os.system("mkdir -p " + fpath)
                os.system("mv " + icon + idest + "glooptoob.png")
                os.system("cp " + desktopfile + ddest)
                InstallDialog()
                sys.exit(0)
            else:
                print("GloopToob path: " + application_path + "/glooptoob")
        else:
            application_path = os.path.dirname(os.path.abspath(__file__))
            print("GloopToob path: " + application_path + "/glooptoob.py")
        self.setWindowTitle("GloopToob") 
        self.setWindowIcon(QIcon(get_path("gt.png")))
        screen = app.primaryScreen()
        rect = screen.availableGeometry()
        self.setGeometry(round(int(rect.width()/2 - 200)), round(int(rect.height()/2 - 200)), 400, 400)
        self.setFixedSize(400, 400)
        sourcelink = "<a href='https://github.com/iontelos/glooptoob'>Read More - Donate</a><br>"
        self.label = QLabel(self)
        self.label.setOpenExternalLinks(True)
        self.label.setTextFormat(QtCore.Qt.RichText)
        self.label.setText('1. Paste/Type a YouTube URL <br><br>2. Click button to download <br><br>3. Search-Download first result <br><br>4. Open GloopToob media folder  <br><br>5. Repeat steps >> Enjoy!   ' + sourcelink)
        self.label.linkHovered.connect(self.donate_timer)
        self.label.setStyleSheet("font-weight: bold");
        self.line = QLineEdit(self)
        self.line.setFixedWidth(380)
        self.line.setPlaceholderText('https://www.youtube.com/watch?v=...   OR keyword')
        self.line.setClearButtonEnabled(True)
        self.line.returnPressed.connect(self.search)
        vbutton = QPushButton(' &Download video', self)
        vbutton.setIcon(QIcon(get_path("v_download.png")))
        vbutton.setFixedSize(250, 30)
        vbutton.clicked.connect(self.get_video)
        vbutton.setToolTip('download video from the YouTube url entered above')
        abutton = QPushButton('    &Get audio only', self)
        abutton.setIcon(QIcon(get_path("a_download.png")))
        abutton.setFixedSize(250, 30)
        abutton.clicked.connect(self.get_audio)
        abutton.setToolTip('download only audio from the YouTube video url entered above')
        sbutton = QPushButton('    &Search  +  Get', self)
        sbutton.setIcon(QIcon(get_path("s_download.png")))
        sbutton.setFixedSize(250, 30)
        sbutton.clicked.connect(self.search_download)
        sbutton.setToolTip('search YouTube for the keyword entered above \nand download the first video in the search results \nHint: press ENTER to just search YouTube in your browser')
        self.fbutton = QPushButton(' &Open GT folder', self)
        self.fbutton.setObjectName("folderbutton")
        self.fbutton.setIcon(QIcon(get_path("f_download.png")))          
        self.fbutton.setFixedSize(250, 30)
        self.fbutton.setToolTip('open folder containing your GloopToob downloads')
        qbutton = QPushButton('&Quit GloopToob', self)
        qbutton.setIcon(QIcon(get_path("q_download.png")))
        qbutton.setFixedSize(250, 30)
        qbutton.clicked.connect(app.quit)
        qbutton.setToolTip('Exit application')
        
        layout = QVBoxLayout()
        layout.addWidget(self.label, alignment=QtCore.Qt.AlignCenter)
        layout.addWidget(self.line, alignment=QtCore.Qt.AlignCenter)
        layout.addWidget(vbutton, alignment=QtCore.Qt.AlignCenter)
        layout.addWidget(abutton, alignment=QtCore.Qt.AlignCenter)
        layout.addWidget(sbutton, alignment=QtCore.Qt.AlignCenter)
        layout.addWidget(self.fbutton, alignment=QtCore.Qt.AlignCenter)
        layout.addWidget(qbutton, alignment=QtCore.Qt.AlignCenter)
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
        self.sBar = QStatusBar()
        self.setStatusBar(self.sBar)
        QtCore.QMetaObject.connectSlotsByName(self)
    
    def get_video(self):
        username = os.getlogin()
        if not self.line.text().strip():
            print('Enter a valid url and try again')
            self.sBar.showMessage('Enter a valid url and try again')
        elif "&list" in self.line.text():
            self.sBar.showMessage('Downloading video playlist..')
            playlist = Playlist(self.line.text())
            for video in playlist.videos:
                print('downloading : {} with url : {}'.format(video.title, video.watch_url))
                video.streams.filter(type='video', progressive=True, file_extension='mp4').order_by('resolution').desc().first().download('/home/' + username + '/Downloads/GloopToob')
            print('Downloaded videos from requested playlist')
            self.sBar.showMessage('Your downloads are ready')  
            self.line.clear()    
        else:
            yt = YouTube(self.line.text())
            print('Downloading video: ' + yt.title)
            YouTube(self.line.text()).streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first().download('/home/' + username + '/Downloads/GloopToob')
            print('Downloaded requested video')
            self.sBar.showMessage('Downloaded ' + yt.title)
            self.line.clear()
            
    def get_audio(self):
        username = os.getlogin()
        if not self.line.text().strip():
            print('Enter a valid url and try again')
            self.sBar.showMessage('Enter a valid url and try again')
        elif "&list" in self.line.text():
            self.sBar.showMessage('Downloading audio playlist..')
            playlist = Playlist(self.line.text())
            for video in playlist.videos:
                print('downloading : {} with url : {}'.format(video.title, video.watch_url))
                video.streams.filter(only_audio=True).first().download('/home/' + username + '/Downloads/GloopToob')
            print('Downloaded audio files from requested playlist')
            self.sBar.showMessage('Your downloads are ready')  
            self.line.clear()    
        else:
            yt = YouTube(self.line.text())
            print('Downloading audio: ' + yt.title)
            YouTube(self.line.text()).streams.filter(only_audio=True).first().download('/home/' + username + '/Downloads/GloopToob')
            print('Downloaded requested audio')
            self.sBar.showMessage('Downloaded ' + yt.title)
            self.line.clear()
    
    def search_download(self): 
        if not self.line.text().strip():
            print('Please provide some context for your search >> Write a keyword or more to search for')
            self.sBar.showMessage('Write a keyword or more to search for')
        else:
            username = os.getlogin()
            s = Search(self.line.text())
            results = s.results
            first_result = results[0]
            print(f"Downloading video (first search result): {first_result.title}")
            webbrowser.open('https://www.youtube.com/results?search_query=' + self.line.text())
            YouTube(first_result.watch_url).streams.filter(type='video', progressive=True, file_extension='mp4').order_by('resolution').desc().first().download('/home/' + username + '/Downloads/GloopToob')
            print('Download finished')
            self.sBar.showMessage('Downloaded video of first YouTube search result')
            self.line.clear()
    
    def search(self):
        webbrowser.open('https://www.youtube.com/results?search_query=' + self.line.text())
    
    @QtCore.pyqtSlot()        
    def on_folderbutton_clicked(self):
        folder = "~/Downloads/GloopToob/"
        download_folder = os.path.expanduser(folder)
        print("Opening media download folder >> " + download_folder)
        os.system("gio open " + download_folder)
     
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
    parser = argparse.ArgumentParser(prog="glooptoob", description="GloopToob : Download YouTube videos or their audio tracks, download all videos/audio tracks from a YouTube playlist, search YouTube and download first search result.",
                                     epilog="~~ Enjoy ! - read more-contribute : https://github.com/iontelos/glooptoob ~~")
    parser.add_argument(
        '-u', '--url', help='provide a YouTube url to download media, include https:// (optional - required when using this script in console mode)', required=False)
    parser.add_argument('-a', '--audio', help='download only audio (optional)',
                        default=False, action='store_true')
    parser.add_argument(
        '-s', '--search', help='search YouTube and download first result (optional - can be combined with --audio)', required=False)

    args = parser.parse_args()
    
    username = os.getlogin()
    locale.setlocale(locale.LC_NUMERIC,"")
    
    if args.search and args.audio:
        s = Search(args.search)
        results = s.results
        first_result = results[0]
        print(f"Downloading audio (first search result): {first_result.title}")
        webbrowser.open('https://www.youtube.com/results?search_query=' + args.search)
        YouTube(first_result.watch_url).streams.filter(only_audio=True).first().download('/home/' + username + '/Downloads/GloopToob')
        os.system("gio open /home/" + username + "/Downloads/GloopToob")
        print('Download finished')
        sys.exit(0)
    elif args.search:
        s = Search(args.search)
        results = s.results
        first_result = results[0]
        print(f"Downloading video (first search result): {first_result.title}")
        webbrowser.open('https://www.youtube.com/results?search_query=' + args.search)
        YouTube(first_result.watch_url).streams.filter(type='video', progressive=True, file_extension='mp4').order_by('resolution').desc().first().download('/home/' + username + '/Downloads/GloopToob')
        os.system("gio open /home/" + username + "/Downloads/GloopToob")
        print('Download finished')
        sys.exit(0)
    elif args.audio and args.url:
        yt = YouTube(args.url)
        print('Downloading audio: ' + yt.title)
        username = os.getlogin()
        YouTube(args.url).streams.filter(only_audio=True).first().download('/home/' + username + '/Downloads/GloopToob')
        print('Downloaded requested audio')
        sys.exit(0)
    elif args.url:
        yt = YouTube(args.url)
        print('Downloading video: ' + yt.title)
        YouTube(args.url).streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first().download('/home/' + username + '/Downloads/GloopToob')
        print('Downloaded requested video')
        sys.exit(0)
    else:
        mainWin.show()
        sys.exit( app.exec_() )

import sys
import os
import re
import groq
import markdown
from youtube_transcript_api import YouTubeTranscriptApi
from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QPushButton, QLabel, QTextEdit, QVBoxLayout, QHBoxLayout,QStatusBar
from PyQt5.QtGui import QIcon
from PyQt5 import QtCore

def extract_video_id(input_string):
	# Check if input_string is a URL
  if re.match(r'http(s)?:\/\/', input_string):
    # Check if it's a YouTube URL
    if 'youtube.com' in input_string:
      match = re.search(r'v=([^&]*)', input_string)
      if match:
        return match.group(1)
    elif 'youtu.be' in input_string:
      match = re.search(r'youtu\.be/([^&]*)', input_string)
      if match:
        return match.group(1)
    return input_string

class AppWindow(QWidget):
  def __init__(self):
    super().__init__()
    self.setWindowTitle('AI Summarised YouTube videos ( English Language )')
    self.setWindowIcon(QIcon('transcription.png'))
    self.resize(875, 590)
    self.setStyleSheet('font-size: 13px;')
    
    self.layout = {}
    self.layout['main'] = QVBoxLayout()
    self.setLayout(self.layout['main'])

    self.init_ui()
    
  def init_container(self):
    self.button = {}
    self.line_edit = {}
    self.label = {}
    
  def init_ui(self):
    self.init_container()
    self._add_video_input_section()
    self._add_output_section()
    self._add_button_section()
    #self._add_myLabel()
    
    self.status_bar = QStatusBar()
    self.layout['main'].addWidget(self.status_bar)
    
    
  def _add_video_input_section(self):
    self.layout['video_input'] = QHBoxLayout()
    self.layout['main'].addLayout(self.layout['video_input'])
    
    self.label['video_id'] = QLabel('Video URL:')
    self.layout['video_input'].addWidget(self.label['video_id'])
    
    self.line_edit['video_id'] = QLineEdit()
    self.line_edit['video_id'].setFixedWidth(500)
    self.line_edit['video_id'].setPlaceholderText('Enter video URL')
    self.layout['video_input'].addWidget(self.line_edit['video_id'])
    
    self.layout['video_input'].addStretch()


  def _add_output_section(self):
    self.label['output'] = QLabel('Transcript/ Summarise:'+" "*108+'By: Jeevan Bhandari |eMail: techways@live.com')
    self.layout['main'].addWidget(self.label['output'])
    
    self.text_edit = QTextEdit()
    self.layout['main'].addWidget(self.text_edit)
    
  def _add_button_section(self):
    self.layout['transcript_download'] = QHBoxLayout()
    self.layout['main'].addLayout(self.layout['transcript_download'])
    
    self.button['download_transcript'] = QPushButton('&Generate Transcript')
    self.button['download_transcript'].setFixedWidth(150)
    self.button['download_transcript'].setFixedHeight(25)
    self.button['download_transcript'].clicked.connect(self.download_transcript)
    self.button['download_transcript'].setStyleSheet('background-color: lightblue')
    self.layout['transcript_download'].addWidget(self.button['download_transcript'])
    
    self.button['summarize_transcript'] = QPushButton('&Summarise with AI')
    self.button['summarize_transcript'].setFixedWidth(150)
    self.button['summarize_transcript'].setFixedHeight(25)

    self.button['summarize_transcript'].clicked.connect(self.summarize_transcript)
    self.button['summarize_transcript'].setStyleSheet('background-color: lightblue')
    self.layout['transcript_download'].addWidget(self.button['summarize_transcript'])
    
    #self.layout['transcript_download'].addStretch()

  def download_transcript(self):
    video_id = self.line_edit['video_id'].text()
    
    if not video_id:
      self.status_bar.showMessage('Please enter a video ID or URL')
      return
    else:
      self.status_bar.clearMessage()
      
    video_url = extract_video_id(video_id)
    
    try:
      transcript = YouTubeTranscriptApi.get_transcript(video_url)
      transcript_text = '\n'.join([f"{line['text']}" for line in transcript])
      self.text_edit.setPlainText(transcript_text)
    except Exception as e:
      self.text_edit.setPlainText(f'Error: {e}')
      return

  def summarize_transcript(self):
    transcript_text = self.text_edit.toPlainText()
    if not transcript_text:
      self.status_bar.showMessage('Transcript is empty.')
      return
    else:
      self.status_bar.clearMessage()
      
      chat_completion = client.chat.completions.create(
        messages=[
          {
            "role": "user",
            "content": f"AI Summarised video-transcript in bullet points: \n\n{transcript_text}",
          }
        ],
        model="llama3-8b-8192",
        temperature=0.3
      )

      html_content =  markdown.markdown(chat_completion.choices[0].message.content)
      self.text_edit.setHtml(html_content)

  '''def _add_myLabel(self):
    self.status_bar.showMessage(" "*139+'By: Jeevan Bhandari | eMail: techways@live.com')

    self.layout['myId'] = QHBoxLayout()
    self.layout['main'].addLayout(self.layout['myId'])
    self.label['my_id1'] = QLabel('By: Jeevan Bhandari | eMail: techways@live.com')
    self.layout['myId'].addWidget(self.label['my_id1'])
    self.label['my_id1'].setAlignment(QtCore.Qt.AlignRight)'''
    

if __name__ == "__main__":
  API_KEY = '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'
  client = groq.Client(api_key=API_KEY)
  
  app = QApplication(sys.argv)
  app.setStyle('Fusion')
  app.setStyleSheet(open('darkpro.css').read())
  

  app_window = AppWindow()
  app_window.show()
  
  sys.exit(app.exec())
  
'''
  https://console.groq.com/keys
  jeevansinghbhandari@groq
  "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"
  '''
	
  
  
      



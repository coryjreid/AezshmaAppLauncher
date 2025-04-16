import json.encoder
import os
from pathlib import Path

ROOT_DIRECTORY = Path(f"{os.environ.get("APPDATA")}\\Aezshma")
APPLICATION_DIRECTORY = Path(f"{ROOT_DIRECTORY}\\Launcher")
DEFAULT_LOG_FILE = Path(f"{APPLICATION_DIRECTORY}\\Launcher.log")

SHUTDOWN_DELAY_SECONDS = 10

LOG_VIEWER_DIRECTORY = Path(f"{APPLICATION_DIRECTORY}\\bin\\snaketail")
LOG_VIEWER_EXECUTABLE = Path(f"{LOG_VIEWER_DIRECTORY}\\SnakeTail.exe")
LOG_VIEWER_SESSION_FILE = Path(f"{APPLICATION_DIRECTORY}\\SnakeTail.xml")
LOG_VIEWER_SESSION_FILE_CONTENT = """
<TailConfig>
  <TailFiles>
    <TailFileConfig>
      <FilePath/>
      <FileEncoding>System.Text.SBCSCodePageEncoding</FileEncoding>
      <FileCacheSize>1000</FileCacheSize>
      <FileCheckInterval>10</FileCheckInterval>
      <FileChangeCheckInterval>100</FileChangeCheckInterval>
      <FileCheckPattern>false</FileCheckPattern>
      <TitleMatchFilename>false</TitleMatchFilename>
      <TextColor>windowtext</TextColor>
      <BackColor>window</BackColor>
      <FontInvariant>Consolas, 12pt</FontInvariant>
      <BookmarkTextColor>Yellow</BookmarkTextColor>
      <BookmarkBackColor>Green</BookmarkBackColor>
      <Modeless>false</Modeless>
      <Title>Aezshma App Launcher</Title>
      <WindowState>Maximized</WindowState>
      <WindowSize>
        <Width>1380</Width>
        <Height>724</Height>
      </WindowSize>
      <WindowPosition>
        <X>-8</X>
        <Y>-31</Y>
      </WindowPosition>
      <ServiceName />
      <ServiceMachineName />
      <IconFile />
      <DisplayTabIcon>false</DisplayTabIcon>
      <ColumnFilterActive>false</ColumnFilterActive>
    </TailFileConfig>
  </TailFiles>
  <SelectedTab>0</SelectedTab>
  <WindowSize>
    <Width>1384</Width>
    <Height>797</Height>
  </WindowSize>
  <WindowPosition>
    <X>572</X>
    <Y>247</Y>
  </WindowPosition>
  <MinimizedToTray>false</MinimizedToTray>
  <AlwaysOnTop>true</AlwaysOnTop>
</TailConfig>
"""

const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('electronAPI', {
  windowMinimize: () => ipcRenderer.send('window-minimize'),
  windowMaximize: () => ipcRenderer.send('window-maximize'),
  windowFullscreen: () => ipcRenderer.send('window-fullscreen'),
  windowClose: () => ipcRenderer.send('window-close')
});

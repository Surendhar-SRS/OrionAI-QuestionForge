const { app, BrowserWindow, ipcMain } = require('electron');
const path = require('path');

function createWindow() {
  const isDev = !app.isPackaged;
  const win = new BrowserWindow({
    width: 1200,
    height: 800,
    frame: false, // Frameless window
    backgroundColor: '#0f172a', // Match dark theme background
    webPreferences: {
      nodeIntegration: true,
      contextIsolation: false, // For simple hackathon setup
    },
    titleBarStyle: 'hidden',
    autoHideMenuBar: true,
  });

  if (isDev) {
    win.loadURL('http://localhost:5176');
  } else {
    win.loadFile(path.join(__dirname, '../dist/index.html'));
  }

  // Window Control Handlers
  ipcMain.on('window-minimize', () => win.minimize());
  ipcMain.on('window-maximize', () => {
    if (win.isMaximized()) {
      win.unmaximize();
    } else {
      win.maximize();
    }
  });
  ipcMain.on('window-fullscreen', () => {
    win.setFullScreen(!win.isFullScreen());
  });
  ipcMain.on('window-close', () => win.close());
}

app.whenReady().then(() => {
  createWindow();

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      createWindow();
    }
  });
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

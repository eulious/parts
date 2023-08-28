import { app, BrowserWindow } from "electron"
import { join } from "path"
import "./ipc"

const isDev = process.argv[process.argv.length - 1].match("dev")

function createWindow() {
    const mainWindow = new BrowserWindow({
        height: 700,
        width: 1300,
        webPreferences: {
            preload: join(__dirname, "./preload.js"),
            contextIsolation: true,
            devTools: true
        }
    })
    if (isDev) {
        mainWindow.loadURL("http://localhost:5173")
        mainWindow.webContents.openDevTools()
    } else {
        mainWindow.loadFile("./dist/index.html")
        // mainWindow.webContents.openDevTools()
        // mainWindow.setMenu(null)
    }
}

app.on("ready", createWindow)

app.on("window-all-closed", () => {
    if (process.platform !== "darwin") {
        app.quit()
    }
})

app.on("activate", () => {
    if (BrowserWindow.getAllWindows().length === 0) {
        createWindow()
    }
})
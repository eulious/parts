import { contextBridge, ipcRenderer } from "electron"
contextBridge.exposeInMainWorld("node", { ipcRenderer })
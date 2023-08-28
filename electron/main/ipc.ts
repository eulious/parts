import { ipcMain, IpcMainInvokeEvent } from "electron";

ipcMain.handle("echo", async (event: IpcMainInvokeEvent, ...args: any) => {
    return { ...args }
})
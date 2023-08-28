import { invoke as tauriInvoke } from '@tauri-apps/api/tauri'

export const invoke: { [key: string]: (...args: any[]) => Promise<any> } = new Proxy({}, {
    get(target, method: string) {
        return (...args: any[]) => {
            return tauriInvoke(method, ...args)
        }
    }
})
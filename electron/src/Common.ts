export const invoke: { [key: string]: (...args: any[]) => Promise<any> } = new Proxy({}, {
    get(target, method) {
        return (...args: any[]) => {
            return (window as any).node.ipcRenderer.invoke(method, ...args)
        }
    }
})
import { css } from '@emotion/react'
import { invoke } from '@tauri-apps/api/tauri'
import { useState } from 'react'

export default function App() {
    const [text, setText] = useState("")

    async function onClick() {
        // await call('init')
        // await call('set', { key: "config", value: "fuga" })
        // await new Promise(s => setTimeout(s, 3000))
        // await call('get', { key: "config1" })
        await call('get_request')
    }

    async function call(method: string, option?: any) {
        await invoke(method, option).then(res => {
            console.log(res)
            setText(res as string)
        }).catch(e => {
            console.error(e)
            setText(e)
        })
    }

    return (
        <div>
            <header>
                <button onClick={onClick}> button </button>
                {text}
            </header>
        </div>
    );
}

const red = css({
    color: "red"
})
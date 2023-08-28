import { useEffect } from 'react'
import { invoke } from './Common'

export default function App() {
    useEffect(() => {
        invoke.echo("hoge").then(console.log)
    }, [])

    return (
        <div></div>
    )
}
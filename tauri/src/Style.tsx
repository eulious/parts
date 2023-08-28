import { css, Global } from "@emotion/react";
// import styled from "@emotion/styled";

export const styleValue = {
    muiPrimary: "#3f51b5",
    black3: "rgb(55, 57, 62)",
    black2: "rgb(49, 49, 54)",
    black1: "rgb(32, 34, 37)",
    white1: "#eee",
    blue1: "#37c0ff",
    paddingTop: "50px",
    paddingBottom: "2em",
    splitLength: "30vw",
}


export default function GlobalStyle() {
    return (
        <Global
            styles={css({
                body: {
                    fontFamily: '"Segoe UI", Meiryo, system-ui, -apple-system, BlinkMacSystemFont, sans-serif'
                },
                img: {
                    width: "auto",
                    height: "auto",
                    maxWidth: "100%",
                    maxHeight: "100%"
                }
            })}
        />
    )
}

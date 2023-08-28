import { build } from "esbuild"

build({
    bundle: true,
    entryPoints: ["./main/main.ts", "./main/preload.ts"],
    tsconfig: "./main/tsconfig.json",
    outdir: "./dist",
    platform: "node",
    external: ["electron"],
    minify: true
}).then(() => {
    console.log("main build complete")
})
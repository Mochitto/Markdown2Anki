import esbuild from "esbuild";
import { sassPlugin } from "esbuild-sass-plugin";

/*
ESBUILD API: https://esbuild.github.io/api/#build-api
Sass Plugin: https://www.npmjs.com/package/esbuild-sass-plugin
*/

esbuild
    .build({
        entryPoints: ["src/style/main.sass", "src/main.ts"],
        outdir: "dist",
        minify: true,
        bundle: true,
        plugins: [sassPlugin({
            type: "css",
        })],
    })
    .then(() => console.log("⚡ Build complete! ⚡"))
    .catch(() => process.exit(1));

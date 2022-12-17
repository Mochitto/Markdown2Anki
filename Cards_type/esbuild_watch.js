import esbuild from "esbuild";
import { sassPlugin } from "esbuild-sass-plugin";
import liveServer from "@compodoc/live-server"

// Look at https://stackoverflow.com/questions/70325815/how-to-setup-custom-esbuild-with-scss-purgecss-liveserver
// For more information on why and how this works.

// Turn on LiveServer on http://localhost:7000
liveServer.start({
    port: 5500,
    host: 'localhost',
    root: '',
    open: true,
    ignore: 'node_modules',
    wait: 0,
});

esbuild
    .build({
        entryPoints: ["src/style/main.sass", "src/main.ts"],
        outdir: "dist",
        minify: true,
        bundle: true,
        watch: true,
        plugins: [sassPlugin({
            type: "css",
        })],
    })
    .then(() => console.log("⚡ Build complete! Watching your files and live at localhost:5500! ⚡"))
    .catch(() => process.exit(1));
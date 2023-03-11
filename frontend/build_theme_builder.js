import esbuild from 'esbuild';
import path from "path";
import { sassPlugin } from "esbuild-sass-plugin";

// Bundle and minimize the CSS files using esbuild with csso plugin
esbuild.build({
  entryPoints: [path.join(".", "src", "style", "themeless_main.sass"), path.join(".", "src", "main.ts")],
  bundle: true,
  minify: true,
  outdir: path.join("..", "theme_builder"),
plugins: [sassPlugin({
    type: "css",
})],
}).then(() => console.log(`⚡ Theme builder's files built! ⚡`))
  .catch(() => process.exit(1));

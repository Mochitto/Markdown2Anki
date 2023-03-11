// This script is meant to bundle together CSS themes
// Which are divided in Highlight themes and UI themes
// This is so that you could, potentially, have different
// Themes between UI and Code highlighting.
import esbuild from 'esbuild';
import path from "path";

// Get the file path and filename from command line arguments
const [themePath] = process.argv.slice(2);
const fileName = path.basename(themePath)

// Bundle and minimize the CSS files using esbuild with csso plugin
esbuild.build({
  entryPoints: [themePath],
  bundle: true,
  minify: true,
  outfile: path.join("..", "themes", fileName),
}).then(() => console.log(`⚡ ${fileName} built! ⚡`))
  .catch(() => process.exit(1));

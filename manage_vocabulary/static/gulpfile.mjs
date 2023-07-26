import gulp from "gulp";
import {
  sassExpanded,
  sassCustomStyleMinified,
  sassThemeMinified,
} from "./sassTasks.mjs";
import { jsExpanded, jsMinified } from "./jsTasks.mjs";
import { vendor } from "./vendorTasks.mjs";
import { deleteSync } from "del";
import browserSync from "browser-sync";
const { stream, reload } = browserSync;

// Define reusable paths
const path = {
  // src: "src",
  dist: "manage_vocabulary",
  src_scss: "src/scss",
  src_js: "src/js",
  dist_vendor: "manage_vocabulary/vendor",
  dist_js: "manage_vocabulary/js",
  dist_css: "manage_vocabulary/css",
};

// Function to clean certain files/folders from the dist directory
async function clean() {
  return await deleteSync([path.dist_css, path.dist_js, path.dist_vendor]);
}

// Watch task
// function watch() {
//   global.watch = true;
//   gulp.watch(`${path.src_scss}/**/*.scss`, sassMinified);
//   gulp.watch(`${path.src_js}/**/*.js`, jsMinified);
// }

// Default task
export default gulp.series(
  clean,
  vendor,
  gulp.parallel(
    jsMinified,
    jsExpanded,
    sassCustomStyleMinified,
    sassThemeMinified
  )
  // watch
);

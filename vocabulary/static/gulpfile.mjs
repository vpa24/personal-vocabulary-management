import gulp from "gulp";
import { sassCustomStyleMinified, sassThemeMinified } from "./sassTasks.mjs";
import { jsThemeMinified, jsMinified } from "./jsTasks.mjs";
import { vendor } from "./vendorTasks.mjs";
import { deleteSync } from "del";
import browserSync from "browser-sync";
import uglify from "gulp-uglify";
import rename from "gulp-rename";
import path from "path";
const { stream, reload } = browserSync;

// Define reusable paths
const path_default = {
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
function watch() {
  global.watch = true;
  // jsWatch
  gulp
    .watch(`${path_default.src_js}/*.js`)
    .on("change", function (file_path, stats) {
      console.log("File " + file_path + " was changed");
      gulp
        .src(file_path)
        .pipe(uglify())
        .pipe(rename({ extname: ".min.js" }))
        .pipe(gulp.dest(path_default.dist_js));
    });

  // gulp.watch(`${path.src_scss}/**/*.scss`).on("change", function (path, stats) {
  //   sassCustomStyleMinified;
  //   jsMinified;
  //   console.log("File " + path + " was changed");
  //   // Additional actions to be performed on change
  // });
}

// Default task
export default gulp.series(
  clean,
  vendor,
  gulp.parallel(
    jsThemeMinified,
    sassThemeMinified,
    sassCustomStyleMinified,
    jsMinified
  )
  // watch
);
gulp.task("watch", watch);

import gulp from "gulp";
import rollup from "gulp-rollup";
import babel from "gulp-babel";
import uglify from "gulp-uglify";
import rename from "gulp-rename";
const path = {
  dist: "manage_vocabulary",
  src_js: "src/js",
  dist_js: "manage_vocabulary/js",
};

// Function to compile and minify JS
export function jsThemeMinified() {
  return gulp
    .src(`${path.src_js}/theme.js`)
    .pipe(
      rollup({
        allowRealFiles: true,
        input: `./${path.src_js}/theme.js`,
        output: {
          format: "iife",
        },
      })
    )
    .pipe(rename("theme.min.js"))
    .pipe(babel({ presets: [["@babel/env", { modules: false }]] }))
    .pipe(uglify({ output: { comments: /^!|@author|@version/i } }))
    .pipe(gulp.dest(path.dist_js));
}

export function jsMinified() {
  return gulp
    .src(`${path.src_js}/*.js`)
    .pipe(uglify())
    .pipe(rename({ extname: ".min.js" }))
    .pipe(gulp.dest(path.dist_js));
}

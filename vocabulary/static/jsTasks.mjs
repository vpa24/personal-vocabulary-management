import gulp from "gulp";
import rollup from "gulp-rollup";
import babel from "gulp-babel";
import uglify from "gulp-uglify";
import rename from "gulp-rename";

const path = {
  // src: "src",
  dist: "manage_vocabulary",
  src_scss: "src/scss",
  src_js: "src/js",
  dist_vendor: "manage_vocabulary/vendor",
  dist_js: "manage_vocabulary/js",
  dist_css: "manage_vocabulary/css",
};

// Function to compile and transpile JS with expanded output
export function jsExpanded() {
  return gulp
    .src(`${path.src_js}/theme.js`)
    .pipe(
      rollup({
        allowRealFiles: true,
        input: `./${path.src_js}/theme.js`,
        output: {
          format: "iife",
          banner: `
        /**
         * Finder | Directory & Listings Bootstrap Template
         * Copyright 2022 Createx Studio
         * Theme core scripts
         * 
         * @author Createx Studio
         * @version 1.4.1
         */
        `,
        },
      })
    )
    .pipe(babel({ presets: [["@babel/env", { modules: false }]] }))
    .pipe(gulp.dest(path.dist_js));
}

// Function to compile and minify JS
export function jsMinified() {
  return gulp
    .src(`${path.src_js}/theme.js`)
    .pipe(
      rollup({
        allowRealFiles: true,
        input: `./${path.src_js}/theme.js`,
        output: {
          format: "iife",
          banner: `
        /**
         * Finder | Directory & Listings Bootstrap Template
         * Copyright 2022 Createx Studio
         * Theme core scripts
         * 
         * @author Createx Studio
         * @version 1.4.1
         */
        `,
        },
      })
    )
    .pipe(rename("theme.min.js"))
    .pipe(babel({ presets: [["@babel/env", { modules: false }]] }))
    .pipe(uglify({ output: { comments: /^!|@author|@version/i } }))
    .pipe(gulp.dest(path.dist_js));
}

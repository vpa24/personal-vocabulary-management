import gulp from "gulp";
import rename from "gulp-rename";
import sourcemaps from "gulp-sourcemaps"
import dartSass from "sass";
import gulpSass from "gulp-sass";
import autoprefixer from "gulp-autoprefixer";
import browserSync from "browser-sync";
const { stream } = browserSync;

const path = {
  // src: "src",
  dist: "manage_vocabulary",
  src_scss: "src/scss",
  dist_vendor: "manage_vocabulary/vendor",
  dist_js: "manage_vocabulary/js",
  dist_css: "manage_vocabulary/css",
};

const sass = gulpSass(dartSass);

// Function to compile Sass with expanded output style
export function sassExpanded() {
  const options = {
    outputStyle: "expanded",
    precision: 10,
  };
  return gulp
    .src(`${path.src_scss}/custom_style.scss`)
    .pipe(sass(options).on("error", sass.logError)) // Use 'sass' directly as a function
    .pipe(autoprefixer({ cascade: false }))
    .pipe(gulp.dest(path.dist_css))
    .pipe(stream());
}

// Function to compile Sass with minified output style
export function sassCustomStyleMinified() {
  const options = {
    outputStyle: "compressed",
    precision: 10,
  };
  return gulp
    .src(`${path.src_scss}/custom_style.scss`)
    .pipe(sass(options).on("error", sass.logError)) // Use 'sass' directly as a function
    .pipe(autoprefixer({ cascade: false }))
	.pipe(rename({ suffix: '.min'}))
	.pipe(sourcemaps.write('.'))
    .pipe(gulp.dest(path.dist_css))
    .pipe(stream());
}

export function sassThemeMinified() {
  const options = {
    outputStyle: "compressed",
    precision: 10,
  };
  return gulp
    .src(`${path.src_scss}/theme.scss`)
    .pipe(sass(options).on("error", sass.logError)) // Use 'sass' directly as a function
    .pipe(autoprefixer({ cascade: false }))
	.pipe(rename({ suffix: '.min'}))
	.pipe(sourcemaps.write('.'))
    .pipe(gulp.dest(path.dist_css))
    .pipe(stream());
}

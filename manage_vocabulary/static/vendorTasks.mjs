import gulp from "gulp";
import packageJSON from "./package.json" assert { type: "json" };

const path = {
  // src: "src",
  dist: "manage_vocabulary",
  src_scss: "scss",
  src_js: "src/js",
  dist_vendor: "manage_vocabulary/vendor",
  dist_js: "manage_vocabulary/js",
  dist_css: "manage_vocabulary/css",
};
// Function to move vendor CSS and JS files from node_modules to dist folder
export function vendor() {
  const dependencies = Object.keys(packageJSON.dependencies);
  const vendor = dependencies.map((key) => {
    return key + "/**/*";
  });
  return gulp
    .src(vendor, { cwd: "node_modules", base: "node_modules" })
    .pipe(gulp.dest(path.dist_vendor));
}

var gulp = require("gulp");
var webpack = require("webpack");
var gutil = require("gulp-util");
var sass = require('gulp-ruby-sass');

var cssRoot = "./cocktails_app/static/css/";
var cssEntry = "cocktails_app/static/css/styles.sass";
var cssFiles = cssRoot + "**/*";

var jsRoot = "./cocktails_app/static/js/";
var jsEntry = jsRoot + "app.coffee";
var jsFiles = jsRoot + "**/*";

var webpackConfig = {
	entry: jsEntry,
	output: {
		path: jsRoot,
		filename: 'app.js',
	},
	module: {
		loaders: [
			{ test: /\.coffee$/, loader: "coffee-loader" },
		],
	}
};

gulp.task("default", function() {
	// compile on start
	gulp.start("compileCSS");
	gulp.start("compileJS");

	// compile on file change
	gulp.watch(cssFiles, ["compileCSS"]);
	gulp.watch(jsFiles, ["compileJS"]);
});

gulp.task('compileCSS', function() {
	return sass(cssEntry)
		.on('error', sass.logError)
		.pipe(gulp.dest(cssRoot));
});

gulp.task("compileJS", function(callback) {
	webpack(webpackConfig, function(err, stats) {
		if (err) {
			throw new gutil.PluginError("webpack", err);
		}

		gutil.log("[webpack]", stats.toString({
			// webpack compilation display options
		}));

		callback();
	});
});

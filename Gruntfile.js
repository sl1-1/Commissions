module.exports = function(grunt) {

    grunt.initConfig({
        clean: ['build/*'],
        bower_concat: {
            all: {
                dest: {
                    js: 'build/bower.js',
                    css: 'static/bower.css'
                },
                dependencies: {
                    'angular': ['jquery']
                },
                mainFiles: {
                    'angular-ui': ['build/angular-ui.js'],
                    'bootstrap': [
                        'dist/js/bootstrap.js',
                        'dist/css/bootstrap.css',
                        'dist/css/bootstrap-theme.css'
                    ]
                }
            }
        },
        uglify: {
            bower: {
                options: {
                    sourceMap: true,
                    sourceMapIncludeSources: true,
                    mangle: true,
                    compress: true
                },
                files: {
                    'static/main.min.js': 'build/main.js'
                }
            }
        },
        concat: {
            options: {
                // define a string to put between each file in the concatenated output
                separator: ';',
                sourceMap: true
            },
            dist: {
                // the files to concatenate
                src: ['build/*.js', 'Angular/scripts/main.js', 'Angular/scripts/*/*.js'],
                // the location of the resulting JS file
                dest: 'build/main.js'
            }
        },
        html2js: {
            options: {
                base: 'Angular',
                module: 'Commissions.templates',
                singleModule: true,
                useStrict: true,
                htmlmin: {
                    collapseBooleanAttributes: true,
                    collapseWhitespace: true,
                    removeAttributeQuotes: true,
                    removeComments: true,
                    removeEmptyAttributes: true,
                    removeRedundantAttributes: true,
                    removeScriptTypeAttributes: true,
                    removeStyleLinkTypeAttributes: true
                }
            },
            main: {
                src: ['Angular/templates/*.html'],
                dest: 'build/templates.js'
            }
        }
    });
    grunt.loadNpmTasks('grunt-bower-concat');
    grunt.loadNpmTasks('grunt-contrib-uglify');
    grunt.loadNpmTasks('grunt-contrib-concat');
    grunt.loadNpmTasks('grunt-html2js');
    grunt.loadNpmTasks('grunt-contrib-clean');

    grunt.registerTask('default', [
        'clean',
        'bower_concat',
        'html2js',
        'concat',
        'uglify'
    ]);
}
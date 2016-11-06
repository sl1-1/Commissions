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
                    sourceMapIn: 'build/main.js.map',
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
                src: [
                    'bower_components/jquery/dist/jquery.js',
                    'bower_components/moment/moment.js',
                    'bower_components/moment-timezone/moment-timezone.js',
                    'bower_components/bootstrap-daterangepicker/daterangepicker.js',
                    'bower_components/api-check/dist/api-check.js',
                    'bower_components/angular/angular.js',
                    'bower_components/angular-bootstrap/ui-bootstrap.js',
                    'bower_components/angular-bootstrap/ui-bootstrap-tpls.js',
                    'bower_components/angular-cookies/angular-cookies.js',
                    'bower_components/angular-daterangepicker/js/angular-daterangepicker.js',
                    'bower_components/angular-file-upload/dist/angular-file-upload.js',
                    'bower_components/angular-formly/dist/formly.js',
                    'bower_components/angular-formly-templates-bootstrap/dist/angular-formly-templates-bootstrap.js',
                    'bower_components/angular-moment/angular-moment.js',
                    'bower_components/angular-resource/angular-resource.js',
                    'bower_components/angular-daterangepicker/js/angular-daterangepicker.js',
                    'bower_components/angular-ui/build/angular-ui.js',
                    'bower_components/angular-ui-router/release/angular-ui-router.js',
                    'bower_components/angular-wizard/dist/angular-wizard.js',
                    'bower_components/angular-xeditable/dist/js/xeditable.js',
                    'bower_components/angularjs-slider/dist/rzslider.js',
                    'bower_components/ng-rollbar/ng-rollbar.js',
                    'bower_components/rangy/rangy-core.js',
                    'bower_components/rangy/rangy-classapplier.js',
                    'bower_components/rangy/rangy-highlighter.js',
                    'bower_components/rangy/rangy-selectionsaverestore.js',
                    'bower_components/rangy/rangy-serializer.js',
                    'bower_components/rangy/rangy-textrange.js',
                    'bower_components/textAngular/dist/textAngular-sanitize.js',
                    'bower_components/textAngular/dist/textAngularSetup.js',
                    'bower_components/textAngular/dist/textAngular.js',
                    'bower_components/angular-file-upload/angular-file-upload.js',
                    'bower_components/checklist-model/checklist-model.js',
                    'build/templates.js',
                    'Angular/scripts/main.js',
                    'build/config.js',
                    'Angular/scripts/controllers/*.js',
                    'Angular/scripts/services/*.js'
                ],
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
            }
            ,
            main: {
                src: [
                    'Angular/templates/*.html',
                    'Angular/templates/formly/*.html'
                ],
                dest: 'build/templates.js'
            }
        },
        replace: {
            dist: {
                options: {
                    patterns: [
                        {
                            match: 'gitsha',
                            replace: '<%= gitinfo.local.branch.current.SHA %>'
                        },
                        {
                            match: 'environment',
                            replace: 'development'
                        }
                    ]
                },
                files: [
                    {
                        expand: false,
                        flatten: true,
                        src: 'Angular/scripts/config.js',
                        dest: 'build/config.js'
                    }
                    ]
            }
        },
        gitinfo: {}
    });
    grunt.loadNpmTasks('grunt-gitinfo');
    grunt.loadNpmTasks('grunt-bower-concat');
    grunt.loadNpmTasks('grunt-contrib-uglify');
    grunt.loadNpmTasks('grunt-contrib-concat');
    grunt.loadNpmTasks('grunt-html2js');
    grunt.loadNpmTasks('grunt-contrib-clean');
    grunt.loadNpmTasks('grunt-replace');

    grunt.registerTask('default', [
        'gitinfo',
        'clean',
        'bower_concat',
        'html2js',
        'replace',
        'concat',
        'uglify'
    ]);
}
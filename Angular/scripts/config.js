function formlyConfig(formlyConfigProvider) {
    formlyConfigProvider.setType(
        {
            name: 'richEditor',
            templateUrl: 'templates/formly/richEditor.html',
            defaultOptions: {
                templateOptions: {
                    'toolbar': [
                        [
                            'h1',
                            'h2',
                            'h3'
                        ],
                        [
                            'bold',
                            'italics',
                            'strikeThrough'
                        ],
                        [
                            'ul'
                        ],
                        [
                            'justifyLeft',
                            'justifyCenter',
                            'justifyRight'
                        ],
                        [
                            'insertImage',
                            'insertLink'
                        ]
                    ]
                }
            }
        });
    formlyConfigProvider.setType(
        {
            name: 'richEditorFile',
            templateUrl: 'templates/formly/richEditor_file.html',
            defaultOptions: {
                templateOptions: {
                    'toolbar': [
                        [
                            'h1',
                            'h2',
                            'h3'
                        ],
                        [
                            'bold',
                            'italics',
                            'strikeThrough'
                        ],
                        [
                            'ul'
                        ],
                        [
                            'justifyLeft',
                            'justifyCenter',
                            'justifyRight'
                        ],
                        [
                            'insertImage',
                            'insertLink'
                        ]
                    ]
                }
            }
        });
    formlyConfigProvider.setType(
        {
            name: 'datepicker',
            templateUrl: 'templates/formly/datepicker.html',
            wrapper: ['bootstrapLabel', 'bootstrapHasError'],
            defaultOptions: {
                templateOptions: {
                    datepicker: {
                        'autoUpdateInput': false,
                        'singleDatePicker': true,
                        'timePicker': true,
                        'alwaysShowCalendars': true,
                        'locale': {
                            'format': 'YYYY/MM/DD h:mm A'
                        }
                    }
                }
            }
        });

    formlyConfigProvider.setType(
        {
            name: 'slider',
            templateUrl: 'templates/formly/slider.html'
        }
    );

}

app.config(
    [
        'formlyConfigProvider',
        formlyConfig
    ]
);


function configUrlRouter($stateProvider, $urlRouterProvider) {

    $urlRouterProvider.otherwise('/');

    $stateProvider
        .state('index', {
            url: '/',
            controller: 'IndexCtrl as vm',
            templateUrl: 'templates/index.html',
            data: {
                requireLogin: false
            }
        })
        .state('enter', {
            url: '/queue/{queue_id}/',
            controller: 'EntryCtrl as vm',
            templateUrl: 'templates/enter.html',
            data: {
                requireLogin: false
            }
        })
        .state('detailform', {
            url: '/queue/:queue_id/commission/:commission_id',
            controller: 'EntryCtrl as vm',
            templateUrl: 'templates/enter.html',
            data: {
                requireLogin: true
            }
        })
        .state('admin-commissions', {
            url: '/admin/queue/',
            controller: 'CommissionsCtrl',
            templateUrl: 'templates/commissions.html',
            data: {
                requireLogin: true
            }
        })
        .state('user-commissions', {
            url: '/user/commissions/',
            controller: 'CommissionsCtrl',
            templateUrl: 'templates/commissions.html',
            data: {
                requireLogin: true
            }
        })
        .state('commission', {
            url: '/commission/:commissionid/',
            controller: 'CommissionCtrl as vm',
            templateUrl: 'templates/commission.html',
            data: {
                requireLogin: true
            }
        })
        .state('admin-panel', {
            url: '/admin/',
            controller: 'AdminCtrl as vm',
            templateUrl: 'templates/admin.html',
            data: {
                requireLogin: true,
                requireAdmin: true
            }
        })
        .state('user-panel', {
            url: '/user/',
            templateUrl: 'templates/user.html',
            data: {
                requireLogin: true
            }
        })
        .state('admin-types', {
            url: '/admin/types/',
            controller: 'TypeCtrl as vm',
            templateUrl: 'templates/options.html',
            data: {
                requireLogin: true,
                requireAdmin: true
            }
        })
        .state('admin-sizes', {
            url: '/admin/sizes/',
            controller: 'SizeCtrl as vm',
            templateUrl: 'templates/options.html',
            data: {
                requireLogin: true,
                requireAdmin: true
            }
        })
        .state('admin-extras', {
            url: '/admin/extras/',
            controller: 'ExtraCtrl as vm',
            templateUrl: 'templates/options.html',
            data: {
                requireLogin: true,
                requireAdmin: true
            }
        })
        .state('admin-queues', {
            url: '/admin/queues/',
            controller: 'QueueCtrl as vm',
            templateUrl: 'templates/queues.html',
            data: {
                requireLogin: true,
                requireAdmin: true
            }
        });

}

app.config(
    [
        '$stateProvider',
        '$urlRouterProvider',
        configUrlRouter
    ]
);

function config_xeditable(editableOptions, editableThemes) {
    // editableThemes.bs3.inputClass = 'input-sm';
    editableThemes.bs3.buttonsClass = 'btn-sm';
    editableOptions.theme = 'bs3';
}

app.run(
    [
        'editableOptions',
        'editableThemes',
        config_xeditable
    ]
);

app.config(['$resourceProvider', function($resourceProvider) {
    // Don't strip trailing slashes from calculated URLs
    $resourceProvider.defaults.stripTrailingSlashes = false;
}]);

function httpProviderConfig($httpProvider) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
}

app.config(
    [
        '$httpProvider',
        httpProviderConfig
    ]
);

function RollbarConfig(RollbarProvider) {
    RollbarProvider.init({
        accessToken: '69281d2c5f4d4c9f8b5cf7a6faf9235e',
        captureUncaught: true,
        payload: {
            client: {
                javascript: {
                    source_map_enabled: true,
                    code_version: '@@gitsha',
                    guess_uncaught_frames: true
                }
            },
            environment: '@@environment'
        }
    });
}

app.config(
    [
        'RollbarProvider',
        RollbarConfig
    ]
);

function myHttpInterceptor($provide, $httpProvider) {
    function myHttpInterceptorFactory($q, Rollbar) {
        return {
            // optional method
            'request': function(config) {
                // do something on success
                return config;
            },

            // optional method
            'requestError': function(rejection) {
                return $q.reject(rejection);
            },


            // optional method
            'response': function(response) {
                // do something on success
                return response;
            },

            // optional method
            'responseError': function(rejection) {
                switch (rejection.status) {
                    case 403:
                        break;
                    default:
                        Rollbar.error(
                            'HTTP Error: ' + rejection.status, rejection);
                }
                return $q.reject(rejection);
            }
        };
    }

    $provide.factory(
        'myHttpInterceptor',
        [
            '$q',
            'Rollbar',
            myHttpInterceptorFactory
        ]
    );

    $httpProvider.interceptors.push('myHttpInterceptor');
}

app.config(
    [
        '$provide',
        '$httpProvider',
        myHttpInterceptor
    ]
);

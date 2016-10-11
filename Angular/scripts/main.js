// Declare app level module which depends on filters, and services
var app = angular.module('Commissions',
    [
        'Commissions.templates',
        'ngCookies',
        'CommissionService',
        'QueueService',
        'UserService',
        'ContactService',
        'TypeService',
        'SizeService',
        'ExtraService',
        'CSRFService',
        'textAngular',
        'formly',
        'formlyBootstrap',
        'rzModule',
        'daterangepicker',
        'xeditable',
        'mgo-angular-wizard',
        'ui.router',
        'ui',
        'ui.filters',
        'ngSanitize',
        'angularMoment',
        'ui.bootstrap',
        'ui.bootstrap.modal',
        'ngSanitize',
        'angularMoment',
        'ui.bootstrap',
        'ui.layout',
        'ui.grid',
        'ui.grid.resizeColumns',
        'ui.grid.selection',
        'tandibar/ng-rollbar'
    ]
);

function formlyConfig(formlyConfigProvider) {
    formlyConfigProvider.setType(
        {
            name: 'richEditor',
            template: '<text-angular ng-model="model[options.key]" required></text-angular>'
        });
    formlyConfigProvider.setType(
        {
            name: 'datepicker',
            templateUrl: 'templates/datepicker.html',
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
                requireLogin: true
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

app.config(['$httpProvider', function($httpProvider) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
}]);


app.config(['RollbarProvider', function(RollbarProvider) {
    RollbarProvider.init({
        accessToken: '69281d2c5f4d4c9f8b5cf7a6faf9235e',
        captureUncaught: true,
        payload: {
            environment: 'development'
        }
    });
}]);

function MainCtrl($rootScope, $scope, $state, UserData, CSRF, $cookies, loginModalService) {
    var csrftoken = $cookies.get('csrftoken');
    if (!csrftoken) {
        CSRF.get();
    }
    $rootScope.$on('$stateChangeStart', function(event, toState, toParams) {
        var requireLogin = toState.data.requireLogin;
        var requireAdmin = toState.data.requireAdmin;
        UserData.initial().then(function() {
            if (requireLogin && (!UserData.id)) {
                event.preventDefault();

                loginModalService().then(function() {
                    return $state.go(toState.name, toParams);
                })
                    .catch(function() {
                        return $state.go('index');
                    });
            }
            if (requireAdmin && (!UserData.is_staff)) {
                event.preventDefault();
                return $state.go('index');
            }
        });
    });
}

app.controller('MainCtrl',
    [
        '$rootScope',
        '$scope',
        '$state',
        'UserData',
        'CSRF',
        '$cookies',
        'loginModalService',
        MainCtrl
    ]
);

function NavCtrl($scope, $state, UserData, loginModalService) {
    $scope.user = UserData;

    $scope.login = function() {
        loginModalService();
    };

    $scope.logout = function() {
        $state.go('index');
        UserData.logout();
    };
}

app.controller('NavCtrl',
    [
        '$scope',
        '$state',
        'UserData',
        'loginModalService',
        NavCtrl
    ]
);

app.config(['$provide', '$httpProvider', function($provide, $httpProvider) {
    $provide.factory('myHttpInterceptor', ['$q', 'Rollbar', function($q, Rollbar) {
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
    }]);

    $httpProvider.interceptors.push('myHttpInterceptor');
}]);

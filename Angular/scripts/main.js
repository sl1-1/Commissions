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
        'ui.grid.selection'
    ],
    ['formlyConfigProvider', function config(formlyConfigProvider) {
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


    }]);

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
        .state('commissions', {
            url: '/admin/queue/',
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

function runRootScope($rootScope, $state, loginModalService) {

    $rootScope.$on('$stateChangeStart', function(event, toState, toParams) {
        var requireLogin = toState.data.requireLogin;
        var requireAdmin = toState.data.requireAdmin;
        $rootScope.user.$promise.then(function() {
            console.log($rootScope.user);
            if (requireLogin && (!$rootScope.user.id)) {
                // var url = $state.href(toState.name, toParams);
                // $window.location.href = '/account/login/?next=/' + url;
                event.preventDefault();

                loginModalService().then(function() {
                    return $state.go(toState.name, toParams);
                })
                    .catch(function() {
                        return $state.go('welcome');
                    });
            }
            if (requireAdmin && (!$rootScope.user.is_staff)) {
                // var url = $state.href(toState.name, toParams);
                // $window.location.href = '/account/login/?next=/' + url;
                event.preventDefault();
                return $state.go('index');
            }
        });

    });
}

app.run(
    [
        '$rootScope',
        '$state',
        'loginModalService',
        runRootScope
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


function MainCtrl($rootScope, $scope, User, CSRF, $cookies) {
    $rootScope.user = User.get();
    var csrftoken = $cookies.get('csrftoken');
    if (!csrftoken) {
        CSRF.get();
    }
}

app.controller('MainCtrl',
    [
        '$rootScope',
        '$scope',
        'User',
        'CSRF',
        '$cookies',
        MainCtrl
    ]
);

function NavCtrl($rootScope, $scope, User, loginModalService) {

    $rootScope.$watch('user', function() {
        console.log('User Change Detected');
        $scope.user = $rootScope.user;
    });
    $scope.user = $rootScope.user;

    $scope.login = function() {
        loginModalService();
    };

    $scope.logout = function() {
        User.logout().$promise.then(function(uservalue) {
            $rootScope.user = uservalue;
        });
    };
}

app.controller('NavCtrl',
    [
        '$rootScope',
        '$scope',
        'User',
        'loginModalService',
        NavCtrl
    ]
);






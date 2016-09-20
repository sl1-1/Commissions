// Declare app level module which depends on filters, and services
var app = angular.module('CommissionForm',
    ['ngCookies', 'CommissionService', 'QueueService', 'UserService', 'ContactService', 'TypeService', 'SizeService', 'ExtraService', 'CSRFService',
        'checklist-model', 'textAngular', 'formly', 'formlyBootstrap', 'rzModule', 'daterangepicker',
        'mgo-angular-wizard', 'ui.router', 'ui', 'ui.filters', 'ngSanitize', 'angularMoment', 'ui.bootstrap', 'ui', 'ui.filters', 'ui.bootstrap.modal', 'ngSanitize', 'angularMoment', 'ui.bootstrap', 'ui.layout', 'ui.grid', 'ui.grid.resizeColumns', 'ui.grid.selection'],
    function config(formlyConfigProvider) {
        var unique = 1;
        formlyConfigProvider.setType({
            name: 'repeatSection',
            templateUrl: 'repeatSection.html',
            controller: function($scope) {
                $scope.formOptions = {formState: $scope.formState};
                $scope.addNew = addNew;

                $scope.copyFields = copyFields;


                function copyFields(fields) {
                    fields = angular.copy(fields);
                    addRandomIds(fields);
                    return fields;
                }

                function addNew() {
                    $scope.model[$scope.options.key] = $scope.model[$scope.options.key] || [];
                    var repeatsection = $scope.model[$scope.options.key];
                    var newsection = {};
                    repeatsection.push(newsection);
                }

                function addRandomIds(fields) {
                    unique++;
                    angular.forEach(fields, function(field, index) {
                        if (field.fieldGroup) {
                            addRandomIds(field.fieldGroup);
                            return; // fieldGroups don't need an ID
                        }

                        if (field.templateOptions && field.templateOptions.fields) {
                            addRandomIds(field.templateOptions.fields);
                        }

                        field.id = field.id || (field.key + '_' + index + '_' + unique + getRandomInt(0, 9999));
                    });
                }

                function getRandomInt(min, max) {
                    return Math.floor(Math.random() * (max - min)) + min;
                }
            }
        });
        formlyConfigProvider.setType({
            name: 'richEditor',
            template: '<text-angular ng-model="model[options.key]" required></text-angular>'
        });
    });

app.config(['$stateProvider', '$urlRouterProvider', function($stateProvider, $urlRouterProvider) {

    $urlRouterProvider.otherwise('/');

    $stateProvider

        .state('index', {
            url: '/',
            controller: 'IndexCtrl as vm',
            templateUrl: '/templates/index.html',
            data: {
                requireLogin: false
            }
        })
        .state('enter', {
            url: '/queue/{queue_id}/',
            controller: 'EntryCtrl as vm',
            templateUrl: '/templates/enter.html',
            data: {
                requireLogin: true
            }
        })
        .state('detailform', {
            url: '/queue/:queue_id/commission/:commission_id',
            controller: 'EntryCtrl as vm',
            templateUrl: '/templates/enter.html',
            data: {
                requireLogin: true
            }
        })
        .state('commissionlist', {
            url: '/commissions/?queueid&commissionid',
            controller: 'CommissionListCtrl as vm',
            templateUrl: '/templates/commissions.html',
            data: {
                requireLogin: true
            }
        })
        .state('queues', {
            url: '/admin/queue/?queueid',
            controller: 'QueueCtrl as vm',
            templateUrl: '/templates/queue.html',
            data: {
                requireLogin: true
            }
        })
        .state('commission', {
            url: '/commission/:commissionid/',
            controller: 'CommissionCtrl as vm',
            templateUrl: '/templates/commission.html',
            data: {
                requireLogin: true
            }
        });
}]);

app.run(['$rootScope', '$window', '$location', '$state', 'loginModal', function($rootScope, $window, $location, $state, loginModal) {

    $rootScope.$on('$stateChangeStart', function(event, toState, toParams) {
        var requireLogin = toState.data.requireLogin;
        $rootScope.user.$promise.then(function() {
            console.log($rootScope.user);
            if (requireLogin && (!$rootScope.user.id)) {
                // var url = $state.href(toState.name, toParams);
                // $window.location.href = '/account/login/?next=/' + url;
                event.preventDefault();

                loginModal().then(function() {
                    return $state.go(toState.name, toParams);
                })
                    .catch(function() {
                        return $state.go('welcome');
                    });
            }
        });

    });
}]);

app.config(['$resourceProvider', function($resourceProvider) {
    // Don't strip trailing slashes from calculated URLs
    $resourceProvider.defaults.stripTrailingSlashes = false;
}]);

app.config(['$httpProvider', function($httpProvider) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
}]);

app.controller('MainCtrl', ['$rootScope', '$scope', 'User', 'CSRF', '$cookies', function($rootScope, $scope, User, CSRF, $cookies) {
    $rootScope.user = User.get();
    var csrftoken = $cookies.get('csrftoken');
    if (!csrftoken) {
        CSRF.get();
    }
}]);

app.controller('NavCtrl', ['$rootScope', '$scope', 'User', 'loginModal', function($rootScope, $scope, User, loginModal) {

    $rootScope.$watch('user', function() {
        console.log('User Change Detected');
        $scope.user = $rootScope.user;
    });
    $scope.user = $rootScope.user;

    $scope.login = function() {
      loginModal();
    };

    $scope.logout = function() {
        User.logout().$promise.then(function(uservalue) {
            $rootScope.user = uservalue;
        });
    };
}]);






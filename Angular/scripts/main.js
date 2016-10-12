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
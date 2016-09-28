function LoginModalCtrl($scope, User) {
    this.cancel = $scope.$dismiss;

    this.submit = function(username, password) {
        User.login({username: username, password: password})
            .$promise.then(function(uservalue) {
                $scope.$close(uservalue);
            }
        );
    };

}

app.controller('LoginModalCtrl',
    [
        '$scope',
        'User',
        LoginModalCtrl
    ]
);

function LoginModalService($uibModal, $rootScope) {

    function assignCurrentUser(uservalue) {
        $rootScope.user = uservalue;
        return uservalue;
    }

    return function() {
        var instance = $uibModal.open({
            templateUrl: 'templates/login.html',
            controller: 'LoginModalCtrl',
            controllerAs: 'LoginModalCtrl'
        });

        return instance.result.then(assignCurrentUser);
    };

}

app.service('loginModalService',
    [
        '$uibModal',
        '$rootScope',
        LoginModalService
    ]
);

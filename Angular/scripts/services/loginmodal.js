app.controller('LoginModalCtrl', ['$scope', 'User', function($scope, User) {
    this.cancel = $scope.$dismiss;

    this.submit = function(username, password) {
        User.login({username:username, password:password}).$promise.then(function(uservalue) {
            $scope.$close(uservalue);
        });
    };

}]);

app.service('loginModal', ['$uibModal', '$rootScope', function($uibModal, $rootScope) {

    function assignCurrentUser(uservalue) {
        $rootScope.user = uservalue;
        return uservalue;
    }

    return function() {
        var instance = $uibModal.open({
            templateUrl: 'templates/login.html',
            controller: 'LoginModalCtrl',
            controllerAs: 'LoginModalCtrl'
        })

        return instance.result.then(assignCurrentUser);
    };

}]);
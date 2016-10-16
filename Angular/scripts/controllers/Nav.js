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

app.directive('navBar', [function() {
    return {
        restrict: 'E',
        templateUrl: 'templates/nav.html',
        controller: [
            '$scope',
            '$state',
            'UserData',
            'loginModalService',
            NavCtrl
        ]
    };
}]);

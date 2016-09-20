app.controller('CommissionCtrl', ['$rootScope', '$scope', '$stateParams', 'Commission', function($rootScope, $scope, $stateParams, Commission) {
    console.log($stateParams);
    $scope.commission = Commission.get({CommissionId: $stateParams.commissionid});
    console.log($scope.commission);

    $scope.update = function() {
        console.log($scope.commission);
        if (typeof $scope.commission.type != 'number') {
            $scope.commission.type = $scope.commission.type.id;
        }
        if (typeof $scope.commission.size != 'number') {
            $scope.commission.size = $scope.commission.size.id;
        }
        $scope.commission.$save({CommissionId: $stateParams.commissionid}, function(response) {
                $scope.commission = Commission.get({CommissionId: $stateParams.commissionid});
            },function(response) {
                console.log(response);
            });
    };
}]);

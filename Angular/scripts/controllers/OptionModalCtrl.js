function OptionModalCtrl($scope, $uibModalInstance) {
    $scope.add = function() {
        console.log($scope.option);
        $scope.option.$save(
            function() {
                $scope.reload();
                $uibModalInstance.close();
            },
            function(response) {
                console.log(response);
            }
        );
    };

    $scope.cancel = function() {
        $uibModalInstance.dismiss('cancel');
    };
}

app.controller('OptionModalCtrl',
    [
        '$scope',
        '$uibModalInstance',
        OptionModalCtrl
    ]
);

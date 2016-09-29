function TypeCtrl($rootScope, $scope, $uibModal, Type) {
    $scope.slider = {
        min: 0,
        max: 50,
        options: {
            floor: 0,
            ceil: 50,
            step: 1,
            onEnd: function() {
                // Stupid Slider... No debounce... Poor server... This help
                $scope.filter.price_min = $scope.slider.min;
                $scope.filter.price_max = $scope.slider.max;
            }
        }
    };
    $scope.options = Type.getall();


    $scope.add = function() {
        var modalInstance = $uibModal.open({
            ariaLabelledBy: 'modal-title',
            ariaDescribedBy: 'modal-body',
            templateUrl: 'templates/optionmodal.html',
            controller: 'TypeModalCtrl',
            controllerAs: '$ctrl',
            size: 'lg'
        });
    };
}

app.controller('TypeCtrl',
    [
        '$rootScope',
        '$scope',
        '$uibModal',
        'Type',
        TypeCtrl
    ]
);

function TypeModalCtrl($scope, $uibModalInstance, Type) {
    $scope.option = new Type;
    $scope.add = function() {
        console.log($scope.option);
        $scope.option.$save(
            function(response) {
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

app.controller('TypeModalCtrl',
    [
        '$scope',
        '$uibModalInstance',
        'Type',
        TypeModalCtrl
    ]
);

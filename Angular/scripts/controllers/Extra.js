function ExtraCtrl($scope, $uibModal, Extra) {
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

    $scope.reload = function() {
        $scope.options = Extra.getall();
    };
    $scope.reload();

    $scope.add = function() {
        $scope.option = new Extra;
        var modalInstance = $uibModal.open({
            ariaLabelledBy: 'modal-title',
            ariaDescribedBy: 'modal-body',
            templateUrl: 'templates/optionmodal.html',
            controller: 'OptionModalCtrl',
            controllerAs: '$ctrl',
            size: 'lg',
            scope: $scope
        });
    };
}

app.controller('ExtraCtrl',
    [
        '$scope',
        '$uibModal',
        'Extra',
        ExtraCtrl
    ]
);


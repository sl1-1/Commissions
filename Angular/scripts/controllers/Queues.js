function QueueCtrl($scope, $uibModal, Queue) {
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
        $scope.queues = Queue.getall();
    };
    $scope.reload();

    $scope.add = function() {
        $scope.queue = new Queue;
        var modalInstance = $uibModal.open({
            ariaLabelledBy: 'modal-title',
            ariaDescribedBy: 'modal-body',
            templateUrl: 'templates/queuesmodal.html',
            controller: 'QueueModalCtrl',
            controllerAs: 'vm',
            size: 'lg',
            scope: $scope
        });
    };
}

app.controller('QueueCtrl',
    [
        '$scope',
        '$uibModal',
        'Queue',
        QueueCtrl
    ]
);

function QueueModalCtrl($scope, $uibModalInstance, Type,
                        Size, Extra, WizardHandler) {
    var vm = this;
    vm.fields = {
        step1: [
            {
                key: 'name',
                type: 'input',
                templateOptions: {
                    label: 'Name',
                    required: true,
                    labelProp: 'name'
                }
            },
            {
                key: 'start',
                type: 'datepicker',
                defaultValue: moment(),
                templateOptions: {
                    label: 'Start',
                    required: true,
                    labelProp: 'name',
                    type: 'text'
                }
            },
            {
                key: 'end',
                type: 'datepicker',
                templateOptions: {
                    label: 'End',
                    labelProp: 'name',
                    type: 'text'
                }
            }
        ],
        step2: [
            {
                key: 'types',
                type: 'multiCheckbox',
                templateOptions: {
                    label: 'Types',
                    required: true,
                    options: Type.getall(),
                    valueProp: 'id',
                    labelProp: 'name'
                }
            },
            {
                key: 'sizes',
                type: 'multiCheckbox',
                templateOptions: {
                    label: 'Sizes',
                    required: true,
                    options: Size.getall(),
                    valueProp: 'id',
                    labelProp: 'name'
                }
            },
            {
                key: 'extras',
                type: 'multiCheckbox',
                templateOptions: {
                    label: 'Extras',
                    options: Extra.getall(),
                    valueProp: 'id',
                    labelProp: 'name'
                }
            },
            {
                key: 'max_characters',
                type: 'input',
                defaultValue: 1,
                templateOptions: {
                    label: 'Max Characters',
                    type: 'number',
                    required: true,
                    min: 1,
                    step: 1
                }
            }
        ],
        step3: [
            {
                key: 'max_commissions_in_queue',
                type: 'input',
                defaultValue: 1,
                templateOptions: {
                    label: 'Max Commissions in Queue',
                    type: 'number',
                    required: true,
                    min: 1,
                    step: 1
                }
            },
            {
                key: 'max_commissions_per_person',
                type: 'input',
                defaultValue: 1,
                templateOptions: {
                    label: 'Max Commissions per Person',
                    type: 'number',
                    required: true,
                    min: 1,
                    step: 1
                }
            }
        ]
    };
    $scope.add = function() {
        console.log($scope.option);
        $scope.queue.$save(
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

    vm.exitValidation = function(form) {
        return form && !form.$invalid;
    };
    $scope.$watch(function() {
        // Watch for a wizard, then grab him!
        return WizardHandler.wizard();
    }, function(wizard) {
        if (wizard) {
            vm.wizard = wizard;
        }
    });
}

app.controller('QueueModalCtrl',
    [
        '$scope',
        '$uibModalInstance',
        'Type',
        'Size',
        'Extra',
        'WizardHandler',
        QueueModalCtrl
    ]
);

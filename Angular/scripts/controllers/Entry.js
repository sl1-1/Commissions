app.controller('EntryCtrl', ['$rootScope', '$scope', '$sce', 'Commission', 'Queue', 'User', 'Contact', '$state', '$stateParams', function($rootScope, $scope, $sce,
                                                                                                                                         Commission, Queue, User,
                                                                                                                                         Contact, $state, $stateParams) {
    var vm = this;
    vm.queue = {};
    console.log($stateParams);
    if ('queue_id' in $stateParams) {
        vm.queue = Queue.get({QueueId: $stateParams.queue_id});
    }
    if ('commission_id' in $stateParams) {
        vm.commission_id = $stateParams.commission_id;
        vm.updateCommission();
    }
    else {
        vm.queue.$promise.then(function(queue) {
            if (queue.existing != null) {
                vm.commission_id = queue.existing;
                vm.updateCommission();
                console.log(vm.commission_id);
            }
        });
        console.log('No Commission ID');
    }

    vm.updateCommission = function() {
        var commission = Commission.get({CommissionId: vm.commission_id});
        commission.$promise.then(function(commission) {

            var newextras = [];
            angular.forEach(commission.extras, function(extra) {
                newextras.push(extra.id);
            });
            commission.extras = newextras;
            vm.model = commission;
        });
    };

    vm.new_commission = function() {
        if (!vm.commission_id) {
            var com = new Commission;
            com.queue = vm.queue.id;
            console.log(com)
            com.$create(function(commission) {
                vm.commission_id = commission.id;
                vm.updateCommission();
            });
        }
        console.log(vm.model);
    };

    vm.finishWizard = finishWizard;

    vm.exitValidation = function(form) {
        return form && !form.$invalid;
    };
    vm.fields = {
        step1: [
            {
                key: 'type.id',
                type: 'select',
                templateOptions: {
                    label: 'Type',
                    required: true,
                    options: [],
                    valueProp: 'id',
                    labelProp: 'name'
                },
                expressionProperties: {
                    'templateOptions.options': function() {
                        return vm.queue.types;
                    }
                }
            },
            {
                key: 'size.id',
                type: 'select',
                templateOptions: {
                    label: 'Size',
                    required: true,
                    options: [],
                    valueProp: 'id',
                    labelProp: 'name'
                },
                expressionProperties: {
                    'templateOptions.options': function() {
                        return vm.queue.sizes;
                    }
                }
            },
            {
                key: 'extras',
                type: 'multiCheckbox',
                templateOptions: {
                    label: 'Extras',
                    options: [],
                    valueProp: 'id',
                    labelProp: 'name'
                },
                expressionProperties: {
                    'templateOptions.options': function() {
                        return vm.queue.extras;
                    }
                }
            },
            {
                key: 'characters',
                type: 'input',
                templateOptions: {
                    label: 'Characters',
                    type: 'number',
                    required: true,
                    min: 1,
                    step: 1
                },
                expressionProperties: {
                    'templateOptions.max': function() {
                        return vm.queue.max_characters;
                    }
                }
            }
        ],
        step2: [
            {
                key: 'message.message',
                type: 'richEditor'
            }
        ]
    };

// function definition
    function finishWizard() {
        vm.model.$save({CommissionId: vm.commission_id}, function(response) {
                $state.go('commission', {commissionid: vm.commission_id});
            },
            function(response) {
                console.log(response);
            });
    }
}]);

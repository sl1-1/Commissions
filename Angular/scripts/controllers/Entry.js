function EntryCtrl($scope, Commission, Queue, $state,
                   $stateParams, $window, UserData,
                   loginModalService, WizardHandler, $timeout) {
    var vm = this;
    // vm.queue = {};
    vm.user = UserData;
    console.log('User', vm.user);
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
            console.log(com);
            com.$create(function(commission) {
                vm.commission_id = commission.id;
                vm.updateCommission();
            }, function(data) {
                Rollbar.error('Error creating new Commission', data);
                $window.alert('An error occured, please report it');

            });
        }
        vm.next();
        console.log(vm.model);
    };

    vm.finishWizard = finishWizard;

    vm.exitValidation = function(form) {
        return form && !form.$invalid && Boolean(vm.user.id);
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
                type: 'slider',
                templateOptions: {
                    label: 'Characters',
                    type: 'number',
                    required: true,
                    min: 1,
                    step: 1,
                    slider: {
                        floor: 1,
                        ceil: 1,
                        step: 1
                    }
                },
                expressionProperties: {
                    'templateOptions.slider.ceil': function() {
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
        if (vm.user.id) {
            vm.model.$save({CommissionId: vm.commission_id}, function() {
                    $state.go('commission', {commissionid: vm.commission_id});
                },
                function(response) {
                    Rollbar.error('Commission Form submission Error', response);
                    $window.alert('There was an error processing this form');
                    console.log(response);
                });
        }
        else {
            Rollbar.error('Attempted to submit Commission' +
                ' form without being logged in');
        }
    }

    vm.login = function() {
        loginModalService().then(function() {
            var wz = WizardHandler.wizard();
            vm.new_commission();
            wz.next();
        }, function() {
            return false;
        });
    };

    vm.next = function() {
        // This is a clumsy fix for the min/max slider labels no showing
        var wz = WizardHandler.wizard();
        wz.next();
        $timeout(function() {
            // $scope.$broadcast('rzSliderForceRender');
            $scope.$broadcast('reCalcViewDimensions');
        }, 50);

    };
}


app.controller('EntryCtrl',
    [
        '$scope',
        'Commission',
        'Queue',
        '$state',
        '$stateParams',
        '$window',
        'UserData',
        'loginModalService',
        'WizardHandler',
        '$timeout',
        EntryCtrl
    ]
);

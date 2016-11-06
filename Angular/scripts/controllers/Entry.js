function EntryCtrl($scope, $state, $stateParams, $window, $timeout, $cookies,
                   Commission, Queue, UserData, loginModalService,
                   FileUploader, WizardHandler, ProgressModal) {
    var vm = this;

    // Set up our FileUploader, this has to be done before the page renders
    var csrftoken = $cookies.get('csrftoken');
    vm.uploader = new FileUploader({
        url: '/api/commissionfiles/',
        alias: 'img',
        headers: {
            'X-CSRFToken': csrftoken
        },
        removeAfterUpload: false
    });

    vm.uploader.onProgressAll = function(progress) {
        progress = (progress / 1.11) + 10;
        ProgressModal.updateProgress(progress);
    };

    vm.uploader.onBeforeUploadItem = function(item) {
        ProgressModal.updateStatus('Uploading: ' + item.file.name);
    };

    vm.uploader.onCompleteAll = function() {
        ProgressModal.close();
        $state.go('commission', {commissionid: vm.commission_id});
    };

    //generate our token, so we can attach the files to the message later.
    vm.token = moment().valueOf();

    vm.user = UserData;
    vm.queue = Queue.get({QueueId: $stateParams.queue_id});
    vm.queue.$promise.then(function(queue) {
        if (queue.existing) {
            vm.commission_id = queue.existing;
        }
    });

    vm.new_commission = function() {
        // Run this even if there is an existing commission
        // as the server will handle choosing between an
        // existing commission, or a new commission
        var com = new Commission;
        com.queue = vm.queue.id;
        com.$create(function(commission) {
            vm.commission_id = commission.id;
            vm.model = Commission.get({CommissionId: vm.commission_id});

            vm.uploader.formData = [
                {token: vm.token},
                {commission: vm.commission_id}
            ];
            vm.next();
        }, function(data) {
            Rollbar.error('Error creating new Commission', data);
            $window.alert('An error occured, please report it');

        });
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
                type: 'richEditorFile',
                templateOptions: {
                    uploader: vm.uploader
                }
            }
        ]
    };

    function finishWizard() {
        if (vm.user.id) {
            ProgressModal.open(0, 'I just got started');
            vm.model.message.token = vm.token;
            vm.model.$save({CommissionId: vm.commission_id}, function() {
                    ProgressModal.update(10, 'Details Submitted');
                    vm.uploader.uploadAll();
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
        console.log(vm.token);
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
            $scope.$broadcast('reCalcViewDimensions');
        }, 50);

    };

    vm.test = function() {
        ProgressModal.open(10, 'Modal?');
        $timeout(function() {
            ProgressModal.update(90, 'Modal!');
        }, 2000);
    };

}


app.controller('EntryCtrl',
    [
        '$scope',
        '$state',
        '$stateParams',
        '$window',
        '$timeout',
        '$cookies',
        'Commission',
        'Queue',
        'UserData',
        'loginModalService',
        'FileUploader',
        'WizardHandler',
        'ProgressModal',
        EntryCtrl
    ]
);

app.directive('fileListBuilder', [function() {
    return {
        scope: {
            uploader: '=uploader'
        },
        restrict: 'E',
        templateUrl: 'templates/file_list_builder.html',
        controller: ['$scope', function($scope) {
            $scope.id = Math.floor(Math.random() * 600000);
            $scope.result = [];
            $scope.filter_update = function($item) {
                $scope.result.push($item);
                $scope.values.splice($scope.values.indexOf($item), 1);
                $scope.data = '';
            };

            $scope.filter_focus = function() {
                angular.element('#listbuilder-input-' + $scope.id).focus();
            };

            $scope.focus = function() {
                angular.element('#listbuilder-' + $scope.id)
                    .addClass('listbuilder-focus');
            };

            $scope.blur = function() {
                angular.element('#listbuilder-' + $scope.id)
                    .removeClass('listbuilder-focus');
            };

        }]
    };
}]);



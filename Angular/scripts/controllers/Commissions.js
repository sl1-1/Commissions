function CommissionsCtrl($scope, $state, $timeout, Commission,
                         Queue, Type, Size, Extra, UserData) {
    $scope.user = UserData;
    $scope.view = $state.current.name;
    $scope.queues = Queue.getall();
    $scope.types = Type.getall();
    $scope.sizes = Size.getall();
    $scope.extras = Extra.getall();
    $scope.datepicker = {
        locale: {
            cancelLabel: 'Clear'
        },
        eventHandlers: {
            'cancel.daterangepicker': function() {
                $scope.filter.date = {
                    startDate: null,
                    endDate: null
                };
            }
        }
    };
    $scope.filter = {
        queue: [],
        type: [],
        size: [],
        extra: [],
        paid: [],
        status: [],
        char_min: 0,
        char_max: 50,
        date: {
            startDate: null,
            endDate: null
        }
    };
    $scope.paid_values = [
        {
            id: 0,
            name: 'Not Yet Requested',
            icon: 'monetization_on',
            icon_color: 'grey'
        },
        {
            id: 1,
            name: 'Invoiced',
            icon: 'monetization_on',
            icon_color: 'yellow'
        },
        {
            id: 2,
            name: 'Paid',
            icon: 'monetization_on',
            icon_color: 'green'
        },
        {
            id: 3,
            name: 'Refunded',
            icon: 'monetization_on',
            icon_color: 'red'
        }
    ];
    $scope.status_values = [
        {
            id: 0,
            name: 'Waiting',
            icon: 'hourglass_empty'
        },
        {
            id: 1,
            name: 'Sketched',
            icon: 'edit'
        },
        {
            id: 2,
            name: 'Lined',
            icon: 'gesture'
        },
        {
            id: 3,
            name: 'Coloured',
            icon: 'palette'
        },
        {
            id: 4,
            name: 'Finished',
            icon: 'done'
        },
        {
            id: 5,
            name: 'Canceled',
            icon: 'stop'
        },
        {
            id: 6,
            name: 'Please Revise',
            icon: 'reply'
        },
        {
            id: 7,
            name: 'Rejected',
            icon: 'block'
        }
    ];
    $scope.slider = {
        min: 0,
        max: 50,
        options: {
            floor: 0,
            ceil: 50,
            step: 1,
            onEnd: function() {
                // Stupid Slider... No debounce... Poor server... This help
                $scope.filter.char_min = $scope.slider.min;
                $scope.filter.char_max = $scope.slider.max;
            }
        }
    };

    $scope.load = function() {
        var queues = [];
        var types = [];
        var sizes = [];
        var extras = [];
        var paids = [];
        var statuses = [];
        angular.forEach($scope.filter.queue, function(item) {
            queues.push(item.id);
        });
        angular.forEach($scope.filter.type, function(item) {
            types.push(item.id);
        });
        angular.forEach($scope.filter.size, function(item) {
            sizes.push(item.id);
            console.log(item);
        });
        angular.forEach($scope.filter.extras, function(item) {
            extras.push(item.id);
        });
        angular.forEach($scope.filter.paid, function(item) {
            paids.push(item.id);
        });
        angular.forEach($scope.filter.status, function(item) {
            statuses.push(item.id);
        });
        var startDate = '';
        var endDate = '';
        if ($scope.filter.date.startDate && $scope.filter.date.endDate) {
            startDate = $scope.filter.date.startDate.utc().format();
            endDate = $scope.filter.date.endDate.utc().format();
        }
        var filter_values = {
            queue: queues.join(),
            type: types.join(),
            size: sizes.join(),
            extras: extras.join(),
            paid: paids.join(),
            status: statuses.join(),
            characters_0: $scope.filter.char_min,
            characters_1: $scope.filter.char_max,
            date_0: startDate,
            date_1: endDate
        };
        console.log($scope.view);
        if ($scope.view == 'user-commissions') {
            filter_values.user = $scope.user.username;
        }
        $scope.loading = true;
        $scope.commissions = Commission.getall(filter_values);
        $scope.commissions.$promise.then(function() {
            $scope.loading = false;
        });
    };
    $scope.user.initial().then(function() {
        $timeout(function() {
            $scope.$watch('filter', $scope.load, true);
        }, 100);
        //$scope.load();
    });

}

app.controller('CommissionsCtrl',
    [
        '$scope',
        '$state',
        '$timeout',
        'Commission',
        'Queue',
        'Type',
        'Size',
        'Extra',
        'UserData',
        CommissionsCtrl
    ]
);


app.directive('listBuilder', [function() {
    return {
        scope: {
            valuesin: '=builderValues',
            result: '=builderResults'
        },
        restrict: 'E',
        templateUrl: 'templates/commission_filter.html',
        controller: ['$scope', function($scope) {
            // console.log(typeof $scope.valuesin);
            $scope.values = []; //$scope.valuesin;
            if ('$promise' in $scope.valuesin) {
                $scope.valuesin.$promise.then(function() {
                    $scope.values = angular.copy($scope.valuesin);
                });
            }
            else {
                $scope.values = angular.copy($scope.valuesin);
            }
            console.log($scope.values);
            $scope.id = Math.floor(Math.random() * 600000);
            $scope.result = [];
            $scope.filter_update = function($item) {
                $scope.result.push($item);
                $scope.values.splice($scope.values.indexOf($item), 1);
                $scope.data = '';
            };

            $scope.filter_delete = function($event, store_model, $index) {
                var item = $scope.result.splice($index, 1)[0];
                if ('id' in item) {
                    if (typeof item.id == 'number') {
                        $scope.values.splice(item.key, 0, item);
                    }
                    else {
                        $scope.values.push(item);
                    }
                }
                else {
                    $scope.values.push(item);
                }
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

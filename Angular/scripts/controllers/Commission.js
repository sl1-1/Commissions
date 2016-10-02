function CommissionCtrl($rootScope, $scope, $stateParams, Commission, Queue) {
    $scope.user = $rootScope.user;
    $scope.paid_values = [
        [0, 'Not Yet Requested'],
        [1, 'Invoiced'],
        [2, 'Paid'],
        [3, 'Refunded']
    ];
    $scope.status_values = [
        [0, 'Waiting'],
        [1, 'Sketched'],
        [2, 'Lined'],
        [3, 'Coloured'],
        [4, 'Finished'],
        [5, 'Canceled'],
        [6, 'Please Revise'],
        [7, 'Rejected']
    ];
    $scope.commission = Commission
        .get({CommissionId: $stateParams.commissionid});

    $scope.commission.$promise.then(function(commission) {
        $scope.queue = Queue.get({QueueId: commission.queue});
        console.log($scope.queue);
    });

    $scope.update = function() {
        console.log($scope.commission.status);
        $scope.commission.$save(
            {CommissionId: $stateParams.commissionid},
            function() {
                $scope.commission = Commission
                    .get({CommissionId: $stateParams.commissionid});
            },
            function(response) {
                console.log(response);
            }
        );
    };
}

app.controller('CommissionCtrl',
    [
        '$rootScope',
        '$scope',
        '$stateParams',
        'Commission',
        'Queue',
        CommissionCtrl
    ]
);

app.directive('statusChanges', [function() {
    return {
        scope: {
            changes: '=changes'
        },
        restrict: 'E',
        templateUrl: 'templates/status_change.html'
        // controller: ['$scope', function($scope) {
        //
        // }]
    };
}]);

app.filter('titleCase', function() {
    //http://stackoverflow.com/questions/24039226/angularjs-format-text-return-from-json-to-title-case
    return function(input) {
        input = input || '';
        return input.replace(/\w\S*/g, function(txt) {
            return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();
        });
    };
});

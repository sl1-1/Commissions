app.controller('CommissionListCtrl', ['$rootScope', '$scope', 'Commission', 'Queue', '$stateParams', 'Type', 'Size', 'Extra', function($rootScope, $scope,
                                                                                                                                       Commission, Queue, $stateParams, Type, Size, Extra) {

    console.log($stateParams);
    var vm = this;

    if ('queueid' in $stateParams) {
        vm.queue = $stateParams.queueid;
    }

    if ('commissionid' in $stateParams) {
        vm.commissionid = $stateParams.commissionid;
    }


    vm.commissions = Commission.query(function(commissions) {
        if (vm.commissionid) {
            angular.forEach(commissions, function(commission) {
                if (vm.commissionid == commission.id) {
                    vm.commission = commission;
                    vm.queue = commission.queue;
                    vm.queue_name = commission.queue_name;
                }
            });
        }
    });

    vm.setQueue = function(queue) {
        vm.queue = queue;
        angular.forEach(vm.commissions, function(commission) {
                if (vm.queue == commission.queue) {
                    vm.queue_name = commission.queue_name;
                }
            });
    };
    vm.setCommission = function(commission) {
        vm.commission = commission;
    };
    console.log(vm.commissions);

    vm.getType = function(type) {
        Type.get({id: type}, function(type) {
            console.log(type);
        });
    };

}]);

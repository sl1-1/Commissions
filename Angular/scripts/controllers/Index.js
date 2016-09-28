function IndexCtrl($scope, $stateParams, Queue) {
    var vm = this;
    vm.queues = [];
    Queue.query(function(queues) {
        angular.forEach(queues, function(queue) {
            if (!queue.ended) {
                vm.queues.push(queue);
            }
        });
    });
}

app.controller('IndexCtrl',
    [
        '$scope',
        '$stateParams',
        'Queue',
        IndexCtrl
    ]
);

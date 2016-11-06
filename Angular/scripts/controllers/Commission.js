function CommissionCtrl($scope, $stateParams, $cookies, Commission, Queue,
                        ProgressModal, FileUploader, UserData) {
    // TODO: Switch from $scope to vm
    var vm = this;
    vm.user = UserData;
    vm.total = 0;
    vm.paid_values = [
        [0, 'Not Yet Requested'],
        [1, 'Invoiced'],
        [2, 'Paid'],
        [3, 'Refunded']
    ];
    vm.status_values = [
        [0, 'Waiting'],
        [1, 'Sketched'],
        [2, 'Lined'],
        [3, 'Coloured'],
        [4, 'Finished'],
        [5, 'Canceled'],
        [6, 'Please Revise'],
        [7, 'Rejected']
    ];

    var csrftoken = $cookies.get('csrftoken');
    vm.token = moment().valueOf();
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
        item.formData = [
            {token: vm.token},
            {commission: vm.commission.id}
        ];
    };

    vm.uploader.onCompleteAll = function() {
        ProgressModal.close();
        angular.forEach(vm.uploader.queue, function(item) {
            item.remove();
        });
        vm.commission = Commission
            .get({CommissionId: $stateParams.commissionid}, vm.load);

    };

    vm.commission_watch = function() {
        //Placeholder
    };

    vm.load = function() {
        vm.commissionOriginal = {};
        vm.queue = Queue.get({QueueId: vm.commission.queue});
        vm.commission.message = {message: undefined};
        angular.copy(vm.commission, vm.commissionOriginal);
        vm.commission_watch = $scope.$watch('vm.commission', function() {
            vm.update_total();
        }, true);
    };

    vm.commission = Commission
        .get({CommissionId: $stateParams.commissionid}, vm.load);

    vm.fields = [
        {
            key: 'message.message',
            type: 'richEditorFile',
            templateOptions: {
                uploader: vm.uploader
            }
        }
    ];

    vm.update = function() {
        vm.token = moment().valueOf();
        ProgressModal.open(0, 'I just got started');
        vm.commission.message.token = vm.token;
        //Unregister our watch
        vm.commission_watch();
        vm.commission.$save(
            {CommissionId: $stateParams.commissionid},
            function() {
                ProgressModal.update(10, 'Details Submitted');
                if (vm.uploader.queue.length > 0) {
                    vm.uploader.uploadAll();
                }
                else {
                    ProgressModal.close();
                    vm.commission = Commission
                        .get({
                            CommissionId: $stateParams.commissionid
                        }, vm.load);
                }
            },
            function(response) {
                console.log(response);
            }
        );
    };

    vm.update_total = function() {
        var total;
        total = vm.commission.type.price;

        total +=
            vm.commission.type.extra_character_price *
            vm.commission.characters;

        total += vm.commission.size.price;

        total +=
            vm.commission.size.extra_character_price *
            vm.commission.characters;

        angular.forEach(vm.commission.extras, function(extra) {
            total += extra.price;
            total += extra.extra_character_price * vm.commission.characters;
        });
        vm.total = total;
    };

    var changewarning = 'You have unsaved changes, do you still want to leave?';

    function onbeforeunload() {
        if (!angular.equals(vm.commission, vm.commissionOriginal)) {
            return changewarning;
        }
    };

    window.onbeforeunload = onbeforeunload;

    $scope.$on('$stateChangeStart', function(event) {
        if (!angular.equals(vm.commission, vm.commissionOriginal)) {
            if (!window.confirm(changewarning)) {
                event.preventDefault();
            }
            else {
                window.onbeforeunload = null;

            }
        }
        else {
            window.onbeforeunload = null;

        }
    });

}

app.controller('CommissionCtrl',
    [
        '$scope',
        '$stateParams',
        '$cookies',
        'Commission',
        'Queue',
        'ProgressModal',
        'FileUploader',
        'UserData',
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

function LoginModalCtrl($scope, User) {
    vm = this;

    vm.login_form = {};
    vm.register_form = {};

    vm.login_fields = [
        {
            key: 'username',
            type: 'input',
            templateOptions: {
                label: 'Username',
                required: true,
                options: [],
                valueProp: 'id',
                labelProp: 'name'
            }
        },
        {
            key: 'password',
            type: 'input',
            templateOptions: {
                label: 'Password',
                type: 'password',
                required: true,
                options: [],
                valueProp: 'id',
                labelProp: 'name'
            }
        }
    ];

    vm.register_fields = [
        {
            key: 'username',
            type: 'input',
            templateOptions: {
                label: 'Username',
                required: true,
                options: [],
                valueProp: 'id',
                labelProp: 'name'
            }
        },
        {
            key: 'email',
            type: 'input',
            templateOptions: {
                label: 'Email',
                required: true,
                type: 'email',
                options: [],
                valueProp: 'id',
                labelProp: 'name'
            }
        },
        {
            key: 'password',
            type: 'input',
            templateOptions: {
                label: 'Password',
                type: 'password',
                required: true,
                options: [],
                valueProp: 'id',
                labelProp: 'name'
            }
        }
    ];

    vm.login = function() {
        console.log(vm.login_form);
        User.login(vm.login_form)
            .$promise.then(function(uservalue) {
                $scope.$close(uservalue);
            }
        );
    };

    vm.register = function() {
        User.register(vm.register_form)
            .$promise.then(function(uservalue) {
                $scope.$close(uservalue);
            }
        );
    };

}

app.controller('LoginModalCtrl',
    [
        '$scope',
        'User',
        LoginModalCtrl
    ]
);

function LoginModalService($uibModal, $rootScope) {

    function assignCurrentUser(uservalue) {
        $rootScope.user = uservalue;
        return uservalue;
    }

    return function() {
        var instance = $uibModal.open({
            templateUrl: 'templates/login.html',
            controller: 'LoginModalCtrl',
            controllerAs: 'vm'
        });

        return instance.result.then(assignCurrentUser);
    };

}

app.service('loginModalService',
    [
        '$uibModal',
        '$rootScope',
        LoginModalService
    ]
);

function LoginModalCtrl($scope, UserData) {
    vm = this;

    vm.login_form = {};
    vm.login_form_error = false;
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
        UserData.login(vm.login_form)
            .then(function(uservalue) {
                    $scope.$close(uservalue);
                },
                function(error) {
                    console.log(error);
                    vm.login_form_error = error.data;
                }
            );
    };

    vm.register = function() {
        UserData.register(vm.register_form)
            .then(function(uservalue) {
                    $scope.$close(uservalue);
                }
            );
    };

    vm.close = function() {
        $scope.close();
    };

}

app.controller('LoginModalCtrl',
    [
        '$scope',
        'UserData',
        LoginModalCtrl
    ]
);

function LoginModalService($uibModal) {

    function assignCurrentUser(uservalue) {
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

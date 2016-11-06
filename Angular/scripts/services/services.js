var QueueService = angular.module('QueueService', ['ngResource']);

QueueService.factory('Queue', ['$resource',
    function($resource) {
        return $resource('/api/queues/:QueueId/', {}, {
            query: {
                method: 'GET',
                url: '/api/queues/',
                isArray: true
            },
            get: {
                method: 'GET',
                params: {QueueId: 'queue'}
            },
            commissions: {
                method: 'GET',
                url: '/api/queues/:QueueId/commissions/',
                params: {QueueId: 'queue'},
                isArray: true
            },
            getall: {
                method: 'GET',
                url: '/api/queues/',
                isArray: true
            }
        });
    }]);

var CommissionService = angular.module('CommissionService', ['ngResource']);

commissionSave = function(data) {
    console.log(data);
    if (typeof data.type != 'number') {
        data.type = data.type.id;
    }
    if (typeof data.size != 'number') {
        data.size = data.size.id;
    }
    for (var i in data.extras) {
        if (typeof data.extras[i] != 'number') {
            data.extras[i] = data.extras[i].id;
        }
    }
    if (typeof data.paid != 'number') {
        data.paid = data.paid[0];
    }
    if (typeof data.status != 'number') {
        data.status = data.status[0];
    }
    if (!('message' in data)) {
        data.message = {};
    }
    if (!('token' in data.message)) {
        // Worst way to do this? Possibly
        data.message.token = data.id + '-' + moment();
    }
    return angular.toJson(data);
};

CommissionService.factory('Commission', ['$resource',
    function($resource) {
        return $resource('/api/commissions/', {}, {
            create: {
                method: 'POST',
                url: '/api/commissions/'
            },
            get: {
                method: 'GET',
                url: '/api/commissions/:CommissionId/',
                params: {CommissionId: 'commission'}
            },
            save: {
                method: 'PUT',
                url: '/api/commissions/:CommissionId/',
                params: {CommissionId: 'commission'},
                transformRequest: commissionSave
            },
            getall: {
                method: 'GET',
                isArray: true
            }
        });
    }]);


var UserService = angular.module('UserService', ['ngResource']);

UserService.factory('User', ['$resource',
    function($resource) {
        return $resource('/api/user/', {}, {
            get: {
                method: 'GET',
                url: '/api/user/current/'
            },
            login: {
                method: 'POST',
                url: '/api/user/login/'
            },
            logout: {
                method: 'GET',
                url: '/api/user/logout/'
            },
            register: {
                method: 'POST',
                url: '/api/user/register/'
            }
        });
    }]);

function UserData($q, User) {
    var userData = {};

    userData.id = false;
    userData.username = false;
    userData.is_staff = false;
    userData.logged_in = false;

    function update(data) {
        console.log(data);
        userData.id = data.id;
        userData.username = data.username;
        userData.is_staff = data.is_staff;
        userData.logged_in = Boolean(userData.id);
        return userData;
    }

    var initial = User.get().$promise.then(update);

    userData.login = function(login_data) {
        // Returns a promise, so the caller can tell if this failed or not.
        return User.login(login_data).$promise.then(update);
    };

    userData.register = function(register_data) {
        // Returns a promise, so the caller can tell if this failed or not.
        return User.register(register_data).$promise.then(update);
    };

    userData.logout = function() {
        User.logout().$promise.then(update);
    };

    userData.initial = function() {
        return initial;
    };

    return userData;
}

app.factory('UserData', ['$q', 'User', UserData]);

var ContactService = angular.module('ContactService', ['ngResource']);

ContactService.factory('Contact', ['$resource',
    function($resource) {
        return $resource('/api/contact/', {}, {
            query: {method: 'GET', isArray: true}
        });
    }]);

var TypeService = angular.module('TypeService', ['ngResource']);

TypeService.factory('Type', ['$resource',
    function($resource) {
        return $resource('/api/type/:id/', {}, {
            get: {method: 'GET'},
            getall: {
                method: 'GET',
                url: 'api/type/',
                isArray: true
            }
        });
    }]);

var SizeService = angular.module('SizeService', ['ngResource']);

SizeService.factory('Size', ['$resource',
    function($resource) {
        return $resource('/api/size/:id/', {}, {
            query: {method: 'GET'},
            getall: {
                method: 'GET',
                url: 'api/size/',
                isArray: true
            }
        });
    }]);

var ExtraService = angular.module('ExtraService', ['ngResource']);

ExtraService.factory('Extra', ['$resource',
    function($resource) {
        return $resource('/api/extra/:id/', {}, {
            query: {method: 'GET'},
            getall: {
                method: 'GET',
                url: 'api/extra/',
                isArray: true
            }
        });
    }]);

var CSRFService = angular.module('CSRFService', ['ngResource']);


CSRFService.factory('CSRF', ['$resource',
    function($resource) {
        return $resource('/api/csrf', {}, {
            query: {method: 'GET'}
        });
    }]);

function progressModal($uibModal) {
    var self = {};

    function modalCtrl($scope, status) {
        //This does nothing right now...
        //Reserved for future use?
    }

    function open(progress, status) {
        self.status = {};
        self.status.progress = progress;
        self.status.message = status;
        self.modalInstance = $uibModal.open({
            templateUrl: 'templates/progressmodal.html',
            controller: ['$scope', 'status', modalCtrl],
            resolve: {
                status: function() {
                    return self.status;
                }
            }
        });
    }

    function update(progress, status) {
        self.status.progress = progress;
        self.status.message = status;
    }

    function updateProgress(progress) {
        self.status.progress = progress;
    }

    function updateStatus(status) {
        self.status.message = status;
    }

    function close() {
        self.modalInstance.close();
    }

    self.open = open;
    self.update = update;
    self.updateProgress = updateProgress;
    self.updateStatus = updateStatus;
    self.close = close;

    return self;
}

app.factory('ProgressModal', ['$uibModal', progressModal]);

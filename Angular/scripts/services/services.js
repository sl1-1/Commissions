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
    return angular.toJson(data);
};

CommissionService.factory('Commission', ['$resource',
    function($resource) {
        return $resource('/api/commissions/', {}, {
            query: {
                method: 'GET',
                url: '/api/commissions/ego/',
                isArray: true
            },
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


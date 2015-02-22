var siAgeApp = angular.module('SiAgeApp');

siAgeApp
    .factory('Players', function ($resource) {
        return $resource('/api/players/:playerId', {}, {
            query: {method: 'GET', params: {playerId: 'playerId'}, isArray: true}
        })
    });



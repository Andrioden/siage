var siAgeApp = angular.module('SiAgeApp');

siAgeApp
    .factory('GameSetting', function ($resource) {
        return $resource('/api/gamesettings/:settingName', {}, {
            query: {method: 'GET', params: {settingName: 'settingName'}, isArray: true, cache: true}
        })
    })
    .factory('Player', function ($resource) {
        return $resource('/api/players/:playerId', {}, {
            get: {method: 'GET', params: {playerId: 'playerId'}, isArray: false},
            query: {method: 'GET', isArray: true},
            save: {method: 'POST'},
            update: {method: 'PUT'}
        })
    })
    .factory('Game', function ($resource) {
        return $resource('/api/games/:gameId', {}, {
            get: {method: 'GET', params: {gameId: 'gameId'}, isArray: false},
            query: {method: 'GET', isArray: true},
            save: {method: 'POST'},
            update: {method: 'PUT'}
        })
    });


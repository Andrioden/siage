var siAgeApp = angular.module('SiAgeApp');

siAgeApp
    .factory('GameSettings', function ($resource) {
        return $resource('/api/gamesettings/:settingName', {}, {
            query: {method: 'GET', params: {settingName: 'settingName'}, isArray: true, cache: true}
        })
    })
    .factory('Players', function ($resource) {
        return $resource('/api/players/:playerId', {}, {
            get: {method: 'GET', params: {playerId: 'playerId'}, isArray: false},
            save: {method: 'POST'},
            update: {method: 'PUT'},
            query: {method: 'GET', isArray: true}
        })
    });
/*.factory('Game', ['$resources',
 function ($resource) {
 return $resource('/api/games/:gameId', {}, {
 query: {method: 'GET', params: {gameId:'gameId'}}
 })
 }])*/


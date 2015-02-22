var siAgeApp = angular.module('SiAgeApp');

siAgeApp
    .factory('GameSettings', function ($resource) {
        return $resource('/api/gamesettings/:settingName', {}, {
            query: {method: 'GET', params: {settingName: 'settingName'}, isArray: true}
        })
    })
    .factory('Players', function ($resource) {
        return $resource('/api/players/:playerId', {}, {
            query: {method: 'GET', params: {playerId: 'playerId'}, isArray: true}
        })
    });
/*.factory('Game', ['$resources',
 function ($resource) {
 return $resource('/api/games/:gameId', {}, {
 query: {method: 'GET', params: {gameId:'gameId'}}
 })
 }])*/


var siAgeApp = angular.module('SiAgeApp');

siAgeApp
    .factory('GameSetting', function ($resource) {
        return $resource('/api/gamesettings/', {}, {
            query: {method: 'GET', isArray: false, cache: true}
        })
    })
    .factory('Player', function ($resource) {
        return $resource('/api/players/:player_id', {player_id: '@playerId'}, {
            get: {method: 'GET', isArray: false},
            query: {method: 'GET', isArray: true},
            save: {method: 'POST'},
            update: {method: 'PUT'}
        })
    })
    .factory('Game', function ($resource) {
        return $resource('/api/games/:game_id', {game_id: '@gameId'}, {
            get: {method: 'GET', isArray: false},
            query: {method: 'GET', isArray: true},
            save: {method: 'POST'},
            update: {method: 'PUT'}
        })
    });


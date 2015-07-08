var siAgeApp = angular.module('SiAgeApp');

siAgeApp
    .factory('GameSetting', function ($resource) {
        return $resource('/api/gamesettings/', {}, {
            query: { method: 'GET', isArray: false, cache: true }
        });
    })

    .factory('Player', function ($resource) {
        return $resource('/api/players/:player_id', null, {
            get: { method: 'GET', isArray: false },
            query: { method: 'GET', isArray: true },
            save: { method: 'POST' },
            update: { method: 'PUT' }
        });
    })

    .factory('User', function ($resource) {
        return $resource('/api/users/me', {}, {
            get: { method: 'GET', isArray: false }
        });
    })

    .factory('Game', function ($resource) {
        return $resource('/api/games/:game_id', { game_id: '@gameId' }, {
            get: { method: 'GET', isArray: false, cache: true },
            query: { method: 'GET', isArray: true },
            save: { method: 'POST' },
            update: { method: 'PUT' }
        });
    })

    .factory('GlobalStats', function ($resource) {
        return $resource('/api/globalstats/', {}, {
            query: { method: 'GET', isArray: false }
        });
    })

    .factory('Civilization', function ($resource) {
        return $resource('/api/civs/:name', { name: '@name' }, {
            get: { method: 'GET', isArray: false },
            query: { method: 'GET', isArray: true },
            save: { method: 'POST' },
            update: { method: 'PUT' }
        });
    })

    .factory('Admin', function ($resource) {
        return $resource('/api/actions/admin/:action/', {}, {
            recalcrating: { method: 'POST', params: { action: 'recalcrating' }, isArray: false },
            cleandb: { method: 'POST', params: { action: 'cleandb' }, isArray: false },
            clearstats: { method: 'POST', params: { action: 'clearstats' }, isArray: false },
            adjustrating: { method: 'POST', params: { action: 'adjustrating' } }
        });        
    })

    .factory('SetupGame', function ($resource) {
        return $resource('/api/actions/setupgame/', {}, {
            submit: { method: 'POST' }
        });

    });
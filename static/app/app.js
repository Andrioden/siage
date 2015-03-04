var siAgeApp = angular.module('SiAgeApp', ['ngRoute', 'ngResource']);

siAgeApp.config(['$routeProvider', '$locationProvider',
    function ($routeProvider, $locationProvider) {
        $routeProvider.
            when('/home', {
                templateUrl: 'static/app/home/leagueview.html',
                controller: 'LeagueController'
            })
            .when('/registergame', {
                templateUrl: 'static/app/registergame/registergameview.html',
                controller: 'RegisterGameController'
            })
            .when('/players/:playerId', {
                templateUrl: 'static/app/player/playerview.html',
                controller: 'PlayerController'
            })
            .when('/registerplayer', {
                templateUrl: 'static/app/registerplayer/registerplayerview.html',
                controller: 'RegisterPlayerController'
            })
            .when('/games/:gameId', {
                templateUrl: 'static/app/game/gameview.html',
                controller: 'GameController'
            })
            .otherwise({
                redirectTo: '/home'
            });

        $locationProvider.html5Mode(true);
    }]);

siAgeApp.config(['$resourceProvider', function ($resourceProvider) {
    // Don't strip trailing slashes from calculated URLs
    $resourceProvider.defaults.stripTrailingSlashes = false;
}]);
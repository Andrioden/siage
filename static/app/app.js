var siAgeApp = angular.module('SiAgeApp', ['ngRoute', 'ngResource']);

siAgeApp.config(['$routeProvider', '$locationProvider',
    function ($routeProvider, $locationProvider) {
        $routeProvider.
            when('/home', {
                templateUrl: 'static/app/home/leagueview.html',
                controller: 'LeagueController'
            }).
            when('/registergame', {
                templateUrl: 'static/app/registergame/registergameview.html',
                controller: 'RegisterGameController'
            }).
            when('/profile', {
                templateUrl: 'static/app/profile/profileview.html',
                controller: 'ProfileController'
            }).
            otherwise({
                redirectTo: '/home'
            });

        $locationProvider.html5Mode(true);
    }]);
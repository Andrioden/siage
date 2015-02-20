var siAgeApp = angular.module('SiAgeApp');

siAgeApp.config(['$routeProvider',
  function ($routeProvider) {
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
  }]);
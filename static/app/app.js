var siAgeApp = angular.module('SiAgeApp', ['ngRoute', 'ngResource', 'ngAnimate']);


siAgeApp.controller('UserController',
    function ($scope, User, $routeParams) {
        User.get(
            function (data) {
                $scope.user = data;
            },
            function (error) {
                $scope.user = null;
            }
        );
    });

siAgeApp.config(['$routeProvider', '$locationProvider',
    function ($routeProvider, $locationProvider) {
        $routeProvider.
            when('/league', {
                templateUrl: 'static/app/league/leagueview.html',
                controller: 'LeagueController'
            })
            .when('/civs', {
                templateUrl: 'static/app/civilizations/civilizationsview.html',
                controller: 'CivilizationsController'
            })
            .when('/globalstats', {
                templateUrl: 'static/app/globalstats/globalstatsview.html',
                controller: 'GlobalStatsController'
            })
            .when('/civs/:name', {
                templateUrl: 'static/app/civilization/civilizationview.html',
                controller: 'CivilizationController'
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
            .when('/games', {
                templateUrl: 'static/app/games/gamesview.html',
                controller: 'GamesController'
            })
            .when('/setupgames', {
                templateUrl: 'static/app/setupgames/setupgamesview.html',
                controller: 'SetupGamesController'
            })
            .when('/admin', {
                templateUrl: 'static/app/admin/adminview.html',
                controller: 'AdminController'
            })
            .otherwise({
                redirectTo: '/league'
            });

        $locationProvider.html5Mode(true);
    }]);

siAgeApp.config(['$resourceProvider', function ($resourceProvider) {
    // Don't strip trailing slashes from calculated URLs
    $resourceProvider.defaults.stripTrailingSlashes = false;
}]);


siAgeApp.filter('yesNo', function () {
    return function (input) {
        return input ? 'Yes' : 'No';
    }
});


siAgeApp.filter('orderEmpty', function () {
    return function (array, key, type) {
        var present, empty, result;

        if (!angular.isArray(array)) return;

        present = array.filter(function (item) {
            return item[key];
        });

        empty = array.filter(function (item) {
            return !item[key];
        });

        switch (type) {
            case 'toBottom':
                result = present.concat(empty);
                break;
            case 'toTop':
                result = empty.concat(present);
                break;

            default:
                result = array;
                break;
        }
        return result;
    };
});

siAgeApp.directive('autoFocus', function ($timeout) {
    return {
        restrict: 'AC',
        link: function (_scope, _element) {
            $timeout(function () {
                _element[0].focus();
            }, 0);
        }
    };
});


siAgeApp.run(function ($rootScope) {
    $rootScope.getFriendlyErrorText = function (error) {
        if (error.data.error_message) {
            return error.data.error_message;
        }
        else return error;
    }
});


siAgeApp.directive('ngConfirmClick', [
    function() {
        return {
            link: function (scope, element, attr) {
                var msg = attr.ngConfirmClick || "Are you sure?";
                var clickAction = attr.confirmedClick;
                element.bind('click', function (event) {
                    console.log(JSON.stringify(msg));
                    if (window.confirm(msg)) {
                        scope.$apply(clickAction);
                    }
                });
            }
        };
    }
]);

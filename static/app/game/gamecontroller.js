var siAgeApp = angular.module('SiAgeApp');

siAgeApp.controller('GameController',
    function ($scope, Game, $routeParams) {
        Game.get({game_id: $routeParams.gameId},
            function (data) {
                $scope.game = data;
            },
            function (error) {
                $scope.gameInfoError = "Unable to load game info!";
            })
    });


var siAgeApp = angular.module('SiAgeApp');

siAgeApp.controller('GameController',
    function ($scope, Game, $routeParams) {
        Game.get({game_id: $routeParams.gameId},
            function (data) {
                $scope.game = data;
                $scope.game.date = new Date(data.date).toLocaleDateString();
                $scope.game.duration_minutes = data.duration_seconds/60;
            },
            function (error) {
                $scope.gameInfoError = "Unable to load game info!";
            })
    });

